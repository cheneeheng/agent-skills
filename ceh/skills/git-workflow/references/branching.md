# Branching Strategy

Trunk-based development. `main` is always deployable.

- Feature branches are short-lived and scoped to a single task or change
- Direct commits to `main` are blocked — all changes go through a PR
- Branch from `main`. Never branch from another feature branch
- Delete branches after merge

## Branch Naming

```
<type>/<short-description>
```

| Prefix | When to use | Example |
|--------|------------|---------|
| `feat/` | New feature | `feat/session-replay` |
| `fix/` | Bug fix | `fix/token-expiry-edge-case` |
| `chore/` | Maintenance, tooling, dependency updates | `chore/update-dependencies` |
| `docs/` | Documentation only | `docs/add-onboarding-guide` |
| `test/` | Test additions or fixes with no source changes | `test/reasoning-engine-invariants` |
| `refactor/` | Code changes without feature or bug changes | `refactor/extract-auth-middleware` |

Short description: lowercase, hyphen-separated, 3–5 words.
