---
name: "open-pr"
description: "Load when creating or opening a pull request, any phrasing — create/open/raise/make/submit/send a PR, pull request, or merge request, or pushing a branch for review. Handles the PR-creation half of compound requests like 'create a PR, merge it, delete the branch' (merge/cleanup is the merge skill). Covers the PR title, the What/Why/How/Testing/Checklist template, size limits, and the author self-review checklist."
---

# Opening a Pull Request

## Size Guidelines

| PR type | Recommended | Max |
|---------|-------------|-----|
| Bug fix | ≤ 200 LOC | 300 LOC |
| New feature | ≤ 400 LOC | 600 LOC |
| Refactor | ≤ 500 LOC | 800 LOC |
| DB migration | Migration file only; split app changes into a separate PR |

If a PR exceeds the guideline, split it by layer (schema → service → API).

## PR Title

Must follow Conventional Commits format. It titles the PR and seeds the merge commit subject.

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
- [ ] docs/adr/DECISIONS.md updated (if a durable decision was made)
- [ ] Attribution included if AI tooling assisted
```

## Definition of Done

Before opening the PR, verify the change meets the bar for its type.

**Bug Fix**
- [ ] Root cause identified and documented in the PR description
- [ ] Failing test added that reproduces the bug
- [ ] Fix applied — the failing test now passes
- [ ] No regressions — full test suite passes
- [ ] Lint and type checks pass

**Feature**
- [ ] Unit tests for new business logic
- [ ] Integration tests for new API surface
- [ ] Lint and type checks pass
- [ ] PR description explains the feature and how it was tested
- [ ] No `any`, `@ts-ignore`, or `# type: ignore` introduced

**Refactor**
- [ ] No behavioral change — proven by existing tests passing unchanged
- [ ] Coverage unchanged (no tests deleted to make the refactor pass)
- [ ] Lint and type checks pass
- [ ] PR description explains what structural problem was addressed

### Coverage Targets

| Area | Minimum |
|------|---------|
| Python application package | 80% |
| Core business logic / domain services | 95% |
| TypeScript `src/lib/` | 70% |

`mypy --strict` and `tsc --noEmit` must pass with zero errors. Do not reduce strictness to meet coverage targets — fix the types.

## Author Self-Review

- [ ] Read full diff (`git diff main...HEAD`) before requesting review
- [ ] No commented-out code or debug logs
- [ ] No `TODO` without a linked ticket
- [ ] Branch is rebased on latest `main`
- [ ] PR is scoped to one concern

## Required Approvals

- Bug fixes and small features: 1 approval
- New API surfaces, schema changes, security changes: 2 approvals
- Hotfixes: 1 approval minimum (do not bypass CI)

## Merge Strategy

**Merge commit only** — never squash, never rebase-merge; every commit lands on `main` as written.
Because commits are not collapsed at merge time, keep them Conventional Commits format and clean the
branch as you go. Full merge mechanics and post-merge cleanup live in the `merge` skill.

## Command

```bash
git push -u origin <branch-name>
gh pr create \
  --title "<type>(<scope>): <short summary>" \
  --body "$(cat <<'EOF'
## What
## Why
## How
## Testing
## Checklist
- [ ] All CI checks pass
- [ ] Tests added or updated for new behavior
- [ ] No `any` / `@ts-ignore` / `# type: ignore` introduced
- [ ] No secrets or credentials in code
- [ ] Migrations (if any) are backward-compatible
- [ ] docs/adr/DECISIONS.md updated (if a durable decision was made)
- [ ] Attribution included if AI tooling assisted
EOF
)"
```
