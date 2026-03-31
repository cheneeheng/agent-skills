# Pull Request Standards

## Size Guidelines

| PR type | Recommended | Max |
|---------|-------------|-----|
| Bug fix | ≤ 200 LOC | 300 LOC |
| New feature | ≤ 400 LOC | 600 LOC |
| Refactor | ≤ 500 LOC | 800 LOC |
| DB migration | Migration file only; split app changes into a separate PR |

If a PR exceeds the guideline, split it by layer (schema change PR → service layer PR → API layer PR). Large PRs without justification will be returned for splitting.

## PR Title

Must follow Conventional Commits format. This becomes the squash commit message.

## PR Description Template

```markdown
## What
<!-- One sentence: what does this change do? -->

## Why
<!-- Why is this change needed? Link to ticket/issue. -->

## How
<!-- Brief explanation of approach if non-obvious. -->

## Testing
<!-- What was tested? What test cases were added? -->

## Checklist
- [ ] All CI checks pass
- [ ] Tests added or updated for new behavior
- [ ] No `any` / `@ts-ignore` / `# type: ignore` introduced
- [ ] No secrets or credentials in code
- [ ] Migrations (if any) are backward-compatible
- [ ] ARCHITECTURE_DECISIONS.md updated (if a durable decision was made)
```

## Author Self-Review Checklist

Before requesting review, the author must:

- [ ] Read the diff top-to-bottom as if seeing it for the first time
- [ ] No commented-out code
- [ ] No debug logs or `console.log` / `print()` left in
- [ ] No `TODO` without a linked ticket
- [ ] Branch is rebased on latest `main`
- [ ] PR description is complete
- [ ] PR is scoped to one concern (if not, split it)

## Required Approvals

- Bug fixes and small features: 1 approval
- New API surfaces, schema changes, security changes: 2 approvals
- Hotfixes: 1 approval minimum (do not bypass CI)
- The author may not approve their own PR
