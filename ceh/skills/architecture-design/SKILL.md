---
name: "architecture-design"
description: >
  Load this skill when making structural decisions, designing new APIs, defining domain models,
  working on event-sourced state, designing or modifying database schemas, or wiring up an LLM
  integration. Covers: ADR format and lifecycle for recording durable decisions, repository layer
  boundaries and separation of concerns, domain modeling with immutable identifiers and bounded
  status enums, event sourcing with append-only event log and atomic snapshot caching, REST API
  URL conventions and HTTP status code usage, consistent error response shapes, API versioning
  strategy, PostgreSQL schema patterns with JSONB and parameterized queries, and LLM integration
  safety rules (stateless LLM as proposal engine, backend validates before any commit). Use this
  skill whenever you are making design decisions, building new endpoints, touching the database
  layer, or integrating an LLM into the application.
---

# Software Architecture Design Standards: Architecture Decision Records Format and Lifecycle, Repository Structure and Layer Boundaries, Domain Modeling with Immutable Identifiers and Bounded Status Enums, Event Sourcing with Append-Only Event Log and Snapshot Cache, REST API URL Conventions and HTTP Status Codes, Consistent Error Response Shape and API Versioning, PostgreSQL Schema Patterns with JSONB and Parameterized Queries, LLM Integration Safety with Stateless Proposal Engine and Backend Validation

---

## Architecture Decision Records (ADRs)

Record every significant architectural decision. A decision is significant if it would be confusing to a future developer without the context behind it, or if reversing it would require a migration or broad refactor.

### When to Write an ADR

- Choosing a framework, runtime, or infrastructure tool
- Defining a data persistence strategy (schema shape, migration approach)
- Choosing between fundamentally different implementation patterns
- Any major version upgrade of a core dependency
- Any decision you find yourself explaining repeatedly in PR reviews

### ADR Format

```markdown
## ADR-<NNN>: <Short, Descriptive Title>

**Status:** Proposed | Accepted | Superseded by ADR-<NNN>
**Date:** YYYY-MM-DD

### Context
Problem or situation requiring a decision. Include constraints, goals, and options considered.

### Decision
What was decided. Be explicit and unambiguous.

### Consequences
Implications, trade-offs, limitations, follow-up considerations.

### Alternatives Considered (Optional)
What was not chosen and why.
```

### ADR Lifecycle

- `Proposed` — written, pending team review
- `Accepted` — agreed upon and in force
- `Superseded by ADR-NNN` — replaced; link to the superseding ADR

Never delete ADRs. Mark as superseded and link forward. History is valuable.

To change a decision: write a new ADR that references and supersedes the old one. Never silently diverge from an accepted ADR.

---

## Repository Structure and Layer Boundaries

Organize by concern, not by file type. Each layer has exactly one job.

```
project/
├── backend/
│   ├── app/
│   │   ├── api/           # Thin route handlers — validate input, call service, return output
│   │   ├── core/          # Config, dependencies, exceptions, middleware
│   │   ├── models/        # Pydantic request/response + domain models
│   │   ├── services/      # Business logic — no HTTP, no SQL
│   │   └── db/            # Database queries — SQL only, no business logic
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── routes/        # SvelteKit pages and load functions
│   │   └── lib/
│   │       ├── components/ # UI components — receive props, emit events
│   │       ├── stores/     # Reactive state — updated by API responses only
│   │       ├── api/        # Centralized API client — all fetch calls go here
│   │       └── types/      # Shared TypeScript types
│   └── tests/
└── migrations/            # Database migrations (Alembic)
```

### Hard Layer Rules

- Route handlers contain no business logic — they call services
- Services contain no SQL — they call the database layer
- Database layer contains no business logic — it executes SQL
- Components do not write to stores directly — they call callbacks or dispatch events
- All `fetch` calls go through the centralized API client — components never call `fetch`
- One mutation path per aggregate — if multiple services could write the same table, define a single state manager

---

## Domain Modeling

### Immutable Identifiers

Every entity has an application-generated, prefixed, URL-safe identifier. Never use database auto-increment as the public ID — it leaks row counts and is meaningless in logs.

```python
import secrets

def generate_id(prefix: str) -> str:
    """Generates a prefixed, URL-safe unique identifier."""
    return f"{prefix}_{secrets.token_urlsafe(12)}"

# Usage
session_id = generate_id("sess")   # sess_abc123...
resource_id = generate_id("res")   # res_xyz456...
```

### Status Enums — Bounded, Not Free-Form Strings

Status values must come from an explicit, closed set. Never trust free-form strings from external callers for status fields.

