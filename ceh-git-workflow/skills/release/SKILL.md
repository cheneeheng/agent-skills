---
name: "release"
description: "Load this skill when cutting a release, bumping a version, tagging, or publishing a release: following semantic versioning, committing the version bump, tagging main, pushing the tag, and creating the release. Trigger when the user says \"cut a release\", \"create a release\", \"tag a release\", \"create a tag and a release\", \"bump the version\", \"bump the versions\", \"bump and release\", \"ship a release\", or \"publish a release\". Auto-load whenever a version field changes in any project manifest (e.g. pyproject.toml, package.json, plugin.json, marketplace.json, Cargo.toml, *.csproj, build.gradle), a git tag is being created, or a release is being created."
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

Before bumping the version, **update the changelog** for this release so the new version section and release notes are ready to reference.

```bash
# 1. Bump the version in this project's manifest(s) — whatever the project uses
#    (pyproject.toml, package.json, plugin.json, marketplace.json, Cargo.toml, ...), commit
git add <manifest files>
git commit -m "chore: bump version to v<X.Y.Z>"
git push origin main

# 2. Tag and push. Use an annotated tag (-a -m): some repos enforce it,
#    and `git tag v<X.Y.Z>` then fails with "no tag message".
git tag -a v<X.Y.Z> -m "v<X.Y.Z> — <summary>"
git push origin v<X.Y.Z>

# 3. (Optional) Publish a GitHub release for the tag
gh release create v<X.Y.Z> --title "v<X.Y.Z>" --notes-file <notes file>
```
