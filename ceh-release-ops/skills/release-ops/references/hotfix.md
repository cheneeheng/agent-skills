# Hotfix Process

For P1/P2 production issues that cannot wait for the next normal release:

1. **Branch:** `fix/critical-<description>` from `main`
2. **Scope:** Minimal fix only — no unrelated changes
3. **Review:** 1 approval minimum, fast-tracked
4. **CI:** All checks must pass — do **not** skip CI under pressure. A broken hotfix is worse than a delayed one.
5. **Merge:** Squash merge to `main`
6. **Tag:** Bump PATCH version, apply tag
7. **Deploy:** Staging → production (abbreviated but both still required)
