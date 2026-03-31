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

# Python Backend Engineering Standards: FastAPI Application Structure with Thin Route Handlers and Dependency Injection, uv Package and Virtual Environment Management, Pydantic v2 Data Modeling, Python 3.12 Async Patterns, ruff Lint and Format Configuration, mypy Strict Type Checking, pytest with pytest-asyncio for Async Tests, asyncpg PostgreSQL Parameterized Queries and Atomic Transactions, Custom Exception Hierarchy with HTTP Mapping, Google-Style Docstrings, structlog Structured Logging, Security Baseline

---

## Environment

- Python: **3.12**
- Package manager: **uv** (not pip, not poetry)
- Virtual environment: `.venv/` (managed by uv — do not create manually)
- Project manifest: `pyproject.toml`
- Lockfile: `uv.lock` (authoritative — never edit manually)

| Action | Command |
|--------|---------|
| Install all dependencies | `uv sync` |
| Add a production dependency | `uv add <package>` |
| Add a dev dependency | `uv add --dev <package>` |
| Run any command | `uv run <command>` |
| Start development server | `uv run uvicorn app.main:app --reload` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |

**Never edit `uv.lock` manually. Never commit `.env`.**

---

## pyproject.toml Configuration

```toml
[project]
name = "your-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic-settings",
    "asyncpg",
    "alembic",
    "structlog",
]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "N",   # pep8-naming
    "B",   # flake8-bugbear
]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.mypy]
strict = true
python_version = "3.12"
ignore_missing_imports = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## Coding Style

- Line length: **88 characters**
- Follow Google Python Style Guide
- Prefer explicit, readable code over clever code

### Type Hints (Required Everywhere)

- Required on all function signatures (parameters and return types)
- Required on class attributes
- Use Python 3.12 built-in generics: `list[str]`, not `List[str]`
- Do not use `Any` without a comment explaining why

### Docstrings (Google Style — Required on All Public Symbols)

Missing docstrings on public modules, classes, functions, and methods are considered incomplete work.

```python
def validate_event(event: ReasoningEvent, state: SessionState) -> ValidationResult:
    """Validates a reasoning event against the current session state.

    Args:
        event: The reasoning event proposed by the LLM.
        state: The current canonical session state.

    Returns:
        A ValidationResult indicating success or the specific failure reason.

    Raises:
        InvalidEventTypeError: If the event type is not in the allowed enum.
    """
```

### Naming Conventions

| Kind | Convention | Example |
|------|-----------|---------|
| Variables, functions | `snake_case` | `session_id`, `validate_event` |
| Classes | `PascalCase` | `SessionState`, `ChallengeEntity` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_CHALLENGES` |
| Private members | `_leading_underscore` | `_apply_event` |
| Type aliases | `PascalCase` | `ChallengeId = str` |

Use descriptive, intention-revealing names. Avoid abbreviations except well-known ones (`id`, `url`, `http`).

### Imports (Three Groups, Separated by Blank Lines)

```python
# 1. Standard library
import asyncio
from typing import Optional

# 2. Third-party
import asyncpg
from fastapi import HTTPException
from pydantic import BaseModel

# 3. Local application
from app.models.session import SessionState
from app.services.reasoning import ReasoningEngine
```

Use `isort` (via ruff) to enforce this automatically. Never use wildcard imports (`from module import *`).

### Data Models — Pydantic v2 for Everything Structured

```python
# Good — typed, validated, documented
class CreateSessionRequest(BaseModel):
    topic: str

class SessionResponse(BaseModel):
    session_id: str
    topic: str
    created_at: datetime

# Bad — untyped, unvalidated
session = {"session_id": "s_1", "topic": "foo"}
```

Use `BaseModel` for all API request/response types and domain entities. Reserve plain dataclasses only for simple value objects with no validation logic.

### Async / Await

All FastAPI route handlers must be `async def`. All I/O calls must use `await`. Never call blocking functions directly in async handlers.

```python
# Good — non-blocking
@router.post("/sessions/{session_id}/message")
async def send_message(session_id: str, body: MessageRequest) -> MessageResponse:
    state = await state_manager.load(session_id)
    ...

# Bad — blocks the event loop
@router.post("/sessions/{session_id}/message")
def send_message(session_id: str, body: MessageRequest) -> MessageResponse:
    state = state_manager.load_sync(session_id)
    ...
```

