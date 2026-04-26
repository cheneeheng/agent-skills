# ceh-agent-coding-contract

Behavioral contract for coding agents. Establishes rules that govern how an agent operates during
a coding session — what it may do, when it must stop, and how it logs decisions.

## Skill

| Skill | Type | Description |
|-------|------|-------------|
| `agent-coding-contract` | Bundle | Full behavioral contract — load at session start |

Invoke manually:

```
/agent-coding-contract
```

Or load automatically when you say:
- `"proceed autonomously"` / `"autonomous mode"`
- `"don't stop to ask"`
- `"interactive mode"`

## What the Contract Defines

**Two execution modes:**

| Mode | Default | Activation | Ambiguity handling |
|------|---------|------------|--------------------|
| Interactive | Yes | Implicit | Stop and ask |
| Autonomous | No | Explicit phrase | Decide and document |

**Five-step task workflow** (no skipping):
1. Understand — clarify request, affected files, risks
2. Confirm scope — verify authorization
3. Apply changes — minimal, localized edits
4. Validate — only if explicitly requested
5. Summarize — what changed, assumptions, decisions logged

**Core rules:**
- Ask, don't guess
- Minimal change bias — no unsolicited refactors
- No implicit actions — never claim work was done without doing it
- Explicit authorization — if unsure, assume not authorized

## Autonomous Mode Decision Log

When operating in Autonomous Mode, decisions are appended to `docs/claude_logs/DECISION_LOG.md`.
Format defined in `skills/agent-coding-contract/references/decision-log.md`.

## Reference Files

| File | Topic |
|------|-------|
| `references/execution-modes.md` | Interactive vs Autonomous, authority hierarchy |
| `references/core-rules.md` | Agent role, rules, behavioral summary table |
| `references/task-workflow.md` | Five-step workflow, task decomposition |
| `references/stop-conditions.md` | When to stop, partial failures, multi-agent |
| `references/decision-log.md` | Decision log format |
| `references/non-goals.md` | Universal non-goals |
