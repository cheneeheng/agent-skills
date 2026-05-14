---
name: "branch"
description: >
  Load this skill when creating or naming a branch: choosing the correct prefix (feat/, fix/,
  chore/, docs/, test/, refactor/), formatting the short description, or starting new work from
  main. Auto-load whenever a new git branch is being created, a branch name is being chosen, or
  work is being started from the main branch.
---

# Branching

Trunk-based development. `main` is always deployable. Branch from `main` only — never from
another feature branch. Delete branches after merge.

Read [../git-workflow/references/branching.md](../git-workflow/references/branching.md) for
naming conventions (`<type>/<short-description>`).

## Start new work

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-description>
```
