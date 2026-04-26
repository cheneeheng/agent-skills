# ceh-release-ops

Release and operations engineering standards for the full deployment lifecycle. Covers semantic
versioning, database migration safety, rollback procedures, incident response, observability,
security baseline, definition of done, and CI/CD pipeline automation via GitHub Actions and
GitLab CI agents.

## Bundle Skills

| Skill | Invoke | Description |
|-------|--------|-------------|
| `release-ops` | `/release-ops` | Full release and ops lifecycle — load when touching deployments, migrations, incidents, logging, metrics, or security config |

## Micro-Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `versioning` | Bumping a version in pyproject.toml or package.json, applying a git tag, classifying a change |
| `database-migrations` | Creating or modifying an Alembic migration, planning a column drop or rename |
| `rollback` | Deployment fails health check, error rates spike post-deploy, data integrity issue detected |
| `incidents` | Responding to a production incident, classifying P1/P2/P3, writing a post-mortem, creating a hotfix branch |
| `observability` | Writing structured log calls, adding Prometheus metrics, touching the /health endpoint |
| `security` | Handling secrets, configuring CORS, writing rate limiting, reviewing input validation |
| `definition-of-done` | Opening a pull request or marking a task complete — verifies bug fix/feature/refactor quality bar |

## Agents

| Agent | When to Use |
|-------|-------------|
| `github-actions` | Create, review, debug, or optimize GitHub Actions workflows in `.github/workflows/` |
| `gitlab-ci` | Create, review, debug, or optimize GitLab CI pipelines in `.gitlab-ci.yml` |

## Scripts

All scripts live in `scripts/`. Used by the CI agents — also callable directly.

| Script | Usage |
|--------|-------|
| `gh-detect-stack.sh` | Identify project stack and existing GitHub workflows |
| `gh-scaffold.sh <stack>` | Emit a starter workflow for node, python-uv, python, go, rust, generic |
| `gh-validate.sh <file>` | YAML lint + actionlint (if installed) |
| `gh-analyze-failure.sh <logfile>` | Extract the first failure signal from a GitHub Actions log |
| `gl-detect-stack.sh` | Identify project stack and existing GitLab CI config |
| `gl-scaffold.sh <stack>` | Emit a starter `.gitlab-ci.yml` for common stacks |
| `gl-validate.sh <file>` | YAML lint + glab ci lint (if installed) |
| `gl-analyze-failure.sh <logfile>` | Extract the first failure signal from a GitLab job log |

## Reference Files

All primary reference files live under `skills/release-ops/references/`:

| File | Topic |
|------|-------|
| `versioning.md` | SemVer rules, 10-step release checklist, change classification |
| `migrations.md` | Alembic commands, migration safety rules, two-step destructive changes |
| `rollback.md` | Rollback triggers, application rollback procedure, database rollback considerations |
| `hotfix.md` | Hotfix branch, minimal scope, CI requirements, abbreviated deploy steps |
| `incidents.md` | P1/P2/P3 severity levels, five-step response, post-mortem format |
| `observability.md` | structlog levels, correlation ID middleware, required Prometheus metrics, health check contract |
| `security.md` | Secrets management, CORS config, rate limiting, input validation |
| `definition-of-done.md` | Done criteria for bug fixes, features, refactors; coverage targets |

Python-specific supplementary references live under `skills/python-backend/references/` (stubs
synced from `ceh-python-backend`):

| File | Topic |
|------|-------|
| `observability.md` | Python structlog examples, log level table, correlation ID, never-log rules |
| `security.md` | Session token format, LLM output validation, per-session rate limit |
