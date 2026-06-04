---
name: "postgresql"
description: Load this skill when designing or modifying a PostgreSQL schema: defining tables and columns, choosing column types (TIMESTAMPTZ, JSONB), adding indexes, enforcing tenant isolation (owner_id filtering), or applying parameterized-query and migration policy. Auto-load whenever a table or column is added, a schema is designed, or SQL-safety / tenant-isolation rules are relevant. For asyncpg query, transaction, and connection-pool code, use the asyncpg skill instead.
---

# PostgreSQL Schema and Access Design

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

## asyncpg Code Lives in the asyncpg Skill

This skill owns schema and access *design*. The concrete asyncpg code — multi-step atomic
transactions, connection-pool configuration, and query execution — lives in the `asyncpg` skill
(`ceh-python-backend:asyncpg`). The event-sourcing atomicity *principle* (event and snapshot written
in one transaction) is in the `event-sourcing` skill. Keep schema design here; keep Python
data-access code there.

## Migrations

- Managed by **Alembic** — never alter the database manually
- Migrations must be backward-compatible: old app version must still work after migration runs
- Destructive changes (column drops, table renames) are a two-step process:
  1. Deploy code that no longer uses the old structure
  2. In a subsequent release, drop the old structure
- Never run a migration and a code deploy simultaneously
