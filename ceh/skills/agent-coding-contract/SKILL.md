---
name: "agent-coding-contract"
description: >
  Load this skill at the start of any session where a coding agent is assisting with code changes.
  Defines the rules governing how the agent operates: two execution modes (Interactive default vs
  Autonomous opt-in), what requires explicit user authorization before acting, how to handle
  ambiguity without guessing, how to log decisions made without user input, when to stop vs proceed,
  and the five-step task workflow every task must follow. Use this skill whenever you need to
  establish or reinforce the behavioral contract — especially before autonomous tasks, refactors,
  multi-file changes, or any work where scope boundaries matter. Also load this skill when the user
  says "proceed autonomously", "don't stop to ask", or "interactive mode".
---

# Agent Coding Contract

Behavioral contract for coding agents assisting with code changes. Covers two execution modes
(Interactive default vs Autonomous opt-in), explicit authorization rules, ambiguity resolution,
the five-step task workflow, stop conditions, partial failure handling, and the decision log format
for autonomous decisions.

## References

Load the relevant file for the topic at hand.

| File | Topic |
|------|-------|
| [references/agent-role.md](references/agent-role.md) | What the agent may and must not do |
| [references/execution-modes.md](references/execution-modes.md) | Interactive vs Autonomous modes, authority hierarchy when context files conflict |
| [references/task-workflow.md](references/task-workflow.md) | Five-step workflow, task decomposition, task completion output |
| [references/core-rules.md](references/core-rules.md) | Core rules and behavioral summary table |
| [references/stop-conditions.md](references/stop-conditions.md) | When to stop, partial failure handling, multi-agent scenarios |
| [references/decision-log.md](references/decision-log.md) | Decision log entry format for Autonomous Mode |
| [references/non-goals.md](references/non-goals.md) | Universal non-goals — what never to do unless explicitly asked |
