# ceh-python-library

Python engineering standards for distributable libraries — packaging, public API discipline, and
semantic versioning on the uv + ruff + mypy + pytest foundation. No web-service dependencies.

Load this plugin for library/SDK projects; use `ceh-python-service` for FastAPI web services.

## Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `python-environment` | Editing pyproject.toml, uv commands, type hints, or ruff/mypy config |
| `python-testing` | Creating or modifying test files, fixtures, or mocks |
| `packaging` | Configuring the build backend, src layout, building wheels, or publishing to PyPI |
| `public-api` | Editing `__init__.py`/`__all__`, changing a public signature, or classifying a semver bump |

## Shared Standards

`python-environment` and `python-testing` are duplicated from `ceh-python-service` per the
repo's [Shared-Standards Duplication Policy](../CLAUDE.md). The library copies drop web-service
dependencies (`fastapi`, `uvicorn`, `asyncpg`) and the uvicorn dev-server command. See
`CROSS_REFERENCES.md` — edit both copies in the same session.