```python
# Python — use StrEnum for serialization compatibility
from enum import StrEnum

class ResourceStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

```ts
// TypeScript — const assertion, never TypeScript enum
const ResourceStatus = {
  Active: 'active',
  Archived: 'archived',
  Deleted: 'deleted',
} as const;
type ResourceStatus = typeof ResourceStatus[keyof typeof ResourceStatus];
```

### Immutability Rules

- IDs are set once at creation, never changed
- `created_at` timestamps are set once, never updated
- Status transitions must be validated — not all transitions are legal
- Document all legal and illegal transitions explicitly

---

## Event Sourcing

### Core Pattern

State is derived from an ordered sequence of immutable events. Never mutate state directly — append an event and recompute the snapshot.

```
event_log (append-only)       state_snapshot (cache)
─────────────────────         ─────────────────────
event 1: created              { status: active, ... }
event 2: updated              ↑ derived from all events
event 3: archived             updated atomically with each event append
```

### Append-Only Invariant

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

### Atomic Event + Snapshot Write

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

### Event Schema Design

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

### Allowed Event Types

Event types form a closed, application-controlled enum. External callers (including LLMs) cannot invent new event types. Any unrecognized event type is rejected before processing begins.

---

## REST API Design

### URL Conventions

- Lowercase, hyphen-separated path segments: `/user-profiles`, not `/userProfiles`
- Plural nouns for collections: `/sessions`, not `/session`
- Nested resources for ownership: `/sessions/{id}/messages`
- No verbs in URLs — HTTP methods express the action

```
POST   /resources              Create
GET    /resources              List
GET    /resources/{id}         Get one
PATCH  /resources/{id}         Partial update
DELETE /resources/{id}         Delete
POST   /resources/{id}/archive Non-CRUD action as sub-resource
```

### HTTP Status Codes

| Code | When to use |
|------|------------|
| `200 OK` | Successful GET, PATCH, or DELETE returning data |
| `201 Created` | Successful POST that creates a resource |
| `204 No Content` | Successful operation with no response body |
| `400 Bad Request` | Malformed request syntax or type mismatch |
| `401 Unauthorized` | Authentication required but missing or invalid |
| `403 Forbidden` | Authenticated but not authorized |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Resource already exists, or illegal state transition |
| `422 Unprocessable Entity` | Syntactically valid but semantically invalid (Pydantic validation) |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server-side failure |
| `503 Service Unavailable` | Dependency unavailable (DB down, upstream timeout) |

Do not return `200` for errors. Do not return `500` for user input errors.

### Error Response Shape

All errors return a consistent envelope:

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "Resource with ID res_abc123 does not exist.",
    "correlation_id": "req_xyz789"
  }
}
```

| Field | Description |
|-------|-------------|
| `code` | Machine-readable, snake_case, stable across versions |
| `message` | Human-readable, safe to display |
| `correlation_id` | Propagated from the request for log tracing |

### API Versioning

Avoid versioning as long as possible — prefer backward-compatible additions (new optional fields, new endpoints). Only version when a breaking change cannot be avoided.

When required: use URL prefix (`/v2/resources`), maintain `/v1/` for a documented deprecation period, and record the deprecation timeline in `ARCHITECTURE_DECISIONS.md`.

### Headers

| Header | Direction | Purpose |
|--------|-----------|---------|
| `X-Correlation-ID` | Request + Response | Request tracing |
| `Content-Type: application/json` | Both | Required on all JSON endpoints |

---

## PostgreSQL Patterns

### Schema Design

```sql
CREATE TABLE entities (
    entity_id      TEXT PRIMARY KEY,
    owner_id       TEXT NOT NULL,
    status         TEXT NOT NULL DEFAULT 'active',
    state_snapshot JSONB NOT NULL DEFAULT '{}',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_entities_owner_id ON entities(owner_id);
CREATE INDEX idx_entities_status ON entities(status) WHERE status != 'deleted';
```

- Use `TIMESTAMPTZ` (not `TIMESTAMP`) for all timestamps. Store UTC; display in local time in the UI.
- Use `JSONB` for flexible or evolving structured data. Use typed columns for fields you filter or sort on.
- All column and table names: `snake_case`. Table names: plural.

### Parameterized Queries (Mandatory)

Never use string interpolation in SQL. Use positional parameters (`$1`, `$2`, etc.) always.

```python
# Good — safe
row = await conn.fetchrow(
    "SELECT entity_id, status FROM entities WHERE entity_id = $1 AND owner_id = $2",
    entity_id, owner_id
)

# Bad — SQL injection risk
row = await conn.fetchrow(
    f"SELECT * FROM entities WHERE entity_id = '{entity_id}'"
)
```

### Session / Tenant Isolation

Every query that reads or writes user-owned data must include the owning user's ID in the `WHERE` clause. One user's data must never be accessible to another.

```python
# Always filter by both entity_id AND owner_id
await conn.fetchrow(
    "SELECT * FROM entities WHERE entity_id = $1 AND owner_id = $2",
    entity_id, current_user_id
)
```

### Migrations

- Managed by **Alembic**
- All schema changes go through Alembic — never alter the database manually
- Migrations must be backward-compatible: the old app version must still work after the migration runs
- Destructive changes (column drops, table renames) are a two-step process:
  1. Deploy code that no longer uses the old structure
  2. In a subsequent release, drop the old structure
- Never run a migration and a code deploy simultaneously in a single step

---

## LLM Integration Safety

### Core Pattern: LLM Proposes, Backend Validates and Commits

The LLM is a stateless collaborator. It never has direct write access to state. Every LLM output must be validated before any mutation occurs.

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

### LLM Output Schema

All LLM output models use `extra='forbid'`. Unknown fields are rejected immediately — never silently ignored.

```python
from pydantic import BaseModel, ConfigDict

class LLMOutput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    chat_message: ChatMessage
    proposed_events: list[ProposedEvent]

class ProposedEvent(BaseModel):
    model_config = ConfigDict(extra='forbid')
    event_type: AllowedEventType  # validated against the closed enum
```

### Invariant Enforcement Before Any Commit

```python
def validate_events(events: list[ProposedEvent], current_state: State) -> None:
    for event in events:
        if event.event_type not in AllowedEventType:
            raise ValidationError(f"Unknown event type: {event.event_type}")
        validate_event_against_state(event, current_state)
    # All-or-nothing: if any event is invalid, none are applied
```

### LLM Safety Rules

| Rule | Reason |
|------|--------|
| Validate before any state mutation | LLM output is untrusted input |
| `extra='forbid'` on all output models | Prevent hidden fields bypassing validation |
| Reject unknown event types immediately | No LLM authority escalation |
| Never retry on schema validation failures | Retrying bad structure wastes quota |
| Log invalid output at WARNING (truncated) | Auditability without leaking session content |
| Never log full LLM responses at INFO | May contain user content or PII |
| Reject the full event batch on any single invalid event | No partial state corruption |
