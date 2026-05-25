---
name: "python-observability"
description: Load this skill when adding logging or observability to Python backend code: structlog setup, choosing log levels, adding correlation IDs, or deciding what not to log. Auto-load whenever structlog is imported, a log statement is written, or a correlation ID is referenced.
---

# Python Observability

## structlog

```python
import structlog
log = structlog.get_logger()

log.info("session_created", session_id=session_id, topic_length=len(topic))
log.warning("llm_output_rejected", session_id=session_id, reason=result.reason)
log.error("database_write_failed", session_id=session_id, error=str(e))
```

| Level | When to use |
|-------|------------|
| `DEBUG` | Detailed diagnostics (disabled in production) |
| `INFO` | Normal operational events |
| `WARNING` | Unexpected but recoverable |
| `ERROR` | Failures requiring attention |

Do not log at `INFO` on every request — use `DEBUG` for high-frequency events.

## Correlation IDs

Every request carries a `correlation_id`:
- Generated at the API boundary if absent
- Propagated through all service calls
- Included in every log entry
- Returned in `X-Correlation-ID` response header

## Never Log

Secrets, tokens, credentials, full session content, database query parameters containing user data, or PII of any kind.
