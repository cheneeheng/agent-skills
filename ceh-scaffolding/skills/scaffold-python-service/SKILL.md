---
name: "scaffold-python-service"
description: Load this skill when starting or scaffolding a new Python (FastAPI) web service: creating the initial directory layout, layer boundaries, base config, and .gitignore. Trigger when the user says "start/scaffold a FastAPI service", "new Python backend project", or sets up a fresh service repo. For a library use scaffold-python-library; for the frontend use scaffold-web-frontend.
---

# Scaffold a Python Service

Organize by concern, not by file type. Each layer has one job.

```
project/
├── backend/
│   ├── app/
│   │   ├── api/           # Thin route handlers — validate input, call service, return output
│   │   ├── core/          # Config, dependencies, exceptions, middleware
│   │   ├── models/        # Pydantic request/response + domain models
│   │   ├── services/      # Business logic — no HTTP, no SQL
│   │   └── db/            # Database queries — SQL only, no business logic
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── system/
├── migrations/            # Database migrations (Alembic)
├── pyproject.toml
└── .gitignore
```

## Hard Layer Rules

- Route handlers contain no business logic — they call services
- Services contain no SQL — they call the database layer
- Database layer contains no business logic — it executes SQL
- One mutation path per aggregate — if multiple services could write the same table, define a single state manager

## Initial Config

- `pyproject.toml` with uv, ruff, mypy, pytest config — see `ceh-python-service:python-service-environment`.
- Web service deps: `fastapi`, `uvicorn[standard]`, `pydantic-settings`, `asyncpg`, `alembic`, `structlog`.

## .gitignore

```
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.db
.DS_Store
```
