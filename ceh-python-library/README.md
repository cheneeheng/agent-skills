# ceh-python-library

Python engineering standards for distributable libraries — packaging, public API discipline, and
semantic versioning on the uv + ruff + mypy + pytest foundation. No web-service dependencies.

Load this plugin for library/SDK projects; use `ceh-python-service` for FastAPI web services.

## Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `python-library-environment` | Editing pyproject.toml, uv commands, type hints, or ruff/mypy config |
| `python-library-testing` | Creating or modifying test files, fixtures, or mocks |
| `packaging` | Configuring the build backend, src layout, building wheels, or publishing to PyPI |
| `public-api` | Editing `__init__.py`/`__all__`, changing a public signature, or classifying a semver bump |

## Hooks

This plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-invariants.sh`) that
injects the **Python library invariants** as always-on context. It fires on the `startup`, `clear`,
and `compact` events and activates automatically when the plugin is enabled.

**Why a hook and not just skills:** the load-bearing rules here (type hints, no `Any`/`# type:
ignore` without comment, docstrings on public symbols, a minimal dependency set) are *invariants* —
they must hold on every relevant change. But skill auto-loading is evaluated against the user's
prompt at the start of a turn, so the style half of `python-library-environment` reliably under-fires —
nothing in "add a parser function" signals "watch the type hints and dependency footprint." The
action skills (`packaging`, `public-api`, `python-library-testing`) trigger fine and stay on-demand. The
hook injects a compact version of the invariants every session so they always apply; each rule is
tagged with the skill (e.g. `[python-library-environment]`) that documents it in depth, loadable as
`ceh-python-library:<name>`.

## Shared Standards

`python-library-environment` and `python-library-testing` are duplicated from `ceh-python-service`
(`python-service-environment` / `python-service-testing`) per the repo's
[Shared-Standards Duplication Policy](../CLAUDE.md). The library copies drop web-service
dependencies (`fastapi`, `uvicorn`, `asyncpg`) and the uvicorn dev-server command. See
`CROSS_REFERENCES.md` — edit both copies in the same session.
