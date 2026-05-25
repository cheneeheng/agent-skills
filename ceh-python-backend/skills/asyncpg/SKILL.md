---
name: "asyncpg"
description: Load this skill when writing asyncpg database code: parameterized queries, atomic transactions, connection pool configuration, or raw SQL patterns. Auto-load whenever asyncpg is imported, a SQL query is written, or a database transaction is needed.
---

# asyncpg

Use **asyncpg** directly — no ORM. Explicit SQL with parameterized queries.

## Queries

```python
row = await conn.fetchrow(
    "SELECT session_id, topic FROM sessions WHERE session_id = $1",
    session_id
)
```

## Atomic Transactions

Use transactions for all multi-step writes:

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        await conn.executemany(
            "INSERT INTO event_log (session_id, event_type, payload) VALUES ($1, $2, $3)",
            [(session_id, e.type, e.model_dump_json()) for e in events]
        )
        await conn.execute(
            "UPDATE sessions SET state_snapshot = $1, updated_at = NOW() WHERE session_id = $2",
            new_state.model_dump_json(), session_id
        )
```

## Connection Pool

```python
pool = await asyncpg.create_pool(
    dsn=settings.database_url,
    min_size=5,
    max_size=20,
    command_timeout=30,
)
```

Create the pool in the FastAPI lifespan function and expose it via `app.state.db_pool`. Never create a pool per request.
