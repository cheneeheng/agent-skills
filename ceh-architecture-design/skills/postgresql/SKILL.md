---
name: "postgresql"
description: Load this skill when writing SQL queries, designing or modifying database schemas, adding indexes, working with JSONB columns, or writing asyncpg query code. Auto-load whenever a SQL statement is written, a table or column is added, a query uses asyncpg fetchrow/execute, or tenant isolation (owner_id filtering) is relevant.
---

# PostgreSQL and asyncpg

## Schema Design

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

- `TIMESTAMPTZ` (not `TIMESTAMP`) for all timestamps. Store UTC; display local in UI.
- `JSONB` for flexible/evolving data. Typed columns for fields you filter or sort on.
- All names: `snake_case`. Table names: plural.

## Parameterized Queries (Mandatory)

Never use string interpolation in SQL. Use positional parameters (`$1`, `$2`, etc.).

```python
row = await conn.fetchrow(
    "SELECT entity_id, status FROM entities WHERE entity_id = $1 AND owner_id = $2",
    entity_id, owner_id
)
```

## Tenant Isolation

Every query on user-owned data must filter by the owning user's ID. One user's data must never be accessible to another.

```python
await conn.fetchrow(
    "SELECT * FROM entities WHERE entity_id = $1 AND owner_id = $2",
    entity_id, current_user_id
)
```

## Atomic Transactions for Multi-Step Writes

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        await conn.executemany(
            "INSERT INTO event_log (entity_id, event_type, payload) VALUES ($1, $2, $3)",
            [(entity_id, e.type, e.model_dump_json()) for e in events]
        )
        await conn.execute(
            "UPDATE entities SET state_snapshot = $1, updated_at = NOW() WHERE entity_id = $2",
            new_state.model_dump_json(), entity_id
        )
```

## Connection Pool Configuration

```python
pool = await asyncpg.create_pool(
    dsn=settings.database_url,
    min_size=5,
    max_size=20,
    command_timeout=30,
)
```

Configure via environment variables, never hard-coded.

## Migrations

- Managed by **Alembic** — never alter the database manually
- Migrations must be backward-compatible: old app version must still work after migration runs
- Destructive changes (column drops, table renames) are a two-step process:
  1. Deploy code that no longer uses the old structure
  2. In a subsequent release, drop the old structure
- Never run a migration and a code deploy simultaneously
