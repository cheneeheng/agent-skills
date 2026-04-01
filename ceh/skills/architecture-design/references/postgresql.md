# PostgreSQL Patterns

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

- Use `TIMESTAMPTZ` (not `TIMESTAMP`) for all timestamps. Store UTC; display in local time in the UI.
- Use `JSONB` for flexible or evolving structured data. Use typed columns for fields you filter or sort on.
- All column and table names: `snake_case`. Table names: plural.

## Parameterized Queries (Mandatory)

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

## Session / Tenant Isolation

Every query that reads or writes user-owned data must include the owning user's ID in the `WHERE` clause. One user's data must never be accessible to another.

```python
# Always filter by both entity_id AND owner_id
await conn.fetchrow(
    "SELECT * FROM entities WHERE entity_id = $1 AND owner_id = $2",
    entity_id, current_user_id
)
```

## Migrations

- Managed by **Alembic**
- All schema changes go through Alembic — never alter the database manually
- Migrations must be backward-compatible: the old app version must still work after the migration runs
- Destructive changes (column drops, table renames) are a two-step process:
  1. Deploy code that no longer uses the old structure
  2. In a subsequent release, drop the old structure
- Never run a migration and a code deploy simultaneously in a single step
