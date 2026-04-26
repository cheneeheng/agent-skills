# Tagging and Releases

Tags follow semantic versioning: `v<major>.<minor>.<patch>`. Apply only to commits on `main` that have passed all CI checks.

## Version Bump Rules

| Change type | Bump | Trigger |
|-------------|------|---------|
| Breaking change | MAJOR (X.0.0) | Removed API, incompatible behavior, `BREAKING CHANGE:` footer or `!` type |
| New backward-compatible feature | MINOR (x.Y.0) | `feat:` commits, new endpoints/options |
| Fixes, chores, docs, refactors | PATCH (x.y.Z) | `fix:`, `chore:`, `docs:`, `refactor:`, `perf:` |

When in doubt, bump PATCH. Never lower a version.

For commands, see [workflows.md](workflows.md) → *Tag a release*.
