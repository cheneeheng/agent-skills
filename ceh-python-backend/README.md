# ceh-python-backend

Python backend engineering standards for the FastAPI + uv + asyncpg stack. Covers environment
setup, coding style, linting, testing, database access, exception hierarchy, observability,
security, and Alembic migrations.

## Bundle Skills

| Skill | Invoke | Description |
|-------|--------|-------------|
| `python-backend` | `/python-backend` | Full stack standards — load when touching any backend Python |

## Micro-Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `fastapi` | Writing route handlers, dependencies, lifespan, or exception handlers |
| `python-testing` | Creating or modifying test files, fixtures, or mocks |

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

## Reference Files

All reference files live under `skills/python-backend/references/`:

| File | Topic |
|------|-------|
| `environment.md` | uv commands, pyproject.toml configuration |
| `coding-style.md` | Type hints, docstrings, naming, imports, Pydantic, async patterns |
| `linting.md` | ruff and mypy — required checks before every PR |
| `testing.md` | pytest, unit/integration/system structure, mocking rules, coverage |
| `fastapi.md` | Thin handlers, DI, lifespan, middleware order, exception handlers |
| `database.md` | asyncpg queries, transactions, connection pool |
| `exceptions.md` | Custom exception hierarchy and service/handler boundary rules |
| `observability.md` | structlog levels, correlation IDs, what never to log |
| `security.md` | Secrets, CORS, rate limiting, input validation baseline |
| `migrations.md` | Alembic setup, migration workflow, test database migrations |
