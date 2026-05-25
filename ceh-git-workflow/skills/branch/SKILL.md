---
name: "branch"
description: "Load this skill when creating or naming a branch: choosing the correct prefix (feat/, fix/, chore/, docs/, test/, refactor/), formatting the short description, or starting new work from main. Auto-load whenever a new git branch is being created, a branch name is being chosen, or work is being started from the main branch."
---

# Branching

Trunk-based development. `main` is always deployable. Branch from `main` only — never from
another feature branch. Delete branches after merge.

## Branch Naming

```
<type>/<short-description>
```

| Prefix | When to use | Example |
|--------|------------|---------|
| `feat/` | New feature | `feat/session-replay` |
| `fix/` | Bug fix | `fix/token-expiry-edge-case` |
| `chore/` | Maintenance, tooling, dependency updates | `chore/update-dependencies` |
| `docs/` | Documentation only | `docs/add-onboarding-guide` |
| `test/` | Test additions or fixes with no source changes | `test/reasoning-engine-invariants` |
| `refactor/` | Code changes without feature or bug changes | `refactor/extract-auth-middleware` |

Short description: lowercase, hyphen-separated, 3–5 words.

## Rebase and Force-push

- Rebase is fine locally during development
- Force-push is allowed only on your own feature branch (never on `main`)

## Start new work

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-description>
```
