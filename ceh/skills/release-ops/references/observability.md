# Observability

## Structured Logging with structlog

All log output is structured JSON. Never use `print()` or unstructured string interpolation in log calls.

```python
import structlog
log = structlog.get_logger()

# Good — structured, machine-parseable
log.info("request_completed", endpoint="/resources", status=200, duration_ms=42)
log.warning("upstream_timeout", service="payment-api", attempt=2)
log.error("database_connection_failed", host=settings.db_host, error=str(e))

# Bad — unstructured
print(f"Request completed in {duration}ms")
logging.info("Database error: " + str(e))
```

## Log Levels

| Level | Use for |
|-------|---------|
| `DEBUG` | Detailed diagnostics — disabled in production |
| `INFO` | Normal operations (request received, resource created) |
| `WARNING` | Unexpected but recoverable (upstream retry, validation rejection) |
| `ERROR` | Failures requiring attention (unhandled exception, dependency failure) |

Do not log at `INFO` on every request — use `DEBUG` for high-frequency events.

**Never log:** secrets, tokens, passwords, PII, raw user-provided content, or full external API responses.

## Correlation IDs

Every request carries a `correlation_id` that must propagate through the full request lifecycle:

- Generated at the API boundary if absent from request headers
- Bound to every log entry for the duration of the request via `structlog.contextvars`
- Returned in the `X-Correlation-ID` response header
- Included in API error response bodies so users can report it

```python
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", generate_id("req"))
    with structlog.contextvars.bound_contextvars(correlation_id=correlation_id):
        response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response
```

## Required Metrics

| Metric | Type | Labels |
|--------|------|--------|
| `requests_total` | Counter | `endpoint`, `method`, `status_code` |
| `request_duration_ms` | Histogram | `endpoint`, `method` |
| `errors_total` | Counter | `error_type`, `endpoint` |
| `external_calls_total` | Counter | `service`, `status` |
| `external_call_duration_ms` | Histogram | `service` |

Add domain-specific metrics as needed (e.g. `orders_created_total`, `reasoning_events_applied_total`).

Use Prometheus-compatible instrumentation (`prometheus-fastapi-instrumentator` or equivalent).

## Health Check Endpoint

```
GET /health
```

Returns `200` when healthy:
```json
{ "status": "ok", "database": "ok", "version": "1.4.2" }
```

Returns `503` when any critical dependency is unavailable:
```json
{ "status": "degraded", "database": "error", "version": "1.4.2" }
```

The health check must verify actual database connectivity — not just process liveness. Used by load balancers, deployment pipelines, and rollback automation.
