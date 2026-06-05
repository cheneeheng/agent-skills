# ceh-release-ops

Release and operations engineering standards for the full deployment lifecycle. Covers semantic
versioning, database migration safety, rollback procedures, incident response, observability,
security baseline, definition of done, and CI/CD pipeline automation via GitHub Actions and
GitLab CI agents.

## Skills (Auto-Load)

| Skill | Phase | Triggers When |
|-------|-------|---------------|
| `observability` | implementation | Writing structured log calls, adding Prometheus metrics, touching the /health endpoint |
| `database-migrations` | implementation | Creating or modifying an Alembic migration, planning a column drop or rename |
| `definition-of-done` | implementation | Opening a pull request or marking a task complete — verifies bug fix/feature/refactor quality bar |
| `security` | implementation | Handling secrets, configuring CORS, writing rate limiting, reviewing input validation |
| `versioning` | release | Bumping a version in pyproject.toml or package.json, applying a git tag, classifying a change |
| `incidents` | operational | Responding to a production incident, classifying P1/P2/P3, writing a post-mortem, creating a hotfix branch |
| `rollback` | operational | Deployment fails health check, error rates spike post-deploy, data integrity issue detected |

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

