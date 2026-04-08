---
name: "release"
description: >
  Load this skill when tagging a release or bumping a version: following semantic versioning,
  committing the version bump, tagging main, and pushing the tag. Auto-load whenever a version
  is being bumped in pyproject.toml or package.json, a git tag is being created, or a release
  is being cut.
---

# Release Tagging

Semantic versioning rules (vX.Y.Z), the version bump + tag + push command sequence, and the
constraint that tags must only be applied to commits that have passed all CI checks.

Read [../git-workflow/references/releases.md](../git-workflow/references/releases.md) for
tagging rules, and
[../git-workflow/references/workflows.md](../git-workflow/references/workflows.md) for the
release command sequence.
