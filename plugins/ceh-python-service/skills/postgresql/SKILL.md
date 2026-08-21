---
name: postgresql
description: >-
  Load this skill when designing or modifying a PostgreSQL schema: defining tables and columns,
  choosing column types (TIMESTAMPTZ, JSONB), adding indexes, or naming conventions. Auto-load
  whenever a table or column is added or a schema is designed. For query, transaction,
  connection-pool, and tenant-isolation code use the asyncpg skill; for migration tooling and safety
  use the alembic skill.
---

# PostgreSQL Schema Design

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
- Every user-owned table carries an `owner_id` column so queries can enforce tenant isolation (see the asyncpg skill).

## Access and Migrations

- Query, transaction, connection-pool, and parameterized-query / tenant-isolation code lives in the `asyncpg` skill.
- Migration tooling, reversibility, and deploy-safety rules live in the `alembic` skill — schema changes are Alembic-managed, backward-compatible, and destructive changes are two-step (stop using, then drop).
