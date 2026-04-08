---
name: "release-ops"
description: >
  Load this skill when working on deployments, database migrations, rollbacks, incident response,
  observability setup, security configuration, or quality gates. Covers the complete release and
  operations loop: semantic versioning and release checklist, database migration safety rules with
  backward-compatible and two-step destructive changes, rollback criteria and procedure, hotfix
  process for production incidents without bypassing CI, incident severity classification and
  post-mortem format, structured logging with structlog and correlation IDs, required observability
  metrics and health check endpoint contract, secrets management and CORS configuration, rate
  limiting, and definition of done for bug fixes, features, and refactors. Use this skill any time
  you touch deployment pipelines, migrations, logging, metrics, security settings, or release
  processes.
---

# Release Operations

Standards for the complete release and operations lifecycle. Covers semantic versioning, release
checklist, database migration safety with backward-compatible and two-step destructive changes,
rollback criteria and procedure, hotfix process, incident severity classification and post-mortem
format, structured logging and correlation IDs, required metrics, health check contract, secrets
management, CORS configuration, and definition of done.

## References

Load the relevant file for the topic at hand.

| File | Topic |
|------|-------|
| [references/versioning.md](references/versioning.md) | SemVer rules, release checklist, change classification |
| [references/migrations.md](references/migrations.md) | Alembic commands, migration safety rules, two-step destructive changes |
| [references/rollback.md](references/rollback.md) | When to roll back, application and database rollback procedures |
| [references/hotfix.md](references/hotfix.md) | Hotfix branch, scope, CI requirements, deploy steps |
| [references/incidents.md](references/incidents.md) | P1/P2/P3 severity levels, response steps, post-mortem format |
| [references/observability.md](references/observability.md) | structlog levels, correlation IDs, required metrics, health check contract |
| [references/security.md](references/security.md) | Secrets management, CORS, rate limiting, input validation |
| [references/definition-of-done.md](references/definition-of-done.md) | Done criteria for bug fixes, features, refactors, coverage targets |
