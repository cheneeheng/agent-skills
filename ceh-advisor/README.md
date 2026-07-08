# ceh-advisor

Owned replacement for the native `/advisor`: the main session (whatever model it runs) consults a
stronger reviewer model at decision points, failure loops, irreversible actions, and
pre-completion gates. Two-layer triggering: soft (description-driven subagent routing) plus hard
(deterministic hooks that ship with the plugin).

The point is control and ownership of the prompt and trigger logic, not vendor independence —
the reviewer model is a single `model:` line in the agent frontmatter, swap it there.

## Contents

```
agents/ceh-advisor.md                  the advisor agent (model: opus — single line to change reviewer)
hooks/hooks.json                       wires both hooks; loads automatically with the plugin
scripts/ceh-advisor-guard.sh           PreToolUse: blocks destructive bash until advisor consulted
scripts/ceh-advisor-failure-watch.sh   PostToolUse: fires after N consecutive bash failures
```

## Install

```
/plugin install ceh-advisor@ceh-plugins --scope user
```

Hooks load with the plugin at session start — no settings.json merge, no manual copying. After
installing (or upgrading), restart Claude Code; hooks do not hot-swap mid-session.

Add `.claude/.ceh-advisor-ack` to your project's `.gitignore`.

Requires `jq` on PATH (the hook scripts parse their stdin payload with it). Without `jq` the
hooks degrade to inert — they allow everything silently instead of erroring — so the hard-trigger
layer only exists once `jq` is installed (`winget install jqlang.jq`, `brew install jq`,
`apt install jq`).

## Design

1. **Reviewer model lives in one place.** The `model:` frontmatter field is the single line to
   touch if the reviewer changes — no model assumptions are scattered through the prompt body.
2. **Two-layer trigger, not one.** Description-driven soft triggering alone repeats the exact
   failure mode that motivates this plugin (the model not recognizing it is at a decision point).
   The hook layer fires deterministically on conditions that should not depend on the model's
   judgment.
3. **Explicit handoff, not free transcript access.** Subagents spawn with a clean context window —
   unlike the native advisor, `ceh-advisor` does NOT see the main conversation. The main session
   must hand off context deliberately (see Handoff below).

## How the hard trigger works

**Destructive commands (guard).** When a Bash command matches a destructive pattern (`rm -rf`,
`git push --force`, `git reset --hard`, migrations, `terraform apply`, `kubectl delete`, etc.),
the guard denies it and tells the main session to:

1. Invoke `ceh-advisor` via Task with a full handoff block,
2. Write the advisor's one-line verdict into `.claude/.ceh-advisor-ack`,
3. Re-run the command.

A fresh ack (default TTL 900 s = 15 min, `CEH_ADVISOR_ACK_TTL` to change) unlocks the command; the
ack file doubles as an audit trail of the last verdict. Add project-specific patterns (one
extended regex per line) in `.claude/ceh-advisor-patterns.txt` or point `CEH_ADVISOR_PATTERNS`
elsewhere.

Matching is string-level, not shell-aware — a destructive pattern inside a quoted argument
(`echo "rm -rf is dangerous"`, `grep "TRUNCATE TABLE" docs/`) also triggers a deny. Deliberate:
the backstop fails toward deny, and a false positive costs one consult while a false negative
costs the data.

Note the honest-agent assumption: nothing stops the model from touching the ack without
consulting. The hook is a backstop against *forgetting*, not an adversarial control — same trust
model as the rest of the setup.

**Repeated failures (watch).** Consecutive failed Bash calls are counted per session in `/tmp`. At
the threshold (default 3, `CEH_ADVISOR_FAIL_THRESHOLD`), the hook exits 2 so its stderr is fed
back to Claude: stop iterating, consult the advisor, challenge the diagnosis. Any success resets
the streak. Failure detection is heuristic (checks `is_error` plus common failure strings in the
response) because the PostToolUse payload shape has varied across Claude Code versions — tune the
grep if you see false negatives.

## Handoff

Inline summary in the Task prompt (Situation / Options considered / Leaning toward / Relevant
files). The contract is encoded twice: in the agent's `description` (so the dispatching session
sees it at routing time) and in the agent body (so the advisor *enforces* it — insufficient
handoff gets a "missing: X, Y" response instead of a guessed verdict). If verdicts start missing
context the inline summary can't carry, switch to a decision-log file the main session appends to
and the advisor reads — the agent already has `Read`, so that change is prompt-only.

## Design notes

- **No Stop hook in the default wiring.** A pre-completion gate on `Stop` fires on *every* stop —
  expensive and noisy. If you want it, add to your own `settings.json`:

  ```json
  "Stop": [{ "matcher": "*", "hooks": [{ "type": "prompt", "prompt": "If this session involved an architectural decision, a multi-file change, or anything tagged high-stakes, and ceh-advisor was never consulted, return 'block' with reason 'consult ceh-advisor for a pre-completion audit'. Otherwise return 'approve'." }] }]
  ```

  Try it behind a flag file first (the temporarily-active-hook pattern) before making it
  unconditional.
- **Guard uses deny + ack protocol rather than `ask`.** `ask` routes the decision to the human;
  the whole point is that *the main session consults the advisor*, so the deny message drives the
  consult loop instead.

## Test plan

Run from a project directory (the guard resolves the ack file against `CLAUDE_PROJECT_DIR` or the
current directory). `$PLUGIN` below is this plugin's root — the repo checkout or the installed
cache directory.

```bash
# Guard: destructive command, no ack -> deny JSON
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"},"session_id":"t1"}' \
  | bash "$PLUGIN/scripts/ceh-advisor-guard.sh"

# Guard: benign command -> silent allow (no output, exit 0)
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"},"session_id":"t1"}' \
  | bash "$PLUGIN/scripts/ceh-advisor-guard.sh"

# Guard: fresh ack -> allow with verdict in reason
mkdir -p .claude && echo "Go ahead — branch is already merged upstream." > .claude/.ceh-advisor-ack
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"},"session_id":"t1"}' \
  | bash "$PLUGIN/scripts/ceh-advisor-guard.sh"

# Failure watch: third consecutive failure -> exit 2 + stderr nudge
for i in 1 2 3; do
  echo '{"tool_name":"Bash","tool_input":{"command":"pytest"},"session_id":"t2","tool_response":{"is_error":true}}' \
    | bash "$PLUGIN/scripts/ceh-advisor-failure-watch.sh"; echo "run $i exit: $?"
done
```

Then test live on one real decision, and track the **proportion of proactive vs. explicit-by-name
invocations**. If most consults are explicit, the soft trigger is under-firing and the hook layer
needs widening.

## Metrics to watch

- Rubber-stamp rate: advisor agreeing with the "leaning toward" option >~80% of the time suggests
  the same-lab blind spot is live (the reviewer shares training lineage with the requester).
- Guard false positives: benign commands matching patterns → tighten regexes.
- Failure-watch false negatives: real failures not detected → extend the grep in the watch script.
