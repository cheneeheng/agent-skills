# Decision Log

### Entry 1

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-29
**Task:** Run the ceh-release-flow:release-flow skill in this repo to release the auto-merge git-workflow changes.

**Context:** The release-flow skill prescribes cutting a `chore/release-vX.Y.Z` branch from `main`, but the session's standing instruction is to develop only on `claude/git-auto-merge-workflow-ne8we4` and never push to a different branch without explicit permission. The feature changes and plugin version bumps already live on that feature branch.
**Decision:** Treat the existing `claude/git-auto-merge-workflow-ne8we4` branch as the release-carrying branch rather than creating a separate `chore/release-` branch. This honors the dev-branch constraint and keeps the version bumps, changelog, and feature changes in one PR. Repo git tag bumped PATCH (v3.13.3 → v3.13.4) because the changes are skill-content only (no new skills or agents), per the repo's two-layer versioning rule in CLAUDE.md.
**Impact / Risk:** PR carries both feature and release-bump commits together (acceptable for this repo). GitHub Release object cannot be created with the available MCP tools (no create-release tool) — the annotated tag can be pushed via git, but the Release page must be created manually or confirmed separately.
**Outcome:** Pending merge + tag.
