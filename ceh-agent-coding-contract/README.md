# ceh-agent-coding-contract

A behavioral contract for coding agents: the rules that govern how an agent operates during a
session — what it may change, when it must stop, and how it logs decisions. The plugin loads the
contract automatically at session start.

> The plan-driven workflow skills (`implement-from-plan`, `review-against-plan`) moved to the
> `ceh-plan-build-review` plugin, which bundles them with the planning skills.

## Skills

| Skill | When it loads | What it does |
|-------|---------------|--------------|
| `agent-coding-contract` | Every coding session (auto, via hook) | The full behavioral contract — role, core rules, five-step workflow, stop conditions, decision logging. |

**Manual triggers**

- `agent-coding-contract` — `/agent-coding-contract`, or say `"load the contract"` / `"agent contract"` / `"coding contract"`.

## How the contract auto-loads

The plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-contract.js`) that injects
a mandatory directive to load the `agent-coding-contract` skill before any other action. It
activates automatically when the plugin is enabled — no global `settings.json` change required.

It fires on three events:

- `startup` / `clear` — a fresh or reset session has no contract loaded.
- `compact` — re-injects the contract in case context compaction dropped it.

`resume` is intentionally omitted: a resumed session inherits the contract already loaded before the
resume.

## What the contract enforces

The `agent-coding-contract` skill is the single source of truth. In short, it requires the agent to:

- **Run Autonomous Mode** — on routine ambiguity, decide the conservative option, log it, and
  continue; stop only for the hard cases (unresolvable conflicts, repo state contradicting
  instructions, risk of data loss, inconsistent partial failure).
- **Follow the five-step workflow** — Understand → Confirm scope → Apply changes → Validate →
  Summarize. Validation, testing, and command execution happen only when explicitly requested.
- **Make minimal, authorized changes** — localized diffs, no unsolicited refactors, touch only what
  is in scope, never claim work was done that wasn't.
- **Log decisions made under ambiguity** to `docs/claude_logs/DECISION_LOG.md` (default path;
  override it via your project `CLAUDE.md`). See the skill for the entry format and when to log.

Refer to the skill for the authoritative wording — this section is a summary and is not the contract
itself.
