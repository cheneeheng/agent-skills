# Coding Style

- Line length: **88 characters**
- Follow Google Python Style Guide
- Prefer explicit, readable code over clever code

## Type Hints (Required Everywhere)

- Required on all function signatures (parameters and return types)
- Required on class attributes
- Use Python 3.12 built-in generics: `list[str]`, not `List[str]`
- Do not use `Any` without a comment explaining why

## Docstrings (Google Style — Required on All Public Symbols)

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

## Naming Conventions

| Kind | Convention | Example |
|------|-----------|---------|
| Variables, functions | `snake_case` | `session_id`, `validate_event` |
| Classes | `PascalCase` | `SessionState`, `ChallengeEntity` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_CHALLENGES` |
| Private members | `_leading_underscore` | `_apply_event` |
| Type aliases | `PascalCase` | `ChallengeId = str` |

Use descriptive, intention-revealing names. Avoid abbreviations except well-known ones (`id`, `url`, `http`).

## Imports (Three Groups, Separated by Blank Lines)

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

## Data Models — Pydantic v2 for Everything Structured

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

## Async / Await

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
result = await asyncio.get_running_loop().run_in_executor(None, blocking_fn, arg)
```

Do not use `time.sleep()` — use `await asyncio.sleep()`.
