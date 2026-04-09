# Event Sourcing

## Core Pattern

State is derived from an ordered sequence of immutable events. Never mutate state directly — append an event and recompute the snapshot.

```
event_log (append-only)       state_snapshot (cache)
─────────────────────         ─────────────────────
event 1: created              { status: active, ... }
event 2: updated              ↑ derived from all events
event 3: archived             updated atomically with each event append
```

## Append-Only Invariant

The event log is a permanent record. `UPDATE` and `DELETE` on event log rows are forbidden, always.

```sql
CREATE TABLE event_log (
    id          BIGSERIAL PRIMARY KEY,
    entity_id   TEXT NOT NULL REFERENCES entities(entity_id),
    event_type  TEXT NOT NULL,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- The INSERT is the only permitted write. No UPDATE. No DELETE. Ever.
```

## Atomic Event + Snapshot Write

Every event append and the resulting snapshot update happen in a single transaction. A snapshot out of sync with its event log is a data integrity failure.

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        # 1. Append event
        await conn.execute(
            "INSERT INTO event_log (entity_id, event_type, payload) VALUES ($1, $2, $3)",
            entity_id, event.type, event.model_dump_json()
        )
        # 2. Update snapshot
        await conn.execute(
            "UPDATE entities SET state_snapshot = $1, updated_at = NOW() WHERE entity_id = $2",
            new_state.model_dump_json(), entity_id
        )
```

## Event Schema Design

Events must be self-contained and replayable without the original request:

```python
class EventBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    event_type: str
    entity_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ResourceCreatedEvent(EventBase):
    event_type: Literal['resource_created']
    name: str
    owner_id: str
```

## Allowed Event Types

Event types form a closed, application-controlled enum. External callers (including LLMs) cannot invent new event types. Any unrecognized event type is rejected before processing begins.
