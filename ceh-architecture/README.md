# ceh-architecture

Stack-agnostic architectural standards: recording significant decisions (ADRs) and domain modeling
(identifier formats, status enums, state transitions, layer boundaries).

REST API design now lives in `ceh-python-service:fastapi`; PostgreSQL schema design in
`ceh-python-service:postgresql`; directory layout in `ceh-scaffolding`.

## Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `adr` | Making a significant architectural decision that should be recorded |
| `domain-modeling` | Designing entities, identifier formats, status enums, state transitions, or layer boundaries |

## Hooks

This plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-invariants.sh`) that
injects the **architecture invariants** as always-on context. It fires on the `startup`, `clear`,
and `compact` events and activates automatically when the plugin is enabled — no global
`settings.json` change required.

**Why a hook and not just skills:** the load-bearing rules here (prefixed IDs, closed status enums,
immutable identifiers, layer boundaries) are *invariants* — they must hold for every relevant change.
But skill auto-loading is evaluated against the user's prompt at the start of a turn, so a skill that
triggers on an implicit mid-turn decision ("deciding where a file belongs", "defining an entity ID")
reliably under-fires. The hook injects a compact version of these invariants every session so they
always apply; the skills remain the on-demand reference for the full patterns and code. Each line in
the injected block is tagged with the skill (e.g. `[domain-modeling]`) that documents it in depth.
