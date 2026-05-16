---
name: "commit"
description: >
  Load this skill when writing a commit message or staging changes for a commit: choosing the
  correct Conventional Commits type and scope, formatting the subject line, writing a useful
  body, or adding footers for breaking changes and issue references. Auto-load whenever a git
  commit is being made, a commit message is being composed, or staged changes are being reviewed
  before committing.
---

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

## Rules

- Subject line: imperative mood, lowercase, no period, ≤ 72 characters
- Body: explain *why*, not *what* — the diff already shows what changed
- Breaking changes: `BREAKING CHANGE:` footer with migration notes
- Reference issues: `Closes #123` or `Refs #456` in footer
- Include AI tooling attribution in the footer if available

Good example:
```
feat(orders): add bulk cancel endpoint

Supports cancelling up to 100 orders per request. Single-cancel
endpoint remains unchanged; no migration needed.

Closes #342
```

## Commands

```bash
git add <files>
git commit -m "<type>(<scope>): <short summary>"
```

Multi-line (body or footer needed):
```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <short summary>

<body — explain why, not what>

<footer — BREAKING CHANGE or Closes #NNN>
EOF
)"
```
