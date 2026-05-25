---
name: "event-sourcing"
description: Load this skill when working with the event log or state snapshots: appending events, reading or replaying the event log, updating snapshots, designing new event types, or modifying the transaction that writes events and snapshots atomically. Auto-load whenever event_log or state_snapshot tables are touched, or a new event type is introduced.
---

# Event Sourcing

State derives from an ordered immutable event log. Never mutate directly — append an event and recompute the snapshot.

## Append-Only Invariant

The event log is a permanent record. `UPDATE` and `DELETE` on event rows are forbidden.

```sql
CREATE TABLE event_log (
    id          BIGSERIAL PRIMARY KEY,
    entity_id   TEXT NOT NULL REFERENCES entities(entity_id),
    event_type  TEXT NOT NULL,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- INSERT only. No UPDATE, no DELETE.
```

## Atomic Event + Snapshot Write

Every event append and snapshot update happen in a single transaction. An out-of-sync snapshot is a data integrity failure.

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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ResourceCreatedEvent(EventBase):
    event_type: Literal['resource_created']
    name: str
    owner_id: str
```

## Allowed Event Types

Event types form a closed, application-controlled enum. External callers (including LLMs) cannot invent new event types. Any unrecognized event type is rejected before processing begins.
