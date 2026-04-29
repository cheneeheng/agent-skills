# Database Migrations

Tool: **Alembic** (Python)

Use the `Bash` tool to execute these commands:

```bash
uv run alembic upgrade head     # Apply all pending migrations
uv run alembic downgrade -1     # Roll back one step
uv run alembic current          # Show current revision
uv run alembic history          # Show migration history
```

## Migration Safety Rules

- Migrations run **before** the new application version deploys (blue-green safe)
- Every migration must be backward-compatible — the **old** app version must still work after the migration runs
- Never run a migration and a code deploy simultaneously in a single step
- Test the migration against a copy of production data before deploying
- Never modify existing event log rows — that table is append-only (see architecture standards)

## Two-Step Destructive Changes

Never drop a column, rename a column, or remove a table in a single release. This would break the running old version mid-deploy.

**Step 1 (this release):** Deploy code that no longer uses the old structure. Old structure stays in place.

**Step 2 (next release):** Drop the old structure now that no code references it.

```sql
-- Step 1 migration: add new column
ALTER TABLE resources ADD COLUMN new_column TEXT;

-- Step 2 migration (next release only): drop old column
ALTER TABLE resources DROP COLUMN old_column;
```

Migrations must never include `UPDATE` or `DELETE` on the `event_log` table.
