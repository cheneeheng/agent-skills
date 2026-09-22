# ceh-git-workflow

Claude Code plugin delivering git workflow standards as skills. Covers trunk-based
branching, Conventional Commits, merge commit policy, PR guidelines, code review conventions,
CI requirements, changelog entries, release tagging, and dependency management — plus two
orchestrated flows that sequence those skills end to end.

## Skills

Auto-trigger on context; each loads only the relevant content.

| Skill | Auto-loads when |
|-------|-----------------|
| `branch` | Creating or naming a branch |
| `commit` | Writing or reviewing a commit message |
| `open-pr` | Opening a pull request; includes the definition-of-done quality gate and queues auto-merge on repos that allow it |
| `merge` | Merging a PR (immediate or auto-merge) or a local branch into `main`, then cleaning up the branch afterward |
| `hotfix` | Executing a critical production fix |
| `release` | Tagging a release or bumping a version |
| `code-review` | Writing PR review comments |
| `dependency-management` | Adding, removing, or upgrading a dependency |
| `update-changelog` | Writing a `CHANGELOG.md` entry — a versioned section, or bullets under `[Unreleased]` |

### Orchestrated flows

Two skills sequence the ones above end to end. They own only the ordering and the gate between
steps; every step is delegated, so nothing is duplicated.

| Skill | Pipeline | Ends at |
|-------|----------|---------|
| `merge-flow` | changelog (Unreleased) → README → commit → PR → merge → cleanup | the merge — no bump, no tag |
| `release-flow` | version bump → changelog → README → CLAUDE.md → commit → PR → merge → tag → release | the published GitHub release |

`merge-flow` starts on the branch you are already on rather than cutting a new one. Pick it for
ordinary work; pick `release-flow` when the same branch should also ship a version.

> README maintenance lives in the `ceh-documentation` plugin — both flows call it conditionally,
> which is why it is not a declared dependency. `update-changelog` lives here instead: every input
> it reads is git (`git describe --tags`, `git log`, `git tag`, `git remote`).
> The former `gitignore` skill was folded into the per-project-type skills in `ceh-scaffolding`.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check-semver.py` | Validate `CHANGELOG.md` — semver format, date order, no duplicates; accepts `-` or `—` date separators (used by `update-changelog`) |

```bash
python3 scripts/check-semver.py CHANGELOG.md
```
