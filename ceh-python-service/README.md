# ceh-python-service

Python web-service engineering standards for the FastAPI + uv + asyncpg + PostgreSQL stack.

For distributable libraries (packaging, public API, semver, no web deps) use `ceh-python-library`.

## Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `fastapi` | Writing route handlers, dependencies, lifespan, exception handlers, or REST API design |
| `asyncpg` | Writing database queries, transactions, tenant isolation, or connection pool config |
| `postgresql` | Designing a schema, choosing column types, or adding indexes |
| `alembic` | Creating or running database migrations; migration deploy safety |
| `python-environment` | Editing pyproject.toml, uv commands, type hints, or ruff/mypy config |
| `python-testing` | Creating or modifying test files, fixtures, or mocks |
| `python-observability` | Adding structlog logging, metrics, health checks, or correlation IDs |
| `python-security` | Secrets management, CORS, rate limiting, or input validation |

## Hooks

This plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-invariants.js`) that
injects the **Python backend invariants** as always-on context. It fires on the `startup`, `clear`,
and `compact` events and activates automatically when the plugin is enabled.

**Why a hook and not just skills:** the load-bearing rules here (type hints, no `Any`/`# type:
ignore` without comment, parameterized SQL, secrets via `pydantic-settings`, the never-log list,
correlation-ID propagation) are *invariants* — they must hold on every relevant change. But skill
auto-loading is evaluated against the user's prompt at the start of a turn, so the invariant skills
(`python-security`, `python-observability`, the style half of `python-environment`) reliably
under-fire — nothing in "add a search endpoint" signals "this is security/logging sensitive." The
action skills (`fastapi`, `python-testing`, `alembic`, `asyncpg`) trigger fine and stay on-demand.
The hook injects a compact version of the invariants every session so they always apply; each rule
is tagged with the skill (e.g. `[python-security]`) that documents it in depth, loadable as
`ceh-python-service:<name>`.

## Agents

| Agent | When to Use |
|-------|-------------|
| `python-unit-tester` | Write isolated unit tests for a function or class |
| `python-integration-tester` | Write tests for module boundaries and DB interactions |
| `python-system-tester` | Write full E2E scenario tests (explicit request only — slow) |

## Scripts

| Script | Usage |
|--------|-------|
| `run-unit-tests.sh [path]` | Run unit tests only (excludes integration/system) |
| `run-integration-tests.sh [path]` | Run integration tests (requires `TEST_DATABASE_URL`) |
| `run-system-tests.sh [path] [--no-docker]` | Run system tests with optional Docker orchestration |
