# Task Workflow

## Five-Step Workflow

Every task follows this order. No skipping.

1. **Understand** — clarify the request, affected files, and potential risks
2. **Confirm scope** — verify authorization; stop if unclear (Interactive Mode)
3. **Apply changes** — minimal, localized edits following project conventions
4. **Validate** — run checks **only if explicitly requested**; when running tests, delegate to a background subagent so the main instance stays unblocked — if a specialized tester agent is available (e.g. `python-unit-tester`, `ts-unit-tester`), it will be triggered automatically; otherwise use `Agent(run_in_background=true)`
5. **Summarize** — what changed, why, any assumptions, any decisions logged

**Hard rule:** Validation, testing, building, formatting, and command execution must not occur unless explicitly requested. This applies in all modes.

## Task Decomposition

For large tasks:
- Break into sequential subtasks
- Track every subtask using the built-in Claude Code task tool (TaskCreate / TaskUpdate)
- Complete and confirm each subtask before proceeding (Interactive Mode)
- Document decomposition decisions in `docs/claude_logs/DECISION_LOG.md` (Autonomous Mode)
- Never silently combine unrelated changes into a single subtask
- When independent subtasks have no ordering dependency or shared state, spawn parallel subagents via the built-in `Agent` tool rather than executing sequentially

## Task Completion Output

End every task with:
- Concise summary of what changed and why
- Any assumptions made (state them, never hide them)
- Decision log entries added (if any)
- Follow-up actions the user should take
