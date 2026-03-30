---
name: "ceh-release-ops"
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

# Release Engineering and Operations Standards: Semantic Versioning and Release Checklist, Database Migration Safety with Backward-Compatible Two-Step Destructive Changes, Application Rollback Criteria and Procedure, Hotfix Process for Production Incidents, Incident Severity Classification and Post-Mortem Format, Structured Logging with structlog and Correlation IDs, Required Observability Metrics, Health Check Endpoint Contract, Secrets Management and CORS Configuration, Definition of Done for Bug Fixes Features and Refactors

---

## Versioning — Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH
```

| Increment | When |
|-----------|------|
| `PATCH` | Bug fixes; no API or schema changes |
| `MINOR` | New features; backward-compatible |
| `MAJOR` | Breaking API or schema changes; requires migration guide |

Version is recorded in both `pyproject.toml` and `package.json`. Both must be updated in the same commit before tagging.

---

## Release Checklist

Complete every step in order. No skipping.

1. All CI checks pass on `main`
2. `CHANGELOG.md` updated with changes since last release
3. Version bumped in `pyproject.toml` and `package.json`
4. Commit: `chore: bump version to v<X.Y.Z>`
5. Tag: `git tag v<X.Y.Z>` and push tag
6. Docker images built and tagged with version
7. Deploy to **staging** → run smoke tests
8. Staging smoke tests pass → deploy to **production**
9. Verify `GET /health` returns `200` post-deploy
10. Confirm error rate and latency metrics are at baseline within 5 minutes

**Staging must pass before production. Non-negotiable. Skip-staging deployments require explicit approval and are flagged high-risk.**

### Change Classification

Every change must be classified before release:

| Class | Definition | Additional requirement |
|-------|-----------|----------------------|
| Internal | No user-visible or API change | None |
| User-visible | UI change, new feature, behavioral change | PR description required |
| Breaking | API contract change, schema migration, removed endpoint | ADR entry + migration plan before merge |

---

## Database Migrations

Tool: **Alembic** (Python)

```bash
uv run alembic upgrade head     # Apply all pending migrations
uv run alembic downgrade -1     # Roll back one step
uv run alembic current          # Show current revision
uv run alembic history          # Show migration history
```

### Migration Safety Rules

- Migrations run **before** the new application version deploys (blue-green safe)
- Every migration must be backward-compatible — the **old** app version must still work after the migration runs
- Never run a migration and a code deploy simultaneously in a single step
- Test the migration against a copy of production data before deploying
- Never modify existing event log rows — that table is append-only (see architecture standards)

### Two-Step Destructive Changes

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

---

## Rollback

### When to Roll Back

Roll back **immediately** — do not wait for root cause analysis — when any of these occur within 10 minutes of deployment:

- `GET /health` returns anything other than `200`
- Error rate > 5× the pre-deploy baseline
- P95 latency > 3× the pre-deploy baseline
- Any data integrity issue detected

### Application Rollback Procedure

1. Re-deploy the previous Docker image tag
2. Verify `GET /health` returns `200`
3. Confirm error rate and latency return to baseline within 2 minutes
4. Open a P1/P2 incident if production was impacted
5. Document the rollback in `DECISION_LOG.md`

### Database Rollback Considerations

- **Additive migrations** (new columns, new tables): roll back the application; leave the schema change. The old application ignores unknown columns.
- **Destructive migrations** (drops, renames): cannot be automatically rolled back. This is why the two-step process is mandatory. If a destructive migration was applied prematurely, a forward-fix is required — not a rollback.

---

## Hotfix Process

For P1/P2 production issues that cannot wait for the next normal release:

1. **Branch:** `fix/critical-<description>` from `main`
2. **Scope:** Minimal fix only — no unrelated changes
3. **Review:** 1 approval minimum, fast-tracked
4. **CI:** All checks must pass — do **not** skip CI under pressure. A broken hotfix is worse than a delayed one.
5. **Merge:** Squash merge to `main`
6. **Tag:** Bump PATCH version, apply tag
7. **Deploy:** Staging → production (abbreviated but both still required)

---

## Incident Severity

| Level | Definition | Response Time |
|-------|-----------|--------------|
| P1 | Production is down or data is corrupted | Immediate — all hands |
| P2 | Major feature broken, no workaround for users | < 1 hour |
| P3 | Feature degraded, workaround exists | < 1 business day |

### Incident Response Steps

1. **Detect** — identify from monitoring alerts or user report
2. **Triage** — classify severity, identify scope
3. **Mitigate** — roll back if available; disable the feature if possible
4. **Fix** — hotfix process above
5. **Post-mortem** — written within 48 hours for P1/P2

### Post-Mortem Format (Required for P1 and P2)

```markdown
## Incident Post-Mortem: <Short Title>

**Date:** YYYY-MM-DD
**Severity:** P1 | P2
**Duration:** <how long production was impacted>

### What Happened
Brief timeline of events.

### Root Cause
The single underlying cause (not symptoms).

