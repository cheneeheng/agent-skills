# ceh-python-backend

Python backend engineering standards for the FastAPI + uv + asyncpg stack.

## Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `fastapi` | Writing route handlers, dependencies, lifespan, or exception handlers |
| `python-testing` | Creating or modifying test files, fixtures, or mocks |
| `python-environment` | Editing pyproject.toml, uv commands, type hints, or ruff/mypy config |
| `asyncpg` | Writing database queries, transactions, or connection pool config |
| `python-observability` | Adding structlog logging, correlation IDs, or choosing log levels |
| `python-security` | Secrets management, CORS, rate limiting, or session token generation |
| `alembic` | Creating or running database migrations |

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
