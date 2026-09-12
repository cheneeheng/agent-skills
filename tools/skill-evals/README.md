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

## Contents

| Path | What |
|------|------|
| `run_behavior.py` | Behavioral eval: builds a fixture repo per run from the eval's `setup`, runs the with-skill and without-skill arms, writes skill-creator's workspace layout plus `timing.json` |
| `scripts/` | Copy of skill-creator's trigger-eval scripts (`claude-plugins-official/skill-creator`, cache revision `3ea32df27be7`), Apache-2.0, see `LICENSE.txt`. Two patches in `run_eval.py`, each marked `# Patch:` — a reader thread replaces `select()`, and `--setting-sources project` is added to the `claude -p` call |

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

Each run writes `commits.txt` (new commits with parents), `status.txt`, and `refs.txt` (HEAD, the
full branch graph, tag types, and origin's refs) for the grader, next to the transcript.

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

Trigger eval and description tuning run from a scratch directory holding an empty `.claude/`, so
`find_project_root()` writes its temporary command file there and not into this repo:

```bash
mkdir -p /tmp/trig/.claude && cd /tmp/trig
PYTHONPATH=<repo>/tools/skill-evals python -m scripts.run_loop \
  --eval-set <trigger-eval.json> --skill-path <repo>/plugins/ceh-git-workflow/skills/commit \
  --model claude-opus-5 --max-iterations 5 --verbose
```

## What isolation does not cover

- **`~/.claude/CLAUDE.md` still loads** in both arms. Only `--bare` skips it, and `--bare` refuses
  OAuth. It is identical in both arms, so it shifts the baseline without favoring either side.
- **The default attribution line is present** in both arms, since user settings are skipped.
- **Permissions are an allowlist** (`ALLOWED_TOOLS`): git, file tools, and `rm`. Pushing works
  against the `remote` fixture, but `gh` is denied, so the `ceh-git-workflow` cases that reach a PR
  or GitHub release step assert that the run reports the step as not done rather than claiming it.
  Measuring the `gh` calls themselves needs that list extended and a `gh` stand-in.
