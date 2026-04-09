---
name: "database-migrations"
description: >
  Load this skill when writing, reviewing, or running database migrations: creating a new Alembic
  migration, modifying an existing one, dropping or renaming columns, or planning a schema change
  that affects a running application. Auto-load whenever an Alembic migration file is created or
  modified, or a destructive schema change (column drop, rename, table removal) is planned.
---

# Database Migrations

Alembic commands, migration safety rules (backward-compatible, old app must still work after
migration runs), and the mandatory two-step process for destructive changes (drop/rename). Never
run a migration and a code deploy simultaneously. Never modify event_log rows.

Read [../release-ops/references/migrations.md](../release-ops/references/migrations.md)
and apply the safety rules defined there.
