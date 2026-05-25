---
name: "release"
description: "Load this skill when tagging a release or bumping a version: following semantic versioning, committing the version bump, tagging main, and pushing the tag. Auto-load whenever a version is being bumped in pyproject.toml or package.json, a git tag is being created, or a release is being cut."
---

# Release Tagging

Tags follow semver: `v<major>.<minor>.<patch>`. Apply only to commits on `main` after all CI passes.

| Change type | Bump |
|-------------|------|
| Breaking change (`BREAKING CHANGE:` footer or `!` type) | MAJOR |
| New backward-compatible feature | MINOR |
| Fixes, chores, docs, refactors | PATCH |

When in doubt, bump PATCH. Never lower a version.

## Command Sequence

```bash
# 1. Bump version in pyproject.toml and package.json, commit
git add pyproject.toml package.json
git commit -m "chore: bump version to v<X.Y.Z>"

# 2. Tag and push
git tag v<X.Y.Z>
git push origin main
git push origin v<X.Y.Z>
```
