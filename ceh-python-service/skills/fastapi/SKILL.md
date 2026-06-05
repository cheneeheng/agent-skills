---
name: "fastapi"
description: Load this skill when writing FastAPI route handlers, services, or middleware: adding a new endpoint, wiring up dependency injection, configuring lifespan startup/shutdown, registering exception handlers, or defining the custom exception hierarchy. Auto-load whenever a route handler is written, a FastAPI dependency is defined, or a domain exception is added.
---

# FastAPI Conventions

## REST API Design

### URL Conventions

- Lowercase, hyphen-separated path segments: `/user-profiles`
- Plural nouns for collections: `/sessions`
- Nested resources for ownership: `/sessions/{id}/messages`
- No verbs in URLs — HTTP methods express the action

```
POST   /resources              Create
GET    /resources              List
GET    /resources/{id}         Get one
PATCH  /resources/{id}         Partial update
DELETE /resources/{id}         Delete
POST   /resources/{id}/archive Non-CRUD action as sub-resource
```

### HTTP Status Codes

| Code | When to use |
|------|------------|
| `200 OK` | Successful GET, PATCH, or DELETE returning data |
| `201 Created` | Successful POST that creates a resource |
| `204 No Content` | Successful operation with no response body |
| `400 Bad Request` | Malformed request syntax or type mismatch |
| `401 Unauthorized` | Authentication required but missing or invalid |
| `403 Forbidden` | Authenticated but not authorized |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Resource already exists, or illegal state transition |
| `422 Unprocessable Entity` | Syntactically valid but semantically invalid (Pydantic validation) |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server-side failure |
| `503 Service Unavailable` | Dependency unavailable (DB down, upstream timeout) |

Do not return `200` for errors. Do not return `500` for user input errors.

### Error Response Shape

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "Resource with ID res_abc123 does not exist.",
    "correlation_id": "req_xyz789"
  }
}
```

| Field | Description |
|-------|-------------|
| `code` | Machine-readable, snake_case, stable across versions |
| `message` | Human-readable, safe to display |
| `correlation_id` | Propagated from the request for log tracing |

### API Versioning

Prefer backward-compatible additions (new optional fields, new endpoints). Only version when a breaking change cannot be avoided. When required: use a URL prefix (`/v2/resources`), maintain `/v1/` for a documented deprecation period, and record the timeline as an ADR.

### Headers

| Header | Direction | Purpose |
|--------|-----------|---------|
| `X-Correlation-ID` | Request + Response | Request tracing |
| `Content-Type: application/json` | Both | Required on all JSON endpoints |

## Route Handlers Are Thin

Validate input, call a service, return output. No business logic.

```python
router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", status_code=201, response_model=SessionResponse)
async def create_session(
    body: CreateSessionRequest,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    return await service.create(body.topic)
```

## Dependency Injection

All dependencies in `app/core/dependencies.py`. Never instantiate services inside route handlers.

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

## Lifespan for Startup and Shutdown

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pool sizing per the asyncpg skill (min_size=5, max_size=20, command_timeout=30)
    app.state.db_pool = await asyncpg.create_pool(
        settings.database_url, min_size=5, max_size=20, command_timeout=30
    )
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)
```

Do not use the deprecated `@app.on_event("startup")`.

## Response Model

Always declare `response_model=SomePydanticModel`. Never return raw dicts.

## Middleware Order

Register in this order (FastAPI processes in reverse registration order):

1. Correlation ID middleware (outermost)
2. CORS middleware
3. Rate limiting middleware
4. Request logging middleware (innermost)

## Global Exception Handlers

Register domain-to-HTTP mappings once in `app/core/middleware.py`:

```python
@app.exception_handler(SessionNotFoundError)
async def handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "code": "session_not_found",
            "message": str(exc),
            "correlation_id": getattr(request.state, "correlation_id", None),
        },
    )
```

The `correlation_id` comes from the correlation-ID middleware (registered outermost). Include it so
the body matches the error contract above (`code` / `message` / `correlation_id`).

## Exception Hierarchy

Define in `app/core/exceptions.py`:

```python
class AppError(Exception):
    """Base exception for all application errors."""

class SessionNotFoundError(AppError): ...
class DomainValidationError(AppError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)
```

- Services raise domain exceptions; global handlers map them to HTTP — never per-route
- Never raise `HTTPException` inside a service layer
- Never swallow exceptions silently with bare `except:`
