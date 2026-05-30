# Cross-Reference Map

Tracks content duplicated word-for-word across multiple skills. When editing any entry,
update **all listed files**. Each block is intentionally inlined (zero file reads at runtime);
this map exists so edits don't get lost.

---

## Observability (structlog, log levels, correlation IDs)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-release-ops/skills/observability/SKILL.md` | entire file | canonical — most complete |
| `ceh-python-backend/skills/python-observability/SKILL.md` | entire file | subset — no correlation ID middleware code, no metrics table, no health check |

**What is shared:** structlog import pattern, log level table (`DEBUG`/`INFO`/`WARNING`/`ERROR`), never-log list (secrets/tokens/PII), correlation ID bullet list.

**What diverges:**
- `python-backend` adds "Do not log at `INFO` on every request" note; omits metrics and health check.

---

## Security (secrets, CORS, rate limiting, input validation)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-release-ops/skills/security/SKILL.md` | entire file | canonical — most complete |
| `ceh-python-backend/skills/python-security/SKILL.md` | entire file | subset — no CORS code block, no TypeScript secrets path; has session token line |

**What is shared:** never hard-code secrets, `pydantic-settings` for Python, `.env` not committed, pip-audit before release, CORS no wildcard in production, rate limiting on mutation endpoints, parameterized SQL, `ConfigDict(extra='forbid')` on external-input models.

**What diverges:**
- `python-backend` adds `Apply rate limiting per session (e.g. 10 req/min)` and `secrets.token_urlsafe(32)` detail; has no CORS code example; uses `uvx pip-audit` (vs `uv run pip-audit` in canonical).
- `security` micro-skill is the superset: both Python and TypeScript, session tokens, `secrets.token_hex(32)` generation command, rate-limiting detail.

---

## Database / asyncpg patterns (transactions, connection pool, migrations)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-architecture-design/skills/postgresql/SKILL.md` | entire file | canonical — schema design + tenant isolation + full asyncpg patterns |
| `ceh-python-backend/skills/asyncpg/SKILL.md` | entire file | identical transaction and pool code |
| `ceh-python-backend/skills/alembic/SKILL.md` | entire file | adds full Alembic CLI and `env.py` config |
| `ceh-release-ops/skills/database-migrations/SKILL.md` | "Safety Rules" + "Two-Step Destructive Changes" sections | superset of migration rules — adds blue-green safe, testing against prod copy, SQL examples |

**What is shared (word-for-word identical):** atomic transaction code block (`pool.acquire` + `conn.transaction()` with `executemany` + `execute`), connection pool creation call (`min_size=5, max_size=20, command_timeout=30`), migration safety rules (backward-compatible, two-step destructive, never simultaneous deploy).

**What diverges:**
- `postgresql` adds schema design template, `TIMESTAMPTZ` / `JSONB` rules, tenant isolation pattern, index examples.
- `asyncpg` adds "Create the pool in the FastAPI lifespan function and expose it via `app.state.db_pool`" guidance.
- `alembic` adds full Alembic CLI commands, `alembic/env.py` `sync_url` workaround, "apply before integration tests" command.
- `database-migrations` is the most comprehensive on migration rules: blue-green deploy safety, test against production data copy, concrete SQL for two-step pattern.

---

## Semantic Versioning (MAJOR/MINOR/PATCH table)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/release/SKILL.md` | "Tags follow semver" section | canonical |
| `ceh-release-ops/skills/versioning/SKILL.md` | "Semantic Versioning" section | near-identical table; adds version file locations and release checklist |

**What is shared:** three-row table mapping change type → version bump (`MAJOR` breaking, `MINOR` new backward-compatible feature, `PATCH` fixes/chores/docs/refactors), "when in doubt bump PATCH" rule.

**What diverges:**
- `versioning` adds: version recorded in both `pyproject.toml` and `package.json`; full release checklist; "BREAKING CHANGE: footer or `!` type" phrasing.
- `release` focuses on git tag commands; semver table is a reference sidebar.

---

