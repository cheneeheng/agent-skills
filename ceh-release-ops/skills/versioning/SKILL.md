---
name: "versioning"
description: >
  Load this skill when bumping a version, tagging a release, writing a release
  checklist, or classifying a change as patch/minor/major. Auto-load whenever a
  version is being incremented in pyproject.toml or package.json, a git tag is
  being applied, or a change must be classified as internal, user-visible, or
  breaking.
---

# Versioning and Release Checklist

SemVer rules (PATCH/MINOR/MAJOR), the 10-step release checklist (CI passes →
CHANGELOG updated → version bumped in pyproject.toml and package.json → commit →
tag → Docker build → staging smoke tests → production deploy → health check →
metrics baseline), and change classification (breaking changes require an ADR entry
and migration plan before merge).

Read [../release-ops/references/versioning.md](../release-ops/references/versioning.md)
and apply the release process defined there.
