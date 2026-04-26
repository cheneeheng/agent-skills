---
name: "agent-coding-contract"
description: >
  Load at the start of any coding-agent session. Defines the behavioral contract: Interactive
  (default) vs Autonomous mode, explicit authorization rules, ambiguity handling, five-step task
  workflow, stop conditions, and decision logging. Trigger when user says "proceed autonomously",
  "don't stop to ask", "interactive mode", or before refactors, multi-file changes, or any work
  where scope boundaries matter.
---

# Agent Coding Contract

Behavioral contract for coding agents. Load all reference files at session start — this contract
applies in full, not selectively.

## References

| File | Topic |
|------|-------|
| [references/execution-modes.md](references/execution-modes.md) | Interactive vs Autonomous modes, authority hierarchy |
| [references/core-rules.md](references/core-rules.md) | Agent role, core rules, behavioral summary table |
| [references/task-workflow.md](references/task-workflow.md) | Five-step workflow, task decomposition, completion output |
| [references/stop-conditions.md](references/stop-conditions.md) | Stop conditions, partial failures, multi-agent scenarios |
| [references/decision-log.md](references/decision-log.md) | Decision log entry format for Autonomous Mode |
| [references/non-goals.md](references/non-goals.md) | Universal non-goals — what never to do unless explicitly asked |
