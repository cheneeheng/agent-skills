---
name: usage-limit-handoff
description: >
  Stop-and-summarize protocol for when the 5-hour usage limit is nearly exhausted. Load
  immediately when a hook or system message reports that 5-hour usage crossed the wrap-up
  threshold ("ceh usage-limit guard"), and whenever the user says "usage limit handoff",
  "wrap up the session", "we're near the usage limit", "stop and summarize", or "hand off
  before the limit". Defines how to stop cleanly: finish only the current atomic step, start
  nothing new, report completed vs open work with resume instructions, and end the turn.
  Not for ordinary end-of-task summaries (the contract's Summarize step covers those) or
  general session summaries without a limit trigger.
---

# Usage Limit Handoff

The 5-hour usage window is nearly exhausted. The goal is no longer finishing the task — it is
stopping at a clean boundary so the work can resume without archaeology. A hard limit cut-off
mid-edit loses more than the remaining budget can save.

## Protocol

Execute these steps in order, then end the turn.

1. **Close the current atomic step — start nothing new.** Complete the single edit, command, or
   file write in flight so nothing is half-applied; if it cannot be completed within a few tool
   calls, revert it instead and record it as open. Do not begin the next subtask, launch
   subagents or background tasks, or run validation that was not already in flight.
2. **Secure unsaved state.** If uncommitted changes exist and committing was already authorized,
   commit them; otherwise leave the working tree as-is and describe its state in the report.
   Never commit or stash unprompted just because the session is ending.
3. **Write the handoff report** (format below) as the final message of the turn.
4. **End the turn.** Do not resume work in this session unless the user explicitly says to
   continue — they may prefer to wait for the window reset reported by the guard message.

## Handoff report format

```markdown
## Usage-limit handoff (5h window at N%, resets at HH:MM)

**Done** — completed and in what state (validated / not validated):
- <item — files touched, what was verified>

**In flight** — the step that was closed or reverted at the cut:
- <state of the working tree, anything half-planned>

**Open** — remaining work, ordered; first item is the next actionable step:
1. <next concrete step, specific enough to execute cold>
2. <...>

**Decisions pending** — forks the user still has to resolve, if any.

**Resume with:** <one line: branch name, command to run, or file to open first>
```

Keep it factual and specific: file paths, branch names, exact commands. The reader is a future
session with none of this context.

## Notes

- The trigger is the `usage-limit-watch.py` PostToolUse hook in this plugin. It fires at
  `CEH_USAGE_LIMIT_THRESHOLD` (default 95%) and re-fires every 5 points above it — a repeat
  warning means the first one was ignored; stop immediately.
- If the guard fires while mid-handoff, ignore it: the protocol is already running.
