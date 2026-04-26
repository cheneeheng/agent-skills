# Changelog

## [2.1.1] — 2026-04-26

### Added
- `references/migrations.md`: Alembic migration patterns — setup, autogenerate, upgrade/downgrade, test DB management.
- `README.md`: Plugin documentation with skills, agents, scripts, and reference index.

### Fixed
- `agents/python-system-tester.md`: Removed non-standard `effort: high` frontmatter field.
- `references/security.md`: Changed `uv run pip-audit` to `uvx pip-audit` (no install required).

### Changed
- `skills/python-backend/SKILL.md`: Trimmed description; added `migrations.md` to references table.
- `references/coding-style.md`: Removed deprecated `from typing import Optional`; removed "bad" async sync-handler example.

---

## [2.1.0] — 2026-04-25

### Fixed
- `references/exceptions.md`: Removed contradictory rule about route handlers converting domain exceptions to `HTTPException`; global handlers in `app/core/middleware.py` are now the stated pattern.
- `references/coding-style.md`: Replaced deprecated `asyncio.get_event_loop()` with `asyncio.get_running_loop()`.
- `references/testing.md`: Added `system/` directory to test structure tree.
- `run-unit-tests.sh`, `run-integration-tests.sh`, `run-system-tests.sh`: Replaced bare `pytest` with `uv run pytest`.

---

## [2.0.0] — 2026-04-22

Initial release after monolith split into per-domain plugins.
