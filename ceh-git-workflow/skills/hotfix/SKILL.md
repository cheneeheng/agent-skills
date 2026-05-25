---
name: "hotfix"
description: "Load this skill when executing a critical production fix: branching from main with the fix/critical- prefix, keeping the fix minimal in scope, opening a PR with the required approval, and tagging a PATCH release after merge. Auto-load whenever a critical bug is being fixed directly, a hotfix branch is being created, or a PATCH release is being cut after an urgent fix."
---

# Hotfix Workflow

For P1/P2 production issues that cannot wait for the next normal release.

1. **Branch:** `fix/critical-<description>` from `main`
2. **Scope:** Minimal fix only — no unrelated changes
3. **Review:** 1 approval minimum, fast-tracked
4. **CI:** All checks must pass — do **not** skip CI under pressure
5. **Merge:** Squash merge to `main`
6. **Tag:** Bump PATCH version, apply tag
7. **Deploy:** Staging → production (abbreviated but both still required)

## Commands

```bash
git checkout main && git pull origin main
git checkout -b fix/critical-<description>

# Fix and commit (minimal scope only)
git add <files>
git commit -m "fix(<scope>): <description>"

# Push and open PR (1 approval minimum, all CI must pass)
git push -u origin fix/critical-<description>
gh pr create --title "fix(<scope>): <description>"

# After merge — bump PATCH version, tag, clean up
git checkout main && git pull origin main
git tag v<X.Y.Z>
git push origin v<X.Y.Z>
git branch -d fix/critical-<description>
git push origin --delete fix/critical-<description>
```
