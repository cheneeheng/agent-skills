---
name: "llm-integration"
description: Load this skill when integrating LLM calls into the application: constructing prompts, defining LLM output schemas, validating LLM responses, applying proposed events from LLM output, or handling LLM API errors. Auto-load whenever an LLM API call is written, an output model is defined, or proposed events from an LLM response are being applied to state.
---

# LLM Integration Safety

## Core Pattern: LLM Proposes, Backend Validates and Commits

The LLM is a stateless collaborator with no direct write access. All output must be validated before any mutation.

```
User message
    ↓
Backend constructs prompt (with current state as context)
    ↓
LLM returns structured output (chat message + proposed events)
    ↓
Backend validates ALL proposed events against domain invariants
    ↓
  If valid: apply events atomically, return response
  If invalid: reject entirely, log warning, return error — no partial state
```

## LLM Output Schema

All LLM output models use `extra='forbid'`. Unknown fields are rejected immediately.

```python
class LLMOutput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    chat_message: ChatMessage
    proposed_events: list[ProposedEvent]

class ProposedEvent(BaseModel):
    model_config = ConfigDict(extra='forbid')
    event_type: AllowedEventType  # validated against the closed enum
```

## Invariant Enforcement Before Any Commit

```python
def validate_events(events: list[ProposedEvent], current_state: State) -> None:
    for event in events:
        if event.event_type not in AllowedEventType:
            raise ValidationError(f"Unknown event type: {event.event_type}")
        validate_event_against_state(event, current_state)
    # All-or-nothing: if any event is invalid, none are applied
```

## Safety Rules

| Rule | Reason |
|------|--------|
| Validate before any state mutation | LLM output is untrusted input |
| `extra='forbid'` on all output models | Prevent hidden fields bypassing validation |
| Reject unknown event types immediately | No LLM authority escalation |
| Never retry on schema validation failures | Retrying bad structure wastes quota |
| Log invalid output at WARNING (truncated) | Auditability without leaking session content |
| Never log full LLM responses at INFO | May contain user content or PII |
| Reject the full event batch on any single invalid event | No partial state corruption |
