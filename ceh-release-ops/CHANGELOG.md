# Changelog — ceh-release-ops

---

## [2.1.1] — 2026-04-26

### Fixed

- `skills/definition-of-done/SKILL.md`: corrected domain services coverage target from 90% → 95% to match reference file.
- `skills/python-backend/references/observability.md`: synced stub with source — added log level table and Correlation IDs section that were missing.

### Changed

- `skills/release-ops/references/observability.md`: removed redundant bad-example block; rule already stated in opening sentence.
- Added `README.md` with bundle skills, micro-skills, agents, scripts, and reference index.

---

## [2.1.0] — 2026-04-25

### Added

- `agents/github-actions.md`: GitHub Actions specialist agent with detect/scaffold/validate/debug workflow and supply-chain security principles.
- `agents/gitlab-ci.md`: GitLab CI specialist agent with equivalent workflow for `.gitlab-ci.yml`.
- Scripts for both agents: `gh-detect-stack.sh`, `gh-scaffold.sh`, `gh-validate.sh`, `gh-analyze-failure.sh`, `gl-detect-stack.sh`, `gl-scaffold.sh`, `gl-validate.sh`, `gl-analyze-failure.sh`.
- `skills/release-ops/references/definition-of-done.md` and `skills/definition-of-done/SKILL.md` micro-skill.
- `skills/release-ops/references/observability.md` and `skills/observability/SKILL.md` micro-skill.
- Cross-bundle stubs: `skills/python-backend/references/observability.md` and `skills/python-backend/references/security.md`.

---

## [2.0.0] — 2026-04-20

### Added

- Initial plugin split from `ceh` monolith.
- Bundle skill `release-ops` with references: `versioning.md`, `migrations.md`, `rollback.md`, `hotfix.md`, `incidents.md`, `security.md`.
- Micro-skills: `versioning`, `database-migrations`, `rollback`, `incidents`, `security`.
