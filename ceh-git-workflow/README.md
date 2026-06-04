# ceh-git-workflow

Claude Code plugin delivering git workflow standards as skills. Covers trunk-based
branching, Conventional Commits, merge commit policy, PR guidelines, code review conventions,
CI requirements, release tagging, and dependency management.

## Skills

Auto-trigger on context; each loads only the relevant content.

| Skill | Auto-loads when |
|-------|-----------------|
| `branch` | Creating or naming a branch |
| `commit` | Writing or reviewing a commit message |
| `open-pr` | Opening a pull request |
| `hotfix` | Executing a critical production fix |
| `release` | Tagging a release or bumping a version |
| `code-review` | Writing PR review comments |
| `dependency-management` | Adding, removing, or upgrading a dependency |
| `gitignore` | Creating or editing `.gitignore` |

> Documentation agents (`changelog-agent`, `readme-updater`) now live in the `ceh-documentation` plugin.
