# ceh-documentation

Claude Code plugin for writing end-user and operator-facing documentation — task-oriented guides that let a reader achieve a goal without already knowing the system.

## Skills

| Skill | Description |
|-------|-------------|
| `user-operator-guide` | Write or revise user guides and operator runbooks — distinguishes the two audiences, picks the right document type, and enforces task-oriented, verifiable procedures |

Invoke manually:

```
/ceh-documentation:user-operator-guide
```

**user-operator-guide** loads automatically when you say:
- `"write a user guide"` / `"write a user manual"`
- `"write an operator guide"` / `"write an ops runbook"`
- `"getting-started guide"` / `"installation guide"`
- `"document how to use this"` / `"document how to operate this"`
- `"admin manual"` / `"configuration guide"`

## What It Produces

Markdown written under `docs/guide/` — a single `index.md` for a focused guide, or a cross-linked tree rooted there with `index.md` as the entry point for a full manual or runbook:
- Audience-correct voice (friendly for users, terse and precise for operators)
- Task-oriented structure — organized by what the reader is trying to do, not by feature
- Numbered procedures where every step has a verifiable result
- Prerequisites and warnings before the steps that need them
- An **Open items** list of anything assumed or left unverified — never invented detail

## Document Types Supported

| Type | Reader's goal |
|------|---------------|
| Getting Started | Go from zero to first success |
| How-To Guide | Accomplish one specific task |
| User Manual | Reference for the whole product |
| Operator Runbook | Operate and recover a system |
| Installation / Config Guide | Stand the system up correctly |
| Troubleshooting Reference | Diagnose and fix a known failure |

## Agents

| Agent | When to use |
|-------|-------------|
| `changelog-agent` | Generate or update `CHANGELOG.md` from git history using semver and Keep a Changelog format |
| `readme-updater` | Keep `README.md` accurate after significant changes (new features, CLI changes, config changes) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check-semver.py` | Validate `CHANGELOG.md` — semver format, date order, no duplicates (used by `changelog-agent`) |

Usage:

```bash
python3 scripts/check-semver.py CHANGELOG.md
```
