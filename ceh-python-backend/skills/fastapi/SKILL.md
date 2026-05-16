---
name: "fastapi"
description: >
  Load this skill when writing FastAPI route handlers, services, or middleware: adding a new
  endpoint, wiring up dependency injection, configuring lifespan startup/shutdown, registering
  exception handlers, or defining the custom exception hierarchy. Auto-load whenever a route
  handler is written, a FastAPI dependency is defined, or a domain exception is added.
---

# FastAPI Conventions

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
    app.state.db_pool = await asyncpg.create_pool(settings.database_url)
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
    return JSONResponse(status_code=404, content={"code": "session_not_found", "message": str(exc)})
```

## Exception Hierarchy

Define in `app/core/exceptions.py`:

```python
class AppError(Exception):
    """Base exception for all application errors."""

class SessionNotFoundError(AppError): ...
class ReasoningValidationError(AppError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)
class InvalidEventTypeError(ReasoningValidationError): ...
```

- Services raise domain exceptions; global handlers map them to HTTP — never per-route
- Never raise `HTTPException` inside a service layer
- Never swallow exceptions silently with bare `except:`
