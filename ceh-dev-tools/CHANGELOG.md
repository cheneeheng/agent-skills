# Changelog — ceh-dev-tools

---

## [1.0.1] — 2026-04-26

### Fixed

- `repo-tree-mapper`: trimmed agent description (~50% shorter); reduced `maxTurns` from 25 to 8.
- `walk-repo.sh`: replaced non-portable `$skip && continue` with `[[ $skip == true ]] && continue`.

### Changed

- `README.md`: expanded with invoke syntax, output example, and install instructions.

---

## [1.0.0] — 2026-04-25

### Added

- `repo-tree-mapper` agent: walks a repository and produces an annotated, clickable `REPO_MAP.md`.
- `walk-repo.sh` script: git-aware directory walker used by the agent.
- `README.md`.
