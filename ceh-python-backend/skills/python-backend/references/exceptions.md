# Exception Hierarchy

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

## Rules

- Services raise domain exceptions
- Route handlers convert domain exceptions to `HTTPException`
- Never raise `HTTPException` inside a service layer
- Never swallow exceptions silently with bare `except:`
- Always log unexpected exceptions before re-raising