If a blocking library must be used, delegate to a thread pool:
```python
result = await asyncio.get_event_loop().run_in_executor(None, blocking_fn, arg)
```

Do not use `time.sleep()` — use `await asyncio.sleep()`.

---

## Linting and Type Checking

**ruff** is the single tool for linting and formatting. It replaces flake8, pylint, isort, and Black. Do not introduce those tools separately.

**mypy** handles type checking. It is separate from ruff.

### Required Checks Before Every PR

```bash
uv run ruff check .           # Lint
uv run ruff format --check .  # Format check (does not modify)
uv run mypy .                 # Type check
```

Do not use `# type: ignore` without a comment explaining why. Do not downgrade `strict = true` to silence errors — fix the underlying type issue.

---

## Testing

Framework: **pytest** with **pytest-asyncio** (`asyncio_mode = "auto"` in `pyproject.toml`)

HTTP testing: **`httpx.AsyncClient`** (async, preferred) or **FastAPI `TestClient`** (sync)

### Test Structure

```
backend/
├── app/
│   └── services/
│       └── reasoning/
│           └── engine.py
└── tests/
    ├── unit/         # Isolated — no I/O, mock all external dependencies
    ├── integration/  # Real database, mock only external APIs (LLM, payment)
    └── conftest.py   # Shared fixtures: test DB, async client, mock factories
```

Test files mirror source structure. Naming: `test_<what>_<expected_behavior>.py`. One logical behavior per test.

### Unit Tests — Fast, No I/O

```python
class TestReasoningEngine:
    async def test_validate_rejects_unknown_event_type(self):
        engine = ReasoningEngine()
        event = ReasoningEvent(event_type="invented_type", ...)
        result = await engine.validate(event, state)
        assert result.is_invalid
        assert "invalid event type" in result.reason
```

### Integration Tests — Real Database, Never Mocked

```python
class TestSessionsAPI:
    async def test_post_message_creates_event(
        self, async_client: AsyncClient, test_db
    ):
        response = await async_client.post(
            f"/sessions/{session_id}/message",
            json={"content": "I think we should rewrite in Rust"}
        )
        assert response.status_code == 200
        assert len(response.json()["reasoning_events"]) > 0

        # Verify it actually landed in the database
        row = await test_db.fetchrow(
            "SELECT * FROM event_log WHERE session_id = $1", session_id
        )
        assert row is not None
```

Do **not** mock PostgreSQL in integration tests. PostgreSQL-specific behavior (JSONB, constraints, transactions) must be verified against a real instance. Each test that writes data should run in a transaction that rolls back after the test.

### Mocking

- Mock the LLM API client in all tests (no real API calls in tests)
- Mock external HTTP services
- Do **not** mock PostgreSQL in integration tests
- Use `unittest.mock` or `pytest-mock`

### Coverage Targets

| Area | Minimum |
|------|---------|
| Overall `app/` package | 80% |
| Core business logic services | 95% |

```bash
uv run pytest --cov=app --cov-report=term-missing
```

---

## FastAPI Conventions

### Route Handlers Are Thin

Route handlers validate input, call a service, and return output. No business logic lives in them.

```python
# app/api/sessions.py
router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", status_code=201, response_model=SessionResponse)
async def create_session(
    body: CreateSessionRequest,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    return await service.create(body.topic)
```

### Dependency Injection for All Shared Resources

Define all dependencies in `app/core/dependencies.py`. Never instantiate services directly inside route handlers.

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()

async def get_session_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
    settings: Settings = Depends(get_settings),
) -> SessionService:
    return SessionService(pool=pool, settings=settings)
```

### Lifespan for Startup and Shutdown

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(settings.database_url)
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)
```

Do not use the deprecated `@app.on_event("startup")`.

### Always Declare `response_model=`

Never return raw dicts from route handlers. Always declare `response_model=SomePydanticModel` on the decorator.

### Middleware Order

Register in this order in `app/main.py` (FastAPI processes in reverse registration order):

1. Correlation ID middleware (outermost)
2. CORS middleware
3. Rate limiting middleware
4. Request logging middleware (innermost)

