# Database (asyncpg)

Use **asyncpg** directly — no ORM. Write explicit SQL with parameterized queries.

```python
# good
row = await conn.fetchrow(
    "SELECT session_id, topic FROM sessions WHERE session_id = $1",
    session_id
)

# bad — SQL injection risk
row = await conn.fetchrow(
    f"SELECT * FROM sessions WHERE session_id = '{session_id}'"
)
```

## Atomic Transactions for Multi-Step Writes

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        # 1. Append events
        await conn.executemany(
            "INSERT INTO event_log (session_id, event_type, payload) VALUES ($1, $2, $3)",
            [(session_id, e.type, e.model_dump_json()) for e in events]
        )
        # 2. Update snapshot
        await conn.execute(
            "UPDATE sessions SET state_snapshot = $1, updated_at = NOW() WHERE session_id = $2",
            new_state.model_dump_json(), session_id
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

Configure via environment variables, not hard-coded values.
