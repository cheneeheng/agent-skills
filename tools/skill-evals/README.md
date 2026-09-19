# skill-evals

Runs [skill-creator](https://github.com/anthropics/claude-plugins-official)'s eval loop against a
skill in this repo, on Windows, with the installed `ceh-*` plugins kept out of the runs.

Two problems stop skill-creator's own flow from working here:

- **Baseline contamination.** skill-creator spawns its runs as `Agent` subagents, which inherit
  every installed plugin, so the "without skill" arm can still load the skill under test.
  `run_behavior.py` runs each arm as `claude -p --setting-sources project` from a throwaway git
  repo instead, which drops user settings and with them every user-enabled plugin and hook.
- **`select()` on Windows.** `scripts/run_eval.py` (the trigger eval behind `run_loop.py`) calls
  `select.select()` on a subprocess pipe, which raises `WinError 10093` on Windows.
- **Trigger runs contaminating each other.** Every parallel run wrote its uniquely-named copy of the
  same command into one shared `.claude/commands/`, so a session could invoke a sibling's copy and
  the name-match detection scored it as "did not trigger". The false-negative rate rose with
  `--num-workers`: at 6 workers a skill that triggers 3/3 serially scored 0/3. `run_eval.py` now
  gives each run its own temp project root.
- **cp1252 mangling the description under test.** `read_text()` with no encoding uses the locale
  encoding, so on Windows an em dash in a `description:` reached `claude -p` as `â€”`. Every
  read and write in `scripts/` is now explicitly utf-8. Fixing only the read would have been
  worse: cp1252 round-trips an em dash but cannot encode `→`, so the write would raise.

## Contents

| Path | What |
|------|------|
| `run_behavior.py` | Behavioral eval: builds a fixture repo per run from the eval's `setup`, runs the with-skill and without-skill arms, writes skill-creator's workspace layout plus `timing.json` |
| `scripts/` | Copy of skill-creator's trigger-eval scripts (`claude-plugins-official/skill-creator`, cache revision `3ea32df27be7`), Apache-2.0, see `LICENSE.txt`. Four patches, each marked `# Patch:`. Three in `run_eval.py`: a reader thread replaces `select()`, `--setting-sources project` is added to the `claude -p` call, and each run gets its own `tempfile.mkdtemp()` project root instead of a shared one (which drops `find_project_root()` and the `project_root` argument threaded through `run_eval()`, so `run_loop.py` no longer passes one). The fourth spans all five files: every `read_text`/`write_text` passes `encoding="utf-8"` |

## Eval definitions

Each skill keeps its own at `plugins/<plugin>/skills/<skill>/evals/evals.json`, in skill-creator's
schema with two additions:

- `name` — a kebab-case case name, used for the workspace folder and the viewer heading.
- `setup` — ordered steps that build the fixture repo, which starts on `main`. Each step, in order:
  switches to `branch` if given (creating it at the current HEAD when it does not exist), writes
  `files` (path → content), commits them if it has a `commit` message, and adds an annotated `tag`
  if given. Files from a final step without `commit` stay as uncommitted working-tree changes,
  which is what the prompt then acts on. The run starts on whichever branch the last step left.
- `remote` — `true` adds a bare `origin` beside the repo and pushes every branch and tag to it
  with upstreams set, so `git push`, `git pull`, and remote-branch deletion work and show up in
  `refs.txt`. It is a local path, not GitHub, so `gh` still has nothing to talk to.

Each run writes `commits.txt` (new commits with parents), `status.txt`, `refs.txt` (HEAD, the
full branch graph, tag types, and origin's refs), and `worktree.txt` for the grader, next to the
transcript. `worktree.txt` holds the `git diff HEAD` plus the full text of every untracked file,
captured before the fixture is deleted: without it a grader has to reconstruct what the run emitted
from the `Write`/`Edit` calls in the transcript, and `status.txt` gives only the changed paths.

## Run it

Run outputs go under `.agents_workspace/skill-evals/<skill>/skill-creator/` (git-ignored). `SC`
below is the installed skill-creator directory, e.g.
`~/.claude/plugins/cache/claude-plugins-official/skill-creator/<rev>/skills/skill-creator`.

```bash
WS=.agents_workspace/skill-evals/commit/skill-creator

# 1. Both arms, every eval. Each run is a real claude -p session and costs real tokens.
python tools/skill-evals/run_behavior.py plugins/ceh-git-workflow/skills/commit --workspace $WS --runs 1

# 2. Grade: one grader subagent per run following $SC/agents/grader.md, reading
#    run-K/outputs/ and writing run-K/grading.json (fields: text, passed, evidence).
#    Leave "timing" out of grading.json: aggregate_benchmark reads tokens from the sibling
#    timing.json only when grading.json has no timing block, and otherwise reports 0 tokens.

# 3. Aggregate and review. PYTHONIOENCODING stops the viewer's banner crashing a cp1252 console.
(cd $SC && python -m scripts.aggregate_benchmark "$OLDPWD/$WS/iteration-1" --skill-name commit)
PYTHONIOENCODING=utf-8 python $SC/eval-viewer/generate_review.py $WS/iteration-1 --skill-name commit \
  --benchmark $WS/iteration-1/benchmark.json
```

Trigger eval and description tuning run from anywhere: each run builds its own temp project root,
so nothing is written into this repo and no scratch directory is needed.

```bash
PYTHONPATH=<repo>/tools/skill-evals python -m scripts.run_loop \
  --eval-set <trigger-eval.json> --skill-path <repo>/plugins/ceh-git-workflow/skills/commit \
  --model claude-opus-5 --max-iterations 5 --verbose
```

`run_eval.py` prints its JSON to stdout and saves nothing, so redirect it. `--verbose` progress
goes to stderr and stays on screen:

```bash
python -m scripts.run_eval --eval-set <trigger-eval.json> --skill-path <skill> \
  --model claude-sonnet-5 --runs-per-query 3 --timeout 180 --verbose \
  > .agents_workspace/skill-evals/<skill>/trigger/$(date +%Y%m%d-%H%M%S).json
```

## What isolation does not cover

- **`~/.claude/CLAUDE.md` still loads** in both arms. Only `--bare` skips it, and `--bare` refuses
  OAuth. It is identical in both arms, so it shifts the baseline without favoring either side.
- **The default attribution line is present** in both arms, since user settings are skipped.
- **Permissions are an allowlist** (`ALLOWED_TOOLS`): git, file tools, and `rm`. Pushing works
  against the `remote` fixture, but `gh` is denied, so the `ceh-git-workflow` cases that reach a PR
  or GitHub release step assert that the run reports the step as not done rather than claiming it.
  Measuring the `gh` calls themselves needs that list extended and a `gh` stand-in.

## Skills that emit into `.claude/`

Claude Code applies a `safetyCheck` to every path under `.claude/`. It is not an allowlist question:
`--allowedTools "Write(.claude/**)"`, `--permission-mode acceptEdits`, an absolute-path
`permissions.allow` rule in a settings file, and a `PreToolUse` hook returning
`permissionDecision: "allow"` were each tested and each still denied. The hook demonstrably fires and
grants ordinary paths, so the check sits above the permission system, and in a `-p` session there is
nobody to approve the prompt.

A skill that emits into `.claude/skills/<name>/` therefore cannot write its own deliverable, and the
run grades as though it produced nothing or produced something in the wrong place — a false negative
that looks exactly like a skill defect. `ceh-workflow-builder`'s first graded round lost most of its
destination assertions this way.

`--skip-permissions` is the only route that measures it. It drops the allowlist and runs with
`--dangerously-skip-permissions`, so each session has unrestricted `Bash` in the fixture repo:

```bash
python tools/skill-evals/run_behavior.py plugins/ceh-workflow-builder/skills/build-agentic-workflow \
  --workspace .agents_workspace/skill-evals/build-agentic-workflow/skill-creator \
  --iteration 3 --timeout 900 --skip-permissions
```

The fixture is a throwaway git repo under the system temp directory, deleted after each run, but the
session is not otherwise sandboxed. Use it only for a skill whose emission destination is the thing
under test, and never with an eval whose `setup` writes anything you care about.
