---
name: "python-backend"
description: >
  Load this skill when writing, reviewing, or debugging Python backend code using the FastAPI +
  uv + asyncpg stack. Covers the complete development loop: setting up and managing the environment
  with uv (Python 3.12), writing idiomatic async FastAPI route handlers with dependency injection,
  structuring Pydantic v2 models for requests, responses, and domain entities, enforcing code
  quality with ruff (lint + format) and mypy in strict mode, writing unit and integration tests
  with pytest and pytest-asyncio, querying PostgreSQL safely with asyncpg (parameterized queries,
  atomic transactions), defining a clean exception hierarchy that maps to HTTP responses, and
  structured logging with structlog and correlation IDs. Use this skill any time you touch backend
  Python — adding an endpoint, writing a service, fixing a bug, writing tests, or reviewing a PR.
---

# Python Backend

Engineering standards for the FastAPI + uv + asyncpg stack. Covers environment setup with uv,
coding style with type hints and Google docstrings, ruff and mypy configuration, pytest testing
patterns, FastAPI route handler conventions, asyncpg query patterns, exception hierarchy, and
structured logging with structlog and correlation IDs.

## References

Load the relevant file for the topic at hand.

| File | Topic |
|------|-------|
| [references/environment.md](references/environment.md) | uv commands, pyproject.toml configuration |
| [references/coding-style.md](references/coding-style.md) | Type hints, docstrings, naming, imports, Pydantic models, async patterns |
| [references/linting.md](references/linting.md) | ruff and mypy — required checks before every PR |
| [references/testing.md](references/testing.md) | pytest, unit vs integration tests, mocking rules, coverage targets |
| [references/fastapi.md](references/fastapi.md) | Thin handlers, dependency injection, lifespan, middleware order, exception handlers |
| [references/database.md](references/database.md) | asyncpg parameterized queries, atomic transactions, connection pool |
| [references/exceptions.md](references/exceptions.md) | Custom exception hierarchy and service/handler boundary rules |
| [references/observability.md](references/observability.md) | structlog levels, correlation IDs, what never to log |
| [references/security.md](references/security.md) | Secrets, CORS, rate limiting, input validation baseline |
