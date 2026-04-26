# ceh-git-workflow

Claude Code plugin delivering git workflow standards as skills and agents. Covers trunk-based
branching, Conventional Commits, squash merge policy, PR guidelines, code review conventions,
CI requirements, release tagging, and dependency management.

## Skills

### Bundle Skill

| Skill | Description |
|-------|-------------|
| `git-workflow` | Full git workflow reference — loads all topics below |

Load `git-workflow` when you need the full picture. It routes to the correct reference file
based on what you're doing.

### Micro-Skills

Auto-trigger on context; each loads only the relevant reference file(s).

| Skill | Auto-loads when |
|-------|-----------------|
| `branch` | Creating or naming a branch |
| `commit` | Writing or reviewing a commit message |
| `open-pr` | Opening a pull request |
| `merge` | Merging or choosing a merge strategy |
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

## Reference Files

All standards live in `skills/git-workflow/references/`. Micro-skills point into this directory.

| File | Topic |
|------|-------|
| `branching.md` | Trunk-based strategy, branch prefix table, naming rules |
| `commits.md` | Conventional Commits format, type table, rules, examples |
| `merging.md` | Squash merge policy, rebase rules, force-push constraints |
| `pull-requests.md` | PR size limits, description template, author self-review, approval requirements |
| `code-review.md` | `[blocking]`/`[advisory]`/`[question]` conventions, review priority order |
| `ci.md` | Required checks for Python and TypeScript backends, branch protection rules |
| `releases.md` | Semantic versioning rules, MAJOR/MINOR/PATCH triggers |
| `dependencies.md` | Evaluation criteria, pinning policy, security audits, major upgrade process |
| `gitignore.md` | Required `.gitignore` entries for Python/TypeScript projects |
| `workflows.md` | Step-by-step Bash command sequences for every common operation |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check-semver.py` | Validate `CHANGELOG.md` — semver format, date order, no duplicates |

Usage:

```bash
python3 scripts/check-semver.py CHANGELOG.md
```

Exits 0 on valid, 1 on errors.
