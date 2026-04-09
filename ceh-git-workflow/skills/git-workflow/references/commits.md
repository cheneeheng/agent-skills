# Commit Messages — Conventional Commits

```
<type>(<scope>): <short summary>

[optional body — explain why, not what]

[optional footer — breaking changes, issue refs]
```

## Types

| Type | When to use |
|------|-------------|
| `feat` | New feature or behavior |
| `fix` | Bug fix |
| `refactor` | Code change with no behavior change |
| `test` | Adding or changing tests |
| `docs` | Documentation only |
| `chore` | Build, tooling, dependency updates |
| `perf` | Performance improvement |

## Scope

Optional but recommended. Use the module, component, or layer changed:

```
feat(auth): add JWT refresh token rotation
fix(api): handle 429 response from upstream correctly
chore(deps): upgrade fastapi to 0.115.0
```

## Rules

- Subject line: imperative mood, lowercase, no period, ≤ 72 characters
- Body: explain *why*, not *what* — the diff already shows what changed
- Breaking changes: add `BREAKING CHANGE:` footer with migration notes
- Reference issues: `Closes #123` or `Refs #456` in footer

**Good:**
```
feat(orders): add bulk cancel endpoint

Supports cancelling up to 100 orders per request. Single-cancel
endpoint remains unchanged; no migration needed.

Closes #342
```

**Bad:**
```
WIP changes
fixed stuff
update auth
```
