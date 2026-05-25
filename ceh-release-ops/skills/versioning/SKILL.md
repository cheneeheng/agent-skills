---
name: "versioning"
description: "Phase: release. Load this skill when bumping a version, tagging a release, writing a release checklist, or classifying a change as patch/minor/major. Auto-load whenever a version is being incremented in pyproject.toml or package.json, a git tag is being applied, or a change must be classified as internal, user-visible, or breaking."
---

# Versioning and Release Checklist

## Semantic Versioning

| Increment | When |
|-----------|------|
| `PATCH` | Bug fixes; no API or schema changes |
| `MINOR` | New features; backward-compatible |
| `MAJOR` | Breaking API or schema changes; requires migration guide |

Version is recorded in both `pyproject.toml` and `package.json`. Both must be updated in the same commit before tagging.

## Release Checklist

Complete every step in order. No skipping.

1. All CI checks pass on `main`
2. `CHANGELOG.md` updated with changes since last release
3. Version bumped in `pyproject.toml` and `package.json`
4. Commit: `chore: bump version to v<X.Y.Z>`
5. Tag: `git tag v<X.Y.Z>` and push tag
6. Docker images built and tagged with version
7. Deploy to **staging** → run smoke tests
8. Staging smoke tests pass → deploy to **production**
9. Verify `GET /health` returns `200` post-deploy
10. Confirm error rate and latency metrics are at baseline within 5 minutes

**Staging must pass before production. Non-negotiable.**

## Change Classification

| Class | Definition | Additional requirement |
|-------|-----------|----------------------|
| Internal | No user-visible or API change | None |
| User-visible | UI change, new feature, behavioral change | PR description required |
| Breaking | API contract change, schema migration, removed endpoint | ADR entry + migration plan before merge |
