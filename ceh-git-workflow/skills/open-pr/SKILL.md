---
name: "open-pr"
description: "Load this skill when opening a pull request: writing the PR title, filling in the description template (What/Why/How/Testing/Checklist), checking PR size limits, or running the author self-review checklist. Auto-load whenever a pull request is being created, a PR description is being written, or a branch is being pushed to open a PR."
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
- [ ] DECISIONS.md updated (if a durable decision was made)
- [ ] Attribution included if AI tooling assisted
```

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

**Merge commit only** — preserve every commit on `main`. The full per-PR history is retained
on purpose: it is the source material for write-ups and blog posts.

- Use a true merge commit (`gh pr merge <number> --merge`) — never squash, never rebase-merge
- Every commit must already be Conventional Commits format; nothing collapses them now, so they
  land on `main` as written
- Clean the branch before merging: rebase on `main`, drop fixup/WIP/debug commits so the
  preserved history reads cleanly

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
- [ ] Tests added or updated
- [ ] No `any` / `@ts-ignore` / `# type: ignore` introduced
- [ ] No secrets or credentials in code
- [ ] Migrations (if any) are backward-compatible
- [ ] DECISIONS.md updated (if a durable decision was made)
EOF
)"
```
