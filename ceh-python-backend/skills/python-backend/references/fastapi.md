# FastAPI Conventions

## Route Handlers Are Thin

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

## Dependency Injection for All Shared Resources

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

## Always Declare `response_model=`

Never return raw dicts from route handlers. Always declare `response_model=SomePydanticModel` on the decorator.

## Middleware Order

Register in this order in `app/main.py` (FastAPI processes in reverse registration order):

1. Correlation ID middleware (outermost)
2. CORS middleware
3. Rate limiting middleware
4. Request logging middleware (innermost)

## Global Exception Handlers

Register domain-to-HTTP mappings once in `app/core/middleware.py`, not repeated in every route handler:

```python
@app.exception_handler(SessionNotFoundError)
async def session_not_found_handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "session_not_found", "message": str(exc), "correlation_id": get_correlation_id()}}
    )
```
