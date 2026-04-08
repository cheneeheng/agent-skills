# Observability

## Structured Logging with structlog

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

## Correlation IDs

Every request must carry a `correlation_id`:
- Generated at the API boundary if not present in request headers
- Propagated through all service calls within that request
- Included in every log entry for that request
- Returned in response headers (`X-Correlation-ID`)

## Never Log

- Secrets, tokens, or credentials
- Full session content (user messages, reasoning state)
- Database query parameters containing user data
- PII of any kind
