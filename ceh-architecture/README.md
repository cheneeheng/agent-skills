# ceh-architecture-design

Architectural standards for APIs, domain modeling, event sourcing, LLM integration, and
PostgreSQL. Covers structural decisions, layer boundaries, REST conventions, schema design,
and LLM safety rules.

## Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `adr` | Making a significant architectural decision that should be recorded |
| `domain-modeling` | Designing entities, identifier formats, status enums, or state transitions |
| `event-sourcing` | Working with event logs, state snapshots, or event types |
| `llm-integration` | Writing LLM API calls, defining output schemas, or validating LLM responses |
| `postgresql` | Writing SQL, designing schemas, asyncpg queries, or filtering by tenant |
| `repository-structure` | Creating new directories, adding modules, or deciding where code belongs |
| `rest-api` | Designing REST endpoints, choosing HTTP status codes, or shaping error responses |

## Hooks

This plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-invariants.js`) that
injects the **architecture invariants** as always-on context. It fires on the `startup`, `clear`,
and `compact` events and activates automatically when the plugin is enabled — no global
`settings.json` change required.

**Why a hook and not just skills:** the load-bearing rules here (prefixed IDs, closed status enums,
layer boundaries, tenant isolation, append-only event log, LLM validate-before-commit) are
*invariants* — they must hold for every relevant change. But skill auto-loading is evaluated against
the user's prompt at the start of a turn, so a skill that triggers on an implicit mid-turn decision
("deciding where a file belongs", "defining an entity ID") reliably under-fires. The hook injects a
compact version of these invariants every session so they always apply; the skills remain the
on-demand reference for the full patterns and code. Each line in the injected block is tagged with
the skill (e.g. `[domain-modeling]`) that documents it in depth.

