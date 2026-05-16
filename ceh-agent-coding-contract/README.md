# ceh-agent-coding-contract

Behavioral contract for coding agents. Establishes rules that govern how an agent operates during
a coding session — what it may do, when it must stop, and how it logs decisions.

## Skills

| Skill | Description |
|-------|-------------|
| `agent-coding-contract` | Full behavioral contract — load at session start before any coding task |
| `execution-modes` | Interactive vs Autonomous mode — triggered by phrases or `/execution-modes` |

### agent-coding-contract

Loads automatically before any implementation, refactoring, or multi-file change. Also invoke
manually:

```
/agent-coding-contract
```

Or when you say:
- `"load the contract"` / `"agent contract"` / `"coding contract"`

### execution-modes

Triggered by mode-switching phrases or invoked directly:

```
/execution-modes
```

Or when you say:
- `"act autonomously"` / `"proceed autonomously"` / `"autonomous mode"`
- `"don't stop to ask"` / `"just do it"`
- `"interactive mode"`

## What the Contract Defines

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

**Two execution modes** (defined in `execution-modes` skill):

| Mode | Default | Activation | Ambiguity handling |
|------|---------|------------|--------------------|
| Interactive | Yes | Implicit | Stop and ask |
| Autonomous | No | Explicit phrase | Decide and document |

## Autonomous Mode Decision Log

When operating in Autonomous Mode, decisions are appended to `docs/claude_logs/DECISION_LOG.md`.
Format defined in the `agent-coding-contract` skill.