### Global Exception Handlers

Register domain-to-HTTP mappings once in `app/core/middleware.py`, not repeated in every route handler:

```python
@app.exception_handler(SessionNotFoundError)
async def session_not_found_handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "session_not_found", "message": str(exc), "correlation_id": get_correlation_id()}}
    )
```

---

## Database (asyncpg)

Use **asyncpg** directly — no ORM. Write explicit SQL with parameterized queries.

```python
# Good — parameterized, safe
row = await conn.fetchrow(
    "SELECT session_id, topic FROM sessions WHERE session_id = $1",
    session_id
)

# Bad — string interpolation, SQL injection risk
row = await conn.fetchrow(
    f"SELECT * FROM sessions WHERE session_id = '{session_id}'"
)
```

### Atomic Transactions for Multi-Step Writes

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        # 1. Append events
        await conn.executemany(
            "INSERT INTO event_log (session_id, event_type, payload) VALUES ($1, $2, $3)",
            [(session_id, e.type, e.model_dump_json()) for e in events]
        )
        # 2. Update snapshot
        await conn.execute(
            "UPDATE sessions SET state_snapshot = $1, updated_at = NOW() WHERE session_id = $2",
            new_state.model_dump_json(), session_id
        )
```

### Connection Pool Configuration

```python
pool = await asyncpg.create_pool(
    dsn=settings.database_url,
    min_size=5,
    max_size=20,
    command_timeout=30,
)
```

Configure via environment variables, not hard-coded values.

---

## Exception Hierarchy

Define all custom exceptions in `app/core/exceptions.py`:

```python
class AppError(Exception):
    """Base exception for all application errors."""

class SessionNotFoundError(AppError):
    """Session ID does not exist."""

class ReasoningValidationError(AppError):
    """A reasoning event failed validation."""
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)

class InvalidEventTypeError(ReasoningValidationError):
    """Event type is not in the allowed enum."""

class LLMOutputInvalidError(AppError):
    """LLM response failed schema validation."""

class LLMAPIError(AppError):
    """Upstream LLM API call failed."""
```

**Rules:**
- Services raise domain exceptions
- Route handlers convert domain exceptions to `HTTPException`
- Never raise `HTTPException` inside a service layer
- Never swallow exceptions silently with bare `except:`
- Always log unexpected exceptions before re-raising

---

## Observability

### Structured Logging with structlog

```python
import structlog
log = structlog.get_logger()

log.info("session_created", session_id=session_id, topic_length=len(topic))
log.warning("llm_output_rejected", session_id=session_id, reason=result.reason)
log.error("database_write_failed", session_id=session_id, error=str(e))
```

| Level | When to use |
|-------|------------|
| `DEBUG` | Detailed diagnostic information (disabled in production) |
| `INFO` | Normal operational events (session created, message processed) |
| `WARNING` | Unexpected but recoverable (LLM output rejected, retry attempted) |
| `ERROR` | Failures requiring attention (database write failed, API unavailable) |

Do not log at `INFO` on every request — use `DEBUG` for high-frequency events.

### Correlation IDs

Every request must carry a `correlation_id`:
- Generated at the API boundary if not present in request headers
- Propagated through all service calls within that request
- Included in every log entry for that request
- Returned in response headers (`X-Correlation-ID`)

### Never Log

- Secrets, tokens, or credentials
- Full session content (user messages, reasoning state)
- Database query parameters containing user data
- PII of any kind

---

## Security Baseline

- Secrets loaded via `pydantic-settings` (`BaseSettings`) from `.env` — never hard-coded
- `.env` files must never be committed — `.gitignore` enforced
- Validate all inputs at the API boundary using Pydantic models
- Never pass raw user input to database queries — use parameterized queries always
- All LLM output must pass schema validation before any state mutation
- Use `ConfigDict(extra='forbid')` on all LLM output models
- Apply rate limiting per session on mutation endpoints (e.g. 10 req/min)
- Configure CORS explicitly — no wildcard origins in production
- Session tokens: randomly generated (`secrets.token_urlsafe(32)`), never logged, never in URLs
- Run `uv run pip-audit` before every release to check for known vulnerabilities
