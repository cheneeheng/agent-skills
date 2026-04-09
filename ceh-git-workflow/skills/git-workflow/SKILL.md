---
name: "git-workflow"
description: >
  Use this skill whenever you're doing anything git-related: writing or reviewing commit messages,
  naming branches, opening or reviewing pull requests, setting up CI checks, or adding and updating
  dependencies. Apply it even when the user doesn't explicitly ask for standards guidance — use it
  to ensure Conventional Commits format, correct branch naming, proper PR structure, and CI
  requirements are followed. Covers trunk-based branching, squash merge policy, PR size guidelines,
  code review comment conventions (blocking vs advisory), branch protection rules, release tagging,
  and dependency evaluation criteria. Use regardless of language or framework.
---

# Git Workflow

Standards for version control and team collaboration. Covers trunk-based branching, Conventional
Commits, squash merge policy, pull request guidelines, code review conventions, CI requirements,
release tagging, and dependency management.

## References

When asked to **perform** a git operation, start with
[references/workflows.md](references/workflows.md) for the command sequence, then load
the standards file for that topic to apply the correct conventions.

When asked about **standards or conventions** only, load the relevant file directly.

| File | Topic |
|------|-------|
| [references/workflows.md](references/workflows.md) | Command sequences: branch, commit, PR, merge, hotfix, release |
| [references/branching.md](references/branching.md) | Branch strategy, naming conventions |
| [references/commits.md](references/commits.md) | Conventional Commits format, types, rules, examples |
| [references/merging.md](references/merging.md) | Squash merge policy, rebase rules |
| [references/pull-requests.md](references/pull-requests.md) | PR size limits, title, description template, self-review, approvals |
| [references/code-review.md](references/code-review.md) | `[blocking]`/`[advisory]`/`[question]` conventions, review priority order |
| [references/ci.md](references/ci.md) | Required checks for Python and TypeScript, branch protection rules |
| [references/releases.md](references/releases.md) | Semantic version tagging |
| [references/dependencies.md](references/dependencies.md) | Evaluation criteria, pinning policy, security audits, major upgrades |
| [references/gitignore.md](references/gitignore.md) | Required `.gitignore` entries |
