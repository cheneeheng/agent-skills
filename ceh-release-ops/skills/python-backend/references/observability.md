# Observability — Python Backend Specifics

## Logging Examples

Application-specific structured log calls using `structlog`:

```python
import structlog
log = structlog.get_logger()

log.info("session_created", session_id=session_id, topic_length=len(topic))
log.warning("llm_output_rejected", session_id=session_id, reason=result.reason)
log.error("database_write_failed", session_id=session_id, error=str(e))
```

## Never Log

- Secrets, tokens, or credentials
- Full session content (user messages, reasoning state)
- Database query parameters containing user data
- PII of any kind