## API Error Response Shape

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-architecture-design/skills/rest-api/SKILL.md` | "Error Response Shape" section | canonical — full JSON structure with field docs |
| `ceh-python-backend/skills/fastapi/SKILL.md` | "Global Exception Handlers" section | implementation — maps exceptions to `JSONResponse` using the same shape |

**What is shared:** `code` and `message` fields in the error response body; same JSON shape consumed by both spec and implementation.

**What diverges:**
- `rest-api` documents the full JSON contract including `correlation_id` field and an example payload.
- `fastapi` shows only the Python handler code returning `code`/`message`; does not include `correlation_id` in the handler or repeat the full field documentation.

---

## Hotfix Workflow (branch naming, scope, process steps)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/hotfix/SKILL.md` | entire file | canonical — full guide with bash commands |
| `ceh-release-ops/skills/incidents/SKILL.md` | "Hotfix Process" section | subset — same 7 steps, no bash commands |

**What is shared:** 7-step process: branch `fix/critical-<description>` from `main`, minimal scope, 1-approval review, CI must pass, squash merge to `main`, bump PATCH + tag, staging → production deploy.

**What diverges:**
- `hotfix` is standalone with full bash command examples for each step.
- `incidents` summarises the same steps as a sub-section with no commands.

---

## PR Checklist Items

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/open-pr/SKILL.md` | two "Checklist" blocks — the rendered template (after the body) and the `gh pr create` heredoc | canonical — only holder; the six items appear twice in this one file |

**What is shared:** six checklist items, repeated word-for-word in both "Checklist" blocks inside `open-pr`: "All CI checks pass", "Tests added or updated", "No `any` / `@ts-ignore` / `# type: ignore` introduced", "No secrets or credentials in code", "Migrations (if any) are backward-compatible", "DECISIONS.md updated (if a durable decision was made)".

**What diverges:**
- The two `open-pr` blocks are not identical: the first (rendered template) reads "Tests added or updated **for new behavior**" and adds an "Attribution included if AI tooling assisted" item; the second (heredoc) reads plain "Tests added or updated" and omits the attribution item. Keep the six shared items in sync across both blocks when editing.
- `ceh-release-ops/skills/definition-of-done/SKILL.md` **no longer carries these six items.** It was rewritten into Bug Fix / Feature / Refactor sections with category-specific criteria that do not overlap word-for-word with this list, so it is no longer part of this block.

---

## Coverage Targets (test coverage minimum percentages)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-release-ops/skills/definition-of-done/SKILL.md` | "Coverage Targets" section | canonical |
| `ceh-python-backend/skills/python-testing/SKILL.md` | coverage section | same two thresholds, but row labels have drifted out of sync (see below) |

**What is shared (same thresholds, wording now DIVERGED):** two rows mapping the same areas to the same percentages — application package → 80%, core business logic → 95%. The labels are no longer word-for-word identical:
- `definition-of-done`: `Python application package | 80%`, `Core business logic / domain services | 95%`.
- `python-testing`: `Overall \`app/\` package | 80%`, `Core business logic services | 95%`.

**What diverges:**
- `definition-of-done` has three rows (adds `TypeScript \`src/lib/\` | 70%`), a `mypy --strict` / `tsc --noEmit` note, and no pytest command.
- `python-testing` has two rows (omits the TypeScript row) and adds the pytest command to run coverage checks.
- Label drift: `definition-of-done` was reworded ("Python application package", "Core business logic / domain services") but `python-testing` still uses the older labels. Re-sync the two row labels, or treat this entry as intentionally divergent.

---

## Alembic CLI Commands

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-python-backend/skills/alembic/SKILL.md` | command reference section | canonical — setup + full command list + rules |
| `ceh-release-ops/skills/database-migrations/SKILL.md` | operational command reference | subset — same four commands, ops context |

**What is shared:** four commands word-for-word: `uv run alembic upgrade head`, `uv run alembic downgrade -1`, `uv run alembic current`, `uv run alembic history`.

**What diverges:**
- `alembic` adds: setup steps, `env.py` `sync_url` workaround, full rules (downgrade reversibility, never edit applied migrations).
- `database-migrations` is operations-focused (Safety Rules, Two-Step Destructive Changes); commands appear as quick-reference only.

---

## Update Protocol

When changing a shared block:
1. Find the canonical file (marked above).
2. Edit it first — that's the source of truth for the rule.
3. Propagate the change to every other listed file in the same commit.
4. Update this file if the scope of sharing changes.
