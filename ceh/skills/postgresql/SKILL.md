---
name: "postgresql"
description: >
  Load this skill when writing SQL queries, designing or modifying database schemas, adding
  indexes, working with JSONB columns, or writing asyncpg query code. Auto-load whenever a
  SQL statement is written, a table or column is added, a query uses asyncpg fetchrow/execute,
  or tenant isolation (owner_id filtering) is relevant.
---

# PostgreSQL

Schema design conventions, parameterized query rules, tenant isolation requirements, and asyncpg
usage patterns. Covers TIMESTAMPTZ vs TIMESTAMP, JSONB usage, snake_case naming, mandatory
parameterized queries (never string interpolation), owner_id filtering on every user-data query,
connection pool configuration, and atomic transactions for multi-step writes.

Read both reference files and apply the conventions defined there:

- [../architecture-design/references/postgresql.md](../architecture-design/references/postgresql.md) — schema design, query safety, tenant isolation, migration policy
- [../python-backend/references/database.md](../python-backend/references/database.md) — asyncpg usage, atomic transactions, connection pool