### Impact
What was broken. How many users/requests affected.

### Detection
How was the incident discovered? How long between impact and detection?

### Resolution
What fixed it?

### Prevention
What changes prevent recurrence?
- [ ] Action item (owner, due date)
```

---

## Observability

### Structured Logging with structlog

All log output is structured JSON. Never use `print()` or unstructured string interpolation in log calls.

```python
import structlog
log = structlog.get_logger()

# Good — structured, machine-parseable
log.info("request_completed", endpoint="/resources", status=200, duration_ms=42)
log.warning("upstream_timeout", service="payment-api", attempt=2)
log.error("database_connection_failed", host=settings.db_host, error=str(e))

# Bad — unstructured
print(f"Request completed in {duration}ms")
logging.info("Database error: " + str(e))
```

### Log Levels

| Level | Use for |
|-------|---------|
| `DEBUG` | Detailed diagnostics — disabled in production |
| `INFO` | Normal operations (request received, resource created) |
| `WARNING` | Unexpected but recoverable (upstream retry, validation rejection) |
| `ERROR` | Failures requiring attention (unhandled exception, dependency failure) |

Do not log at `INFO` on every request — use `DEBUG` for high-frequency events.

**Never log:** secrets, tokens, passwords, PII, raw user-provided content, or full external API responses.

### Correlation IDs

Every request carries a `correlation_id` that must propagate through the full request lifecycle:

- Generated at the API boundary if absent from request headers
- Bound to every log entry for the duration of the request via `structlog.contextvars`
- Returned in the `X-Correlation-ID` response header
- Included in API error response bodies so users can report it

```python
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", generate_id("req"))
    with structlog.contextvars.bound_contextvars(correlation_id=correlation_id):
        response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response
```

### Required Metrics

| Metric | Type | Labels |
|--------|------|--------|
| `requests_total` | Counter | `endpoint`, `method`, `status_code` |
| `request_duration_ms` | Histogram | `endpoint`, `method` |
| `errors_total` | Counter | `error_type`, `endpoint` |
| `external_calls_total` | Counter | `service`, `status` |
| `external_call_duration_ms` | Histogram | `service` |

Add domain-specific metrics as needed (e.g. `orders_created_total`, `reasoning_events_applied_total`).

Use Prometheus-compatible instrumentation (`prometheus-fastapi-instrumentator` or equivalent).

### Health Check Endpoint

```
GET /health
```

Returns `200` when healthy:
```json
{ "status": "ok", "database": "ok", "version": "1.4.2" }
```

Returns `503` when any critical dependency is unavailable:
```json
{ "status": "degraded", "database": "error", "version": "1.4.2" }
```

The health check must verify actual database connectivity — not just process liveness. Used by load balancers, deployment pipelines, and rollback automation.

---

## Security

### Secrets Management

- Never hard-code secrets, API keys, or passwords in source code
- **Python:** `pydantic-settings` (`BaseSettings`) loads from environment variables / `.env`
- **TypeScript:** SvelteKit `$env/static/private` for server-only secrets
- Never commit `.env`; always maintain `.env.example` with placeholder values
- Generate cryptographic secrets: `python -c "import secrets; print(secrets.token_hex(32))"`
- Run `uv run pip-audit` (Python) and `bun audit` (TypeScript) before every release

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # from config — never wildcard in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "X-Correlation-ID"],
)
```

Never use `allow_origins=["*"]` in production. Enumerate allowed origins explicitly per environment.

### Rate Limiting

Apply to all mutating endpoints and expensive read endpoints. Return `429 Too Many Requests` with a `Retry-After` header when exceeded.

### Input Validation

- All request bodies validated through Pydantic models — reject with `422` on failure
- All SQL queries use parameterized placeholders — never string interpolation
- Use `ConfigDict(extra='forbid')` on models receiving externally-sourced input (API requests, LLM output)

---

## Definition of Done

### Bug Fix

- [ ] Root cause identified and documented in the PR description
- [ ] Failing test added that reproduces the bug
- [ ] Fix applied — the failing test now passes
- [ ] No regressions — full test suite passes
- [ ] Lint and type checks pass

### Feature

- [ ] Unit tests for new business logic
- [ ] Integration tests for new API surface
- [ ] Lint and type checks pass
- [ ] PR description explains the feature and how it was tested
- [ ] No `any`, `@ts-ignore`, or `# type: ignore` introduced

### Refactor

- [ ] No behavioral change — proven by existing tests passing unchanged
- [ ] Coverage unchanged (no tests deleted to make the refactor pass)
- [ ] Lint and type checks pass
- [ ] PR description explains what structural problem was addressed

### Coverage Targets

| Area | Minimum |
|------|---------|
| Python application package | 80% |
| Core business logic / domain services | 90% |
| TypeScript `src/lib/` | 70% |

`mypy --strict` and `tsc --noEmit` must pass with zero errors. Do not reduce strictness to meet coverage targets — fix the types.
