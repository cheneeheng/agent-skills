# Cross-Reference Map

Tracks content duplicated word-for-word across multiple skills. When editing any entry,
update **all listed files**. Each block is intentionally inlined (zero file reads at runtime);
this map exists so edits don't get lost.

---

## Layer boundaries (route → service → db)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-architecture/skills/domain-modeling/SKILL.md` | "Layer Boundaries" section | canonical — the always-on invariant (also injected by the architecture SessionStart hook) |
| `ceh-scaffolding/skills/scaffold-python-service/SKILL.md` | "Hard Layer Rules" section | restates the same rules at scaffold time |

**What is shared:** route handlers contain no business logic (call services); services contain no SQL (call the db layer); the db layer contains no business logic; one mutation path per aggregate.

**What diverges:**
- `domain-modeling` frames it as a design-time invariant and notes the concrete directory layout lives in `ceh-scaffolding`.
- `scaffold-python-service` lists the rules alongside the initial backend directory tree.

---

## asyncpg connection pool + transaction code

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-python-service/skills/asyncpg/SKILL.md` | "Atomic Transactions" + "Connection Pool" | canonical — full transaction and pool code |
| `ceh-python-service/skills/fastapi/SKILL.md` | lifespan / pool setup | same `asyncpg.create_pool(...)` call |

**What is shared:** `asyncpg.create_pool(min_size=5, max_size=20, command_timeout=30)` call; the atomic transaction pattern (`pool.acquire` + `conn.transaction()`).

---

## Hotfix Workflow (branch naming, scope, process steps)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/hotfix/SKILL.md` | entire file | canonical — full guide with bash commands |
| `ceh-ops/skills/incidents/SKILL.md` | "Hotfix Process" section | subset — same 7 steps, no bash commands |

**What is shared:** 7-step process: branch `fix/critical-<description>` from `main`, minimal scope, 1-approval review, CI must pass, merge commit to `main`, bump PATCH + tag, staging → production deploy.

**What diverges:**
- `hotfix` is standalone with full bash command examples for each step.
- `incidents` summarises the same steps as a sub-section with no commands.

---

## PR Checklist Items

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/open-pr/SKILL.md` | two "Checklist" blocks — the rendered template (after the body) and the `gh pr create` heredoc | canonical — only holder; the seven items appear twice in this one file |

**What is shared:** seven checklist items, repeated word-for-word in both "Checklist" blocks inside `open-pr`: "All CI checks pass", "Tests added or updated for new behavior", "No `any` / `@ts-ignore` / `# type: ignore` introduced", "No secrets or credentials in code", "Migrations (if any) are backward-compatible", "docs/adr/DECISIONS.md updated (if a durable decision was made)", "Attribution included if AI tooling assisted".

**What diverges:**
- The two `open-pr` blocks are identical — keep them in sync when editing.

---

## Coverage Targets (test coverage minimum percentages)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/open-pr/SKILL.md` | "Coverage Targets" section (under Definition of Done) | canonical — three rows incl. TypeScript |
| `ceh-python-service/skills/python-testing/SKILL.md` | coverage section | two Python thresholds with identical row labels |
| `ceh-python-library/skills/python-testing/SKILL.md` | coverage section | two Python thresholds with identical row labels |

**What is shared (identical labels and thresholds):** two rows, word-for-word — `Python application package | 80%`, `Core business logic / domain services | 95%`.

**What diverges:**
- `open-pr` adds a third row (`TypeScript src/lib/ | 70%`) and the `mypy --strict` / `tsc --noEmit` note.
- both `python-testing` copies omit the TypeScript row and add a pytest `--cov` command (`--cov=app` for the service, `--cov=your_library` for the library).

---

## Python environment foundation (uv / ruff / mypy + style)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-python-service/skills/python-environment/SKILL.md` | entire file | service copy — web-service deps + uvicorn dev server |
| `ceh-python-library/skills/python-environment/SKILL.md` | entire file | library copy — no web deps, no uvicorn dev server |

**What is shared:** Python 3.12 + uv + `pyproject.toml`/`uv.lock` workflow, the uv command table, the ruff (line-length 88, `select = [E,F,I,UP,N,B]`) + mypy (`strict = true`) + pytest (`asyncio_mode = "auto"`) config, the coding-style rules (type hints, built-in generics, no `Any` without comment), naming table, three-group imports, and the "ruff only / no `# type: ignore` without comment" linting rules.

**What diverges (per the Shared-Standards Duplication Policy):**
- library copy drops `fastapi`/`uvicorn[standard]`/`asyncpg` from the deps example and the uvicorn dev-server command; sets `dependencies = []` and `known-first-party` to the library package; uses a library-flavored docstring example.

---

## Python testing foundation (pytest core)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-python-service/skills/python-testing/SKILL.md` | entire file | service copy — real DB / HTTP integration |
| `ceh-python-library/skills/python-testing/SKILL.md` | entire file | library copy — public-API tests, no DB/HTTP |

**What is shared:** pytest + pytest-asyncio (`asyncio_mode = "auto"`), `tests/unit/` structure, `test_<what>_<expected_behavior>.py` naming, one-behavior-per-test rule, mocking rules (mock external boundaries, `unittest.mock`/`pytest-mock`), and the Coverage Targets block (see above).

**What diverges:**
- service copy adds `httpx.AsyncClient`/FastAPI `TestClient`, a real-database integration tier, and a system tier.
- library copy replaces those with an `api/` tier that imports the package as a consumer and tests the public surface; no real DB/HTTP.

---

## .gitignore entries (per project type)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-scaffolding/skills/scaffold-python-service/SKILL.md` | ".gitignore" block | Python entries |
| `ceh-scaffolding/skills/scaffold-python-library/SKILL.md` | ".gitignore" block | Python entries |
| `ceh-scaffolding/skills/scaffold-web-frontend/SKILL.md` | ".gitignore" block | Node/frontend entries |
| `ceh-scaffolding/skills/scaffold-fullstack-web/SKILL.md` | "Combined .gitignore" block | union of both |

**What is shared:** the standard ignore fragments — Python (`.venv/`, `__pycache__/`, `*.pyc`, `*.egg-info/`, `.coverage`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`), Node (`node_modules/`, `.svelte-kit/`), build output (`dist/`, `build/`), secrets (`.env`, `.env.*`, `!.env.example`), and `.DS_Store`. When a fragment changes, update every scaffold skill that carries it.

**What diverges:**
- Python scaffolds carry only the Python + secrets + OS fragments (the service adds `*.db`); the frontend scaffold carries only the Node + secrets + OS fragments; the fullstack scaffold carries the union under labeled comment groups.

---

## Update Protocol

When changing a shared block:
1. Find the canonical file (marked above).
2. Edit it first — that's the source of truth for the rule.
3. Propagate the change to every other listed file in the same commit.
4. Update this file if the scope of sharing changes.
