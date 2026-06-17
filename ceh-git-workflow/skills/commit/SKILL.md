---
name: "commit"
description: "Load this skill when writing a commit message or staging changes for a commit: choosing the correct Conventional Commits type and scope, formatting the subject line, writing a useful body, or adding footers for breaking changes and issue references. Auto-load whenever a git commit is being made, a commit message is being composed, or staged changes are being reviewed before committing."
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
| `perf` | Performance improvement |
| `test` | Adding or changing tests |
| `docs` | Documentation only |
| `style` | Formatting only — whitespace, semicolons; no code change |
| `build` | Build system, packaging, or external dependencies |
| `ci` | CI/CD configuration and pipelines |
| `chore` | Maintenance, tooling; anything not covered above |
| `revert` | Reverts a previous commit (body: `Reverts <sha>`) |

## Scope

The optional `(<scope>)` names the area of the codebase touched — a module, package, or
component (`auth`, `orders`, `api`). Pick the narrowest noun that covers the change. Omit the
parentheses entirely for repo-wide changes (`chore: bump all dev dependencies`). Keep it
lowercase and consistent with scopes already used in the log (`git log --oneline`).

## Rules

- One logical change per commit. Don't mix a refactor with a feature, or two unrelated fixes —
  split them so each can be reviewed and reverted on its own.
- Subject line: imperative mood ("add", not "added"/"adds"), lowercase, no trailing period,
  ≤ 72 characters.
- Body: explain *why*, not *what* — the diff already shows what changed. Wrap at 72 columns.
  Use `-` bullets for multiple points. Separate it from the subject with one blank line.
- Breaking changes: `BREAKING CHANGE:` footer with migration notes (or a `!` after the
  type/scope: `feat(api)!: ...`).
- Reference issues: `Closes #123` (auto-closes on merge) or `Refs #456` (links only) in footer.
- Attribution: when AI tooling assisted, add a footer line, e.g.
  `Generated with [Claude Code](https://claude.com/claude-code)`.

### Subject: bad vs. good

```
bad:  fixed bug                          # not imperative, no type/scope, vague
bad:  fix(orders): Fixed the bug where.. # capitalized, past tense, trailing detail
good: fix(orders): reject cancel on shipped orders
```

Full example (subject + body + footers):
```
feat(orders): add bulk cancel endpoint

Supports cancelling up to 100 orders per request. Single-cancel
endpoint remains unchanged; no migration needed.

Closes #342
Co-authored-by: Jane Doe <jane@example.com>
Generated with [Claude Code](https://claude.com/claude-code)
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
