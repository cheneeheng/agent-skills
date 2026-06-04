# ceh-agent-coding-contract

Behavioral contract for coding agents. Establishes rules that govern how an agent operates during
a coding session — what it may do, when it must stop, and how it logs decisions.

## Skills

| Skill | Description |
|-------|-------------|
| `agent-coding-contract` | Full behavioral contract — load at session start before any coding task |

### agent-coding-contract

Loads automatically before any implementation, refactoring, or multi-file change. Also invoke
manually:

```
/agent-coding-contract
```

Or when you say:
- `"load the contract"` / `"agent contract"` / `"coding contract"`

## Hooks

This plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-contract.js`) that
injects a mandatory directive to load the `agent-coding-contract` skill before any other action.
It fires on the `startup` and `clear` events and activates automatically when the plugin is
enabled — no global `settings.json` configuration required.

## What the Contract Defines

**Five-step task workflow** (no skipping):
1. Understand — clarify request, affected files, risks
2. Confirm scope — verify authorization
3. Apply changes — minimal, localized edits
4. Validate — only if explicitly requested
5. Summarize — what changed, assumptions, decisions logged

**Core rules:**
- Decide, don't guess silently
- Minimal change bias — no unsolicited refactors
- No implicit actions — never claim work was done without doing it
- Explicit authorization — if unsure, assume not authorized

**Execution mode:** Autonomous. On ambiguity, decide the conservative option, document it, and
continue; stop only for the hard cases in Stop Conditions. The authority hierarchy for resolving
conflicting context files is defined in the `agent-coding-contract` skill.

## Decision Log

Decisions made under ambiguity are appended to `docs/claude_logs/DECISION_LOG.md`.
Format defined in the `agent-coding-contract` skill.
