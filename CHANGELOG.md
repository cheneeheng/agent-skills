# Changelog

Versions follow [Semantic Versioning](https://semver.org/).
Versions refer to the Marketplace versions.

---

## [2.4.0] — 2026-05-25

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.2 |
| `ceh-architecture-design` | v2.1.0 |
| `ceh-blog` | v1.0.0 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.4.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.2.0 |
| `ceh-release-ops` | v2.2.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.2.0 |

### Added

- **`ceh-blog` plugin (new, v1.0.0)** — interview-driven blog writing end-to-end:
  - `blog-interviewer`: structured interview skill to extract ideas, audience, and key points from the user.
  - `blog-writer`: drafts a full publication-ready blog post from interview output.
  - `blog-editor`: iterative editing pass — tone, clarity, and structure review.
  - `blog-repurpose`: repurposes a finished post for Twitter/X, LinkedIn, TL;DR, and newsletter formats.

### Changed

- **`ceh-agent-coding-contract`** (v2.2.2): Karpathy-derived rules added to the coding contract — opinionated heuristics on scope discipline, implementation order, and change minimalism.

---

## [2.3.0] — 2026-05-16

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.1 |
| `ceh-architecture-design` | v2.1.0 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.4.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.2.0 |
| `ceh-release-ops` | v2.2.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.2.0 |

### Added

- **`ceh-agent-coding-contract`** (v2.2.1): New `execution-modes` micro-skill extracted from references — covers interactive vs. autonomous mode rules and stop conditions.
- **`ceh-python-backend`** (v2.2.0): Four new micro-skills promoted from the former `python-backend` bundle:
  - `alembic`: Alembic migration setup, autogenerate, upgrade/downgrade workflow.
  - `asyncpg`: asyncpg query patterns, connection pool, and database reference (replaces `references/database.md`).
  - `python-environment`: uv environment setup, dependency management, and linting (ruff, mypy).
  - `python-observability`: structured logging, metrics, and health-check patterns.
  - `python-security`: secrets handling, CORS, rate limiting, and input validation.
- **`ceh-typescript-frontend`** (v2.2.0): New `environment` micro-skill covering Bun/Node setup, Vite config, and toolchain commands — extracted from the former `typescript-frontend` bundle.
- **Repo**: `scripts/sync-stubs.ps1` added — synchronises cross-plugin stub reference files in one pass.
- **Repo**: `CROSS_REFERENCES.md` added — tracks content duplicated across skills with canonical source and all copy locations.

### Changed

- **`ceh-agent-coding-contract`** (v2.2.1): All reference files (`core-rules.md`, `decision-log.md`, `execution-modes.md`, `non-goals.md`, `stop-conditions.md`, `task-workflow.md`) inlined into `agent-coding-contract/SKILL.md`; reference files removed. `implement-from-plan` and `review-against-plan` skills updated to inline their reference content.
- **`ceh-architecture-design`** (v2.1.0): Former `architecture-design` bundle skill and all its `references/` files removed. Content inlined into the existing micro-skills: `adr`, `domain-modeling`, `event-sourcing`, `llm-integration`, `postgresql`, `repository-structure`, `rest-api`.
- **`ceh-git-workflow`** (v2.4.0): Former `git-workflow` bundle skill and all its `references/` files removed. Content inlined into the existing micro-skills: `branch`, `code-review`, `commit`, `dependency-management`, `gitignore`, `hotfix`, `open-pr`, `release`. `merge` skill removed; merge strategy content consolidated into `open-pr`.
- **`ceh-python-backend`** (v2.2.0): Former `python-backend` bundle skill and all its `references/` files removed. Content distributed into `fastapi`, `python-testing`, and the four new micro-skills above. Agent descriptions trimmed (`python-integration-tester`, `python-system-tester`).
- **`ceh-release-ops`** (v2.2.1): Former `release-ops` bundle skill and all its `references/` files removed. Content inlined into existing micro-skills: `database-migrations`, `definition-of-done`, `incidents`, `observability`, `rollback`, `security`, `versioning`. Lifecycle phase labels added to micro-skill descriptions.
- **`ceh-typescript-frontend`** (v2.2.0): Former `typescript-frontend` bundle skill and all its `references/` files removed. Content inlined into existing micro-skills: `accessibility`, `coding-style`, `frontend-testing`, `linting`, `sveltekit`, plus new `environment`.
- **`ceh-git-workflow`** (v2.4.0): `readme-updater` agent — `maxTurns` tuned; `effort` field removed.
- **Repo**: `CLAUDE.md` updated — bundle/micro-skill distinction removed; versioning and plugin table updated to reflect new structure.
- **Repo**: All plugin `README.md` files updated to reflect bundle removal and current skill lists.
- **Repo**: `ceh-dev-tools/CHANGELOG.md` removed (stale, not maintained).

---

## [2.2.3] — 2026-05-14

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.1.2 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.3 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Added

- **`ceh-git-workflow`** (v2.2.3): Attribution footer guidance added to commit (`commits.md`) and PR (`pull-requests.md`) standards. Test-run delegation rule added to `task-workflow.md` — test execution should be handed off to background subagents (auto-triggered tester agents take precedence; `Agent(run_in_background=True)` as fallback).
- **Repo**: `LICENSE.md` added.

### Changed

- **`ceh-git-workflow`** (v2.2.3): `branch` skill inlines start-new-work commands, dropping the `workflows.md` pointer (~135 lines/invocation saved).
- **`ceh-agent-coding-contract`** (v2.1.2): `agent-coding-contract` skill trigger narrowed to explicit phrases only, removing broad auto-load on refactors and multi-file changes. `review-against-plan` skill drops §01/§03 audit rows and tightens wording (~10 lines/run saved).
- **Repo**: `CLAUDE.md` updated — "Adding an Agent" section added parallel to "Adding a Skill"; `ceh-dev-tools` flagged as agents-only in the Plugins table; cross-bundle stub check command narrowed to `skills/python-backend` path; versioning rules clarified (PATCH for updates, MINOR for new skills/agents).

---

## [2.2.2] — 2026-05-02

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.1.0 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.1 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Added

- **`ceh-agent-coding-contract`** (v2.1.0): Two new bundle skills for plan-driven development:
  - `implement-from-plan`: implements a SKELETON.md or ITER_NN.md planning document section by section, resolving iteration pointers and respecting scope boundaries.
  - `review-against-plan`: audits the codebase against a planning document, categorizes findings as Gap / Deviation / Error, fixes them in-line, and produces a Plan Compliance Report.
  - `plan-schema.md` reference: defines SKELETON and ITER frontmatter, section table (§01–§06), pointer rules, and resolution order.

---

## [2.2.1] — 2026-04-29

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.2 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.1 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Changed

- **`ceh-agent-coding-contract`** (v2.0.2): Added built-in tool guidance across reference files — `AskUserQuestion` in `core-rules.md` (ask-don't-guess rule), `execution-modes.md` (Interactive Mode stop), and `stop-conditions.md`; `TaskCreate`/`TaskUpdate` and `Agent` tool in `task-workflow.md` for subtask tracking and parallel execution.

- **`ceh-git-workflow`** (v2.2.1): Added tool guidance — `Read`/`Grep`/`Bash` for code inspection in `code-review.md`; `Bash` with `git diff main...HEAD` in `pull-requests.md` author self-review checklist; `Bash` for audit commands in `dependencies.md`.

- **`ceh-python-backend`** (v2.1.2): Added `Bash` tool notes to `environment.md` (command table), `linting.md` (pre-PR checks), `migrations.md` (alembic workflow), `testing.md` (coverage run), and `security.md` (`pip-audit`).

- **`ceh-typescript-frontend`** (v2.1.2): Added `Bash` tool notes to `environment.md` (command table) and `linting.md` (pre-PR checks).

- **`ceh-release-ops`** (v2.1.2): Added `Bash` tool notes to `migrations.md` (alembic commands), `versioning.md` (release checklist), `security.md` (audit commands), and `rollback.md` (rollback procedure).

### Fixed

- Removed stale `docs/claude_logs/LESSONS_LEARNED.md` session log.

---

## [2.2.0] — 2026-04-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.1 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.1 |
| `ceh-release-ops` | v2.1.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.1 |

### Changed

- **`ceh-dev-tools`** (v1.1.0):
  - `repo-tree-mapper` agent: defaults to running in background.

- **`ceh-git-workflow`** (v2.2.0):
  - `changelog-agent` agent: defaults to running in background.
  - `readme-updater` agent: defaults to running in background.

---

## [2.1.1] — 2026-04-26

### Fixed

- Added full list of agents to the readme.

---

## [2.1.0] — 2026-04-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.1 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.0.1 |
| `ceh-git-workflow` | v2.1.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.1 |
| `ceh-release-ops` | v2.1.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.1 |

### Added

- **`ceh-dev-tools` plugin (new, v1.0.1)** — developer productivity agents:
  - `repo-tree-mapper` agent: walks a repo and produces an annotated `REPO_MAP.md`; trimmed description ~50%, `maxTurns` 25 → 8.
  - `walk-repo.sh` script: git-aware directory walker (fixed non-portable `$skip && continue` → `[[ $skip == true ]] && continue`).
  - Registered in top-level `README.md`, `CLAUDE.md`, and `marketplace.json`.

- **`ceh-git-workflow`** (v2.1.0) — new agents and scripts:
  - `changelog-agent`: generates or updates `CHANGELOG.md` (Keep a Changelog + semver).
  - `readme-updater`: applies surgical README edits after feature changes.
  - `check-semver.py` script: validates all version headers in a changelog file.

- **`ceh-python-backend`** (v2.1.1) — new agents, scripts, and references:
  - `python-unit-tester`, `python-integration-tester`, `python-system-tester` agents.
  - `run-unit-tests.sh`, `run-integration-tests.sh`, `run-system-tests.sh` scripts (use `uv run pytest`).
  - `references/migrations.md`: Alembic setup, autogenerate, upgrade/downgrade, test DB management.

- **`ceh-typescript-frontend`** (v2.1.1) — new agents, scripts, and micro-skills:
  - `ts-unit-tester`, `ts-integration-tester`, `ts-system-tester` agents.
  - `detect-test-framework.sh`, `run-unit-tests.sh`, `run-integration-tests.sh`, `check-coverage.sh`, `run-e2e.sh` scripts.
  - `skills/linting/SKILL.md`: new micro-skill for ESLint/Prettier/svelte-check/tsc.
  - `skills/coding-style/SKILL.md`: new micro-skill for TypeScript type conventions and naming.
  - `references/accessibility.md`: expanded with ARIA patterns, focus management, keyboard nav, form labelling, and color contrast rules.

- **`ceh-release-ops`** (v2.1.1) — new agents, scripts, and micro-skills:
  - `github-actions`, `gitlab-ci` agents for creating, reviewing, and debugging CI pipelines.
  - `gh-detect-stack.sh`, `gh-scaffold.sh`, `gh-validate.sh`, `gh-analyze-failure.sh` scripts.
  - `gl-detect-stack.sh`, `gl-scaffold.sh`, `gl-validate.sh`, `gl-analyze-failure.sh` scripts.
  - `skills/versioning/SKILL.md`: micro-skill for version bumps and release tagging.
  - `skills/rollback/SKILL.md`: micro-skill for deployment health-check failures.

- **READMEs and CHANGELOGs** added to all plugins that were missing them (`ceh-agent-coding-contract`, `ceh-architecture-design`, `ceh-git-workflow`, `ceh-python-backend`, `ceh-release-ops`, `ceh-lessons-learned`, `ceh-summarize-chat`, `ceh-typescript-frontend`, `ceh-dev-tools`).

### Fixed

- **`ceh-agent-coding-contract`** (v2.0.1): merged `agent-role.md` into `core-rules.md`; updated `SKILL.md` to load all references (full contract, not selective).
- **`ceh-python-backend`**: `references/exceptions.md` — removed contradictory rule about route handlers converting domain exceptions; `references/coding-style.md` — replaced deprecated `asyncio.get_event_loop()` with `asyncio.get_running_loop()`; `references/security.md` — `uv run pip-audit` → `uvx pip-audit`; `references/testing.md` — added `system/` to test structure tree.
- **`ceh-typescript-frontend`**: `references/error-handling.md` — component example now uses `onSuccess` callback instead of writing `sessionStore` directly; removed `scripts/setup-test-db.sh` (Postgres setup does not belong in a frontend plugin).
- **`ceh-release-ops`**: `references/definition-of-done.md` — corrected core domain services coverage target from 90% → 95%, matching `ceh-python-backend/references/testing.md` and `ceh-git-workflow/references/ci.md`; trimmed `references/observability.md` (removed redundant bad-example block); synced `skills/python-backend/references/observability.md` stub.
- **`ceh-git-workflow`**: `references/workflows.md` — added `git push origin --delete <branch-name>` to the "After PR is merged" sequence.

### Changed

- Token optimizations across reference files (no content removed): `ceh-summarize-chat/SKILL.md`, `ceh-lessons-learned/SKILL.md`, `ceh-architecture-design/references/domain-modeling.md`, `ceh-architecture-design/references/postgresql.md`, `ceh-python-backend/references/database.md`, `ceh-release-ops/references/observability.md`, `ceh-python-backend/references/coding-style.md`, `ceh-python-backend/references/testing.md`; both database stubs kept in sync.

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
