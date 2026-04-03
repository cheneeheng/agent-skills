---
name: "merge"
description: >
  Load this skill when merging branches or deciding on a merge strategy: applying the squash
  merge policy, understanding why merge commits are disallowed on main, or knowing when rebase
  vs force-push is acceptable. Auto-load whenever a pull request is being merged, a merge
  strategy is being chosen, or a rebase operation is being performed.
---

# Merging

Squash merge policy (one commit per PR on main), why merge commits are disallowed, when local
rebase is fine, and force-push rules (feature branches only, never main).

Read [../git-workflow/references/merging.md](../git-workflow/references/merging.md) and apply
the merge strategy defined there.
