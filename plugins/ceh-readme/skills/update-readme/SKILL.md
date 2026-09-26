---
name: update-readme
description: >-
  Load this skill when keeping README.md accurate after a significant change — shipping a new
  feature, adding a command/script/endpoint, changing install or setup steps, adding or removing
  dependencies, introducing environment variables, or changing the public API surface. Trigger on
  "update the readme", "refresh the docs", "document this feature", "I just shipped X — update
  docs". Not for bug fixes, refactors, or any change that does not affect how someone installs,
  runs, or configures the project; not for changelogs (use update-changelog).
compatibility: >-
  Requires the git CLI on PATH and a git working tree, to read what changed via `git diff` and
  `git status`. Nothing else is needed - the output is Markdown.
---

# Update README

Keep the project's README.md accurate after a significant change. Prefer surgical edits over rewrites. Do nothing when nothing material changed.

## Significance Gate

Before touching the README, confirm AT LEAST ONE applies:

- New user-facing feature, command, flag, or endpoint
- Installation, build, or run instructions changed
- Dependencies, runtime versions, or environment variables changed
- Configuration file format or required config keys changed
- Project structure changed in a way a new contributor needs to know
- Public API (exported functions, CLI surface, HTTP routes) changed
- Project purpose, name, or scope changed

If none apply, respond with:

```
No README update needed — change is internal/minor.
```

and stop.

## Discovery

1. Find README: check `README.md` at root, then `readme.md`, `README.rst`, `docs/README.md`. If none exists and the change is significant, create `README.md` at root.
2. Understand what changed: `git diff HEAD~1 HEAD` or `git status` + `git diff`. Look at changed files, new top-level files, changes to the project's dependency/build manifest (e.g. `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.csproj`), new CLI args, route definitions, `.env.example`.
3. Read the current README fully before editing.

## Editing Principles

- **Surgical edits.** Update only sections affected by the change.
- **Match existing voice.** Preserve tone, heading style, formatting conventions.
- **Update in place.** No "Recent changes" section — that's CHANGELOG.md.
- **No speculation.** Only document what you can verify from the code.
- **Keep examples runnable.** Flags, args, and paths must match current code.
- **Update table of contents** if one exists and you added/removed a section.

## Sections to Check

Only update sections the diff touches:

- Title/tagline (scope changed)
- Features/What it does (new capability)
- Installation (deps or steps changed)
- Quick start/Usage (entry command or basic flow changed)
- Configuration (env vars or config keys changed)
- API reference/Commands (public surface changed)
- Project structure (top-level layout changed)
- Requirements/Prerequisites (runtime version or system deps changed)

Do NOT touch: license, contributing guidelines, acknowledgments, badges — unless the change specifically requires it.

## Constraints

- Never delete existing content unless it's factually wrong.
- Never add marketing language or emojis.
- Never rewrite the whole README when a few edits suffice.
- Never commit or push.
- In a monorepo, update only the READMEs affected by the change.
