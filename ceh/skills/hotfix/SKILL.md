---
name: "hotfix"
description: >
  Load this skill when executing a critical production fix: branching from main with the
  fix/critical- prefix, keeping the fix minimal in scope, opening a PR with the required
  approval, and tagging a PATCH release after merge. Auto-load whenever a critical bug is
  being fixed directly, a hotfix branch is being created, or a PATCH release is being cut
  after an urgent fix.
---

# Hotfix Workflow

The complete hotfix sequence: branch from main with fix/critical- prefix, commit with minimal
scope, open PR (1 approval minimum, all CI must pass), merge, tag PATCH release, clean up
branch.

Read [../git-workflow/references/workflows.md](../git-workflow/references/workflows.md) (the
Hotfix section) for the command sequence, and
[../git-workflow/references/releases.md](../git-workflow/references/releases.md) for the
tagging rules applied after merge.
