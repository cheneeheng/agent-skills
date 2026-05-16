# ceh-git-workflow

Claude Code plugin delivering git workflow standards as skills and agents. Covers trunk-based
branching, Conventional Commits, squash merge policy, PR guidelines, code review conventions,
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

## Agents

| Agent | When to use |
|-------|-------------|
| `changelog-agent` | Generate or update `CHANGELOG.md` from git history using semver and Keep a Changelog format |
| `readme-updater` | Keep `README.md` accurate after significant changes (new features, CLI changes, config changes) |


## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check-semver.py` | Validate `CHANGELOG.md` — semver format, date order, no duplicates |

Usage:

```bash
python3 scripts/check-semver.py CHANGELOG.md
```
