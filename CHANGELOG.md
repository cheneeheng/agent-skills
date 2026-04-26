# Changelog

Versions follow [Semantic Versioning](https://semver.org/).
Versions refer to the Marketplace versions.

---

## [2.1.0] — 2026-04-25

### Added

- **`ceh-dev-tools` plugin (new, v1.0.0)** — developer productivity agents with no prior home:
  - `repo-tree-mapper` agent: walks a repo and produces an annotated, clickable `REPO_MAP.md`.
  - `walk-repo.sh` script: git-aware directory walker used by the agent.
  - `README.md`.

### Fixed

- **`ceh-python-backend`** (v2.1.0):
  - `references/exceptions.md`: removed contradictory rule "route handlers convert domain exceptions
    to HTTPException"; global exception handlers in `app/core/middleware.py` are now the stated
    pattern, consistent with `fastapi.md`.
  - `references/coding-style.md`: replaced deprecated `asyncio.get_event_loop()` with
    `asyncio.get_running_loop()` (Python 3.10+).
  - `references/testing.md`: added `system/` directory to the test structure tree.
  - `run-unit-tests.sh`, `run-integration-tests.sh`, `run-system-tests.sh`: replaced bare `pytest`
    calls with `uv run pytest`; replaced `pip install` error messages with `uv add --dev`.

- **`ceh-typescript-frontend`** (v2.2.0):
  - `references/error-handling.md`: component example now uses `onSuccess` callback instead of writing `sessionStore` directly, consistent with the SvelteKit convention.
  - `scripts/setup-test-db.sh`: removed — Postgres setup script does not belong in a frontend plugin.

### Changed

- **`ceh-git-workflow` agents** (v2.1.0):
  - `changelog-agent`: generates or updates `CHANGELOG.md` following Keep a Changelog + semver.
  - `readme-updater`: applies surgical README edits after significant feature changes.
  - `check-semver.py` script: validates all version headers in a changelog file.

- **`ceh-python-backend` agents** (v2.1.0):
  - `python-unit-tester`: writes isolated pytest unit tests with mocked dependencies.
  - `python-integration-tester`: writes pytest integration tests against real internal components.
  - `python-system-tester`: writes full-stack scenario tests with Docker Compose support.
  - `run-unit-tests.sh`, `run-integration-tests.sh`, `run-system-tests.sh` scripts.
  - Token optimizations: trimmed all three tester agents by 40–52% (removed redundant bash
    find/cat commands, duplicate pytest marker-registration sections, verbose step narration);
    hard rules and key process steps retained in full.

- **`ceh-typescript-frontend` agents** (v2.1.0):
  - `ts-unit-tester`: writes isolated Vitest/Jest/Mocha unit tests.
  - `ts-integration-tester`: writes in-process multi-module tests with supertest/testcontainers.
  - `ts-system-tester`: writes Playwright/Cypress E2E tests with compose stack management.
  - `detect-test-framework.sh`, `run-unit-tests.sh`, `run-integration-tests.sh`,
    `check-coverage.sh`, `run-e2e.sh`, `setup-test-db.sh` scripts.
  - `skills/linting/SKILL.md`: new micro-skill for ESLint/Prettier/svelte-check/tsc configuration.
  - `skills/coding-style/SKILL.md`: new micro-skill for TypeScript type conventions and naming.
  - `references/accessibility.md`: expanded with ARIA patterns, focus management, keyboard nav, form labelling, and color contrast rules.

- **`ceh-release-ops` agents** (v2.1.0):
  - `github-actions`: creates, reviews, and debugs GitHub Actions workflows.
  - `gitlab-ci`: creates, reviews, and debugs GitLab CI pipelines.
  - `gh-detect-stack.sh`, `gh-scaffold.sh`, `gh-validate.sh`, `gh-analyze-failure.sh` scripts.
  - `gl-detect-stack.sh`, `gl-scaffold.sh`, `gl-validate.sh`, `gl-analyze-failure.sh` scripts.
  - `skills/versioning/SKILL.md`: new micro-skill — triggers on version bumps, release tagging, and change classification.
  - `skills/rollback/SKILL.md`: new micro-skill — triggers on deployment health-check failures and post-deploy metric spikes.

### Fixed (2026-04-26)

- **`ceh-release-ops`**: `references/definition-of-done.md` — corrected core domain services coverage
  target from 90% → 95%, matching `ceh-python-backend/references/testing.md` and
  `ceh-git-workflow/references/ci.md`.
- **`ceh-git-workflow`**: `references/workflows.md` — added `git push origin --delete <branch-name>`
  to the "After PR is merged" sequence; `references/branching.md` states branches must be deleted
  after merge but the workflow only deleted locally.

### Changed (2026-04-26)

- Token optimizations across reference files (no content removed):
  - `ceh-summarize-chat/SKILL.md`: removed redundant Purpose section (duplicated frontmatter),
    merged Tone and Length into Writing Rules, removed `---` dividers.
  - `ceh-lessons-learned/SKILL.md`: removed four `---` section dividers.
  - `ceh-architecture-design/references/domain-modeling.md`: removed obvious docstring from
    `generate_id` example; shortened StrEnum/const assertion comments.
  - `ceh-architecture-design/references/postgresql.md`, `ceh-python-backend/references/database.md`,
    `ceh-release-ops/references/observability.md`, `ceh-python-backend/references/coding-style.md`,
    `ceh-python-backend/references/testing.md`: shortened verbose inline code example comments
    (`# Good — parameterized, safe` → `# good`; `# Bad — ...` → `# bad — ...`).
  - Both database stubs (`ceh-architecture-design/skills/python-backend/references/database.md`
    and `ceh-python-backend`) updated in sync.

---

## [2.0.0] — 2026-04-08 (all plugins)

### Changed

- **Breaking**: split the monolithic `ceh` plugin into 8 standalone plugins, one per domain:
  `ceh-agent-coding-contract`, `ceh-architecture-design`, `ceh-python-backend`,
  `ceh-typescript-frontend`, `ceh-git-workflow`, `ceh-release-ops`,
  `ceh-summarize-chat`, `ceh-lessons-learned`.
- Each bundle skill and its associated micro-skills now live in the same plugin. Skill invoke
  prefixes changed from `ceh:*` to `ceh-<plugin>:*` (e.g. `ceh:commit` → `ceh-git-workflow:commit`).
- Cross-bundle micro-skills (`postgresql`, `observability`, `security`) retain identical relative
  reference paths; foreign reference files are duplicated into the host plugin where needed.
- `marketplace.json` updated to list all 8 plugins; old `ceh` entry removed.

---

## [1.0.5] — 2026-04-06

### Fixed

- `lessons-learned` skill: clarified append instruction to always add new entries at the very end of `LESSONS_LEARNED.md`, never before the last existing entry.

---

## [1.0.4] — 2026-04-05

### Changed

- Standardised all Claude-generated log file paths to `docs/claude_logs/`: `LESSONS_LEARNED.md`, `DECISION_LOG.md` (referenced across `lessons-learned`, `agent-coding-contract`, `git-workflow`, and `release-ops` skills).
- Moved `ARCHITECTURE_DECISIONS.md` references out of `docs/claude_logs/` to `docs/adr/DECISIONS.md` — this file is shared developer documentation, not a Claude session artifact (`git-workflow/references/code-review.md`, `architecture-design/references/rest-api.md`).

---

## [1.0.3] — 2026-04-03

### Added

7 micro-skills extracted from `git-workflow` for fine-grained auto-triggering on individual
git operations.

| Micro-skill | Sources | Auto-triggers when |
|---|---|---|
| `branch` | git-workflow/branching + workflows | Creating or naming a branch |
| `commit` | git-workflow/commits + workflows | Writing a commit message or staging changes |
| `open-pr` | git-workflow/pull-requests + workflows | Opening a pull request or writing a PR description |
| `merge` | git-workflow/merging | Merging a branch or choosing a merge strategy |
| `hotfix` | git-workflow/workflows + releases | Executing a critical production fix |
| `release` | git-workflow/releases + workflows | Tagging a release or bumping a version |
| `gitignore` | git-workflow/gitignore | Creating or editing a `.gitignore` file |

---

## [1.0.2] — 2026-04-01

### Added

18 micro-skills for precise auto-triggering. Each is a thin skill that points to the relevant
reference file(s) already defined in the bundle skills — no content duplication.

| Micro-skill | Sources | Auto-triggers when |
|---|---|---|
| `adr` | architecture-design/adrs | Making significant design decisions |
| `domain-modeling` | architecture-design/domain-modeling | Designing entities, IDs, status fields |
| `event-sourcing` | architecture-design/event-sourcing | Working with event log or state snapshots |
| `rest-api` | architecture-design/rest-api | Building endpoints, choosing HTTP codes |
| `postgresql` | architecture-design/postgresql + python-backend/database | Writing SQL, asyncpg queries, schema changes |
| `llm-integration` | architecture-design/llm-integration | Integrating LLM calls or handling output |
| `fastapi` | python-backend/fastapi + python-backend/exceptions | Writing route handlers, DI, exception hierarchy |
| `python-testing` | python-backend/testing | Writing Python tests |
| `sveltekit` | typescript-frontend/sveltekit + typescript-frontend/error-handling | Routes, stores, components, API client |
| `frontend-testing` | typescript-frontend/testing | Writing frontend tests |
| `accessibility` | typescript-frontend/accessibility | Writing Svelte component markup |
| `observability` | python-backend/observability + release-ops/observability | Logging, metrics, health checks |
| `database-migrations` | release-ops/migrations | Writing or running Alembic migrations |
| `incidents` | release-ops/incidents + release-ops/hotfix | Production incidents, post-mortems |
| `definition-of-done` | release-ops/definition-of-done | Preparing to open a PR |
| `security` | python-backend/security + release-ops/security | Secrets, CORS, rate limiting, input validation |
| `code-review` | git-workflow/code-review | Reviewing PRs, leaving review comments |
| `dependency-management` | git-workflow/dependencies | Adding or upgrading packages |

---

## [1.0.1] — 2026-04-01

### Changed

- Refactored `agent-coding-contract`, `architecture-design`, `python-backend`, `typescript-frontend`, and `release-ops` skills: replaced long, keyword-stuffed `SKILL.md` titles with a short title and a summary paragraph, and moved all detailed content into topic-specific files under a `references/` folder — matching the pattern established by `git-workflow`.
- Updated `summarize-chat` skill: replaced the verbose title with a short title and summary paragraph (no reference files needed).

### Reference files added

| Skill | New reference files |
|-------|-------------------|
| `agent-coding-contract` | agent-role, core-rules, decision-log, execution-modes, non-goals, stop-conditions, task-workflow |
| `architecture-design` | adrs, domain-modeling, event-sourcing, llm-integration, postgresql, repository-structure, rest-api |
| `python-backend` | coding-style, database, environment, exceptions, fastapi, linting, observability, security, testing |
| `release-ops` | definition-of-done, hotfix, incidents, migrations, observability, rollback, security, versioning |
| `typescript-frontend` | accessibility, coding-style, environment, error-handling, linting, sveltekit, testing |

---

## [1.0.0] — 2026-03-31

### Added

- Initial release of the `ceh` plugin.
- Skills: `agent-coding-contract`, `architecture-design`, `git-workflow`, `lessons-learned`, `python-backend`, `release-ops`, `summarize-chat`, `typescript-frontend`.
- `git-workflow` ships with reference files: branching, ci, code-review, commits, dependencies, gitignore, merging, pull-requests, releases, workflows.
- `LESSONS_LEARNED.md` for capturing session retrospectives.
- `marketplace.json` for plugin discovery.
