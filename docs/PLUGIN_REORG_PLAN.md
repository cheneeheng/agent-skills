# Plugin Reorganization Migration Plan

Status: proposed (not yet executed)
Author: reorg triage session, 2026-06-04
Scope: all `ceh-*` plugins and skills in this repo

---

## 1. Why

Two independent problems, conflated in the current layout:

- **Problem A — triggering & redundancy.** Skills fire on *verbs/moments* ("I'm about to
  commit", "I'm writing a post"), not *nouns/topics* ("PostgreSQL", "FastAPI"). Topic-named
  skills either never auto-trigger or restate knowledge the model already has. The fix is
  per-skill: cut generic content to the repo-opinionated delta, and reframe surviving topics as
  moments.
- **Problem B — organizing axis.** Plugins are split on two incompatible axes at once:
  **tech domain** (`python-backend`, `typescript-frontend`, `architecture-design`) and
  **lifecycle phase** (`release-ops`). Both bake in a fullstack-web assumption, don't
  self-document their scope, and — critically — force the *same standard* into multiple plugins
  where copies drift. The fix is structural: reorganize around **use case**.

Reorganizing without trimming just relocates dead weight. Do **A and B together, A first.**

### Evidence: the duplication the current axis forces

`release-ops` was carved by lifecycle phase, but "phase" cuts across the same topics the stack
plugins already own. Verified content overlaps:

| Topic | Copy A | Copy B | Reality after reading both |
|---|---|---|---|
| Security baseline | `python-backend/python-security` | `release-ops/security` | B is the richer superset (covers Python **and** TS) |
| Observability | `python-backend/python-observability` | `release-ops/observability` | B is the superset (adds metrics + `/health`) |
| DB migrations | `python-backend/alembic` | `release-ops/database-migrations` | **Not** dupes: A = tool mechanics, B = deploy safety; overlap only on the command block |
| Versioning | `git-workflow/release` | `release-ops/versioning` | **Not** dupes: A = git tagging, B = full deploy pipeline |
| PR completion | `git-workflow/open-pr` | `release-ops/definition-of-done` | Overlap on the pre-PR quality gate |
| Hotfix | `git-workflow/hotfix` | `release-ops/incidents` | A = git mechanics, B = incident response |
| API design vs impl | `architecture-design/rest-api` | `python-backend/fastapi` | Complementary; already cross-reference each other |

After dedupe, `release-ops` has only two skills genuinely its own (`incidents`, `rollback`) —
confirming the axis was wrong.

### Evidence: app-specific leaks masquerading as standards

`architecture-design/event-sourcing` and `architecture-design/llm-integration` are bound to one
specific application (the `event_log`/`entities` schema and the "LLM proposes events → backend
validates" pattern). They are not reusable standards — together they are a single niche use case.

---

## 2. Target architecture

Three tiers on a single coherent axis. Plugin names declare their scope, which removes the silent
"fullstack-web-only" assumption and makes the Python-library gap an obvious empty slot.

```
Tier 1 — cross-cutting (load most sessions)
  ceh-agent-coding-contract     contract + plan implement/review
  ceh-git-workflow              branch, commit, open-pr, code-review, release, hotfix,
                                dependency-management, gitignore

Tier 2 — use-case workflow (load per activity)
  ceh-blog                      (unchanged — the reference design)
  ceh-documentation             user/operator guides + changelog/readme agents
  ceh-ops                       (rename of release-ops) incidents, rollback, deploy + CI agents
  ceh-session-utils             (optional merge) summarize-chat + lessons-learned

Tier 3 — stack/build (load per project type)
  ceh-python-service            (rename of python-backend) FastAPI/asyncpg/migrations/web service
  ceh-python-library            (NEW) packaging, public API, semver, no web deps
  ceh-web-frontend              (rename of typescript-frontend) SvelteKit/a11y/Vitest
  ceh-architecture              (rename of architecture-design) stack-agnostic design moments

Optional / niche
  ceh-llm-event-backend         event-sourcing + llm-integration (extracted) — or delete
  ceh-dev-tools                 (unchanged) repo-tree-mapper agent
```

Net: 11 plugins → ~9 (+1 optional). ~46 skills → ~30 after merges/deletes.

---

## 3. Per-skill migration map

Verdict legend: **KEEP** (well-formed, leave) · **TRIM** (cut generic → delta) ·
**MOMENTIZE** (reframe topic→verb trigger) · **MERGE** (fold into another skill) ·
**MOVE** (relocate, content largely intact) · **DELETE/EXTRACT** (remove or pull into niche
plugin). "✓ read" = content verified this session; "desc" = verdict from description, confirm at
execution.

### ceh-agent-coding-contract (T1, keep)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| agent-coding-contract | moment | KEEP (desc) | unchanged |
| implement-from-plan | moment | KEEP (desc) | unchanged |
| review-against-plan | moment | KEEP (desc) | unchanged |

### ceh-git-workflow (T1, keep — absorbs dedupes)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| branch, commit, code-review | moment | KEEP (desc) | unchanged |
| open-pr | moment | KEEP + absorb `definition-of-done` quality gate ✓ | unchanged |
| release | moment | KEEP — git tagging mechanics only; dedupe semver table vs `versioning` ✓ | unchanged |
| hotfix | moment | KEEP — git mechanics; `incidents` references it ✓ | unchanged |
| dependency-management | moment | KEEP (desc) | unchanged |
| gitignore | file-edit | KEEP — small but complete, triggers reliably ✓ | unchanged (or MOVE to stack env skills) |

### ceh-architecture-design → ceh-architecture (T3)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| adr | moment | KEEP (desc) | ceh-architecture (or ceh-documentation — it's a doc artifact) |
| domain-modeling | moment | TRIM, keep ID-format/status-enum opinions (desc) | ceh-architecture |
| repository-structure | rare moment | TRIM; split python bits → service, frontend bits → web (desc) | ceh-architecture |
| rest-api | moment | MOVE + co-locate with fastapi (kills cross-plugin ref) ✓ | ceh-python-service |
| postgresql | topic | TRIM + MERGE into data moments (`domain-modeling` + migrations) (desc) | ceh-python-service |
| event-sourcing | — | EXTRACT to ceh-llm-event-backend, or DELETE ✓ | niche / removed |
| llm-integration | — | EXTRACT to ceh-llm-event-backend, or DELETE (overlaps built-in `claude-api`) ✓ | niche / removed |

### ceh-python-backend → ceh-python-service (T3)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| fastapi | moment | TRIM + absorb `rest-api` design rules ✓ | ceh-python-service |
| asyncpg | moment | TRIM + absorb `postgresql` driver rules (desc) | ceh-python-service |
| alembic | moment | KEEP as single migrations home; absorb deploy-safety from `database-migrations`, drop `event_log` lines ✓ | ceh-python-service |
| python-observability | import | MERGE — adopt richer `release-ops/observability` content ✓ | ceh-python-service |
| python-security | moment | MERGE — adopt richer `release-ops/security`; TS secret line → web-frontend ✓ | ceh-python-service |
| python-environment | file-edit | TRIM web specifics; **duplicate into python-library** (see §4) ✓ | ceh-python-service + ceh-python-library |
| python-testing | file-edit | KEEP; **duplicate into python-library** (desc) | ceh-python-service + ceh-python-library |

### ceh-python-library (NEW, T3)
| Source | Verdict |
|---|---|
| python-environment (trimmed: no fastapi/uvicorn/asyncpg deps, no uvicorn dev server) | duplicate-and-trim |
| python-testing | duplicate |
| NEW: public API surface, semver discipline, packaging/publishing (build backend, wheels), no-web-deps rule | author fresh |

### ceh-typescript-frontend → ceh-web-frontend (T3)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| sveltekit | file-edit | TRIM (desc) | ceh-web-frontend |
| accessibility | file-edit | KEEP — real opinionated value (desc) | ceh-web-frontend |
| frontend-testing | file-edit | TRIM (desc) | ceh-web-frontend |
| environment | moment | KEEP — consolidation target (mirror python-environment's all-in-one shape) ✓ | ceh-web-frontend |
| coding-style | topic | KEEP content (real delta), MOMENTIZE — MERGE into `environment`/`sveltekit` so it fires on file edits ✓ | ceh-web-frontend |
| linting | topic | MERGE into `environment` (mostly a quality gate + config) ✓ | ceh-web-frontend |

> Normalization note: Python folds env+style+linting into one `python-environment`; TS splits the
> same into three. Consolidate TS to match — fewer, file-triggered skills.

### ceh-release-ops → ceh-ops (T2)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| incidents | moment | KEEP (desc) | ceh-ops |
| rollback | moment | KEEP (desc) | ceh-ops |
| versioning | moment | SPLIT: deploy pipeline (changelog→docker→staging→prod→health) stays as `deploy`; semver table dedupes against git-workflow/release ✓ | ceh-ops |
| security | moment | MERGE → python-service (richer copy wins) ✓ | removed from ops |
| observability | moment | MERGE → python-service (richer copy wins) ✓ | removed from ops |
| database-migrations | moment | MERGE → python-service/alembic ✓ | removed from ops |
| definition-of-done | moment | MERGE → git-workflow/open-pr ✓ | removed from ops |

### Unchanged use-case plugins (T2)
| Plugin | Verdict |
|---|---|
| ceh-blog (4 skills) | KEEP — reference design; rewrite other plugins' descriptions to this standard |
| ceh-documentation (user-operator-guide + changelog/readme agents) | KEEP |
| ceh-summarize-chat, ceh-lessons-learned | KEEP; optional MERGE into ceh-session-utils |
| ceh-dev-tools (repo-tree-mapper) | KEEP |

### Agents
| Agent | Target |
|---|---|
| python-{unit,integration,system}-tester | ceh-python-service (share with library) |
| ts-{unit,integration,system}-tester | ceh-web-frontend |
| github-actions, gitlab-ci | ceh-ops |
| changelog-agent, readme-updater | ceh-documentation (unchanged) |
| repo-tree-mapper | ceh-dev-tools (unchanged) |

---

## 4. Shared Python foundation — duplication policy (DECIDED)

The uv/pyproject/ruff/mypy environment and the pytest testing standards are needed by **both**
`ceh-python-service` and `ceh-python-library`. Decision (user, this session): **duplicate the
trimmed delta into both plugins** rather than extract a shared `ceh-python-base`. Each use-case
plugin stays self-contained; a user loads exactly one plugin per use case.

Cost: the two copies can drift. Mitigation: register every duplicated block in
`CROSS_REFERENCES.md` and propagate edits in the same session (existing Cross-Reference Rule).
This policy is recorded in `CLAUDE.md` so future sessions honor it.

Trim difference between copies: the library copy drops web-only dependencies
(`fastapi`, `uvicorn`, `asyncpg`) and the uvicorn dev-server command from `python-environment`.

---

## 5. Execution phases

Incremental and independently shippable. Each phase = one PR, with version bumps in both
`plugin.json` and `marketplace.json`, README skill/agent table updates, and `CROSS_REFERENCES.md`
updates per touched plugin (per CLAUDE.md process).

1. **Dedupe release-ops (highest value, no renames).** Merge security/observability/migrations
   into python-backend; move definition-of-done into open-pr; split versioning into git-workflow
   (tagging) + a `deploy` skill. Delete the emptied skills. Rename `release-ops` → `ceh-ops`.
2. **Pull the app leaks.** Extract `event-sourcing` + `llm-integration` into `ceh-llm-event-backend`,
   or delete if unused. Strip remaining `event_log` references from migrations.
3. **Rename + retarget stack plugins.** `python-backend` → `ceh-python-service` (absorb rest-api,
   postgresql); `typescript-frontend` → `ceh-web-frontend` (consolidate env/style/linting);
   `architecture-design` → `ceh-architecture` (trim to design moments).
4. **Create ceh-python-library.** Duplicate-and-trim environment + testing; author packaging/API/
   semver skills.
5. **Description pass (Problem A).** Rewrite every surviving skill's description to the blog-plugin
   standard: action verbs, explicit trigger signals, explicit "not for…" boundaries. Drop the
   `Phase:` prefixes.
6. **Optional:** merge summarize-chat + lessons-learned → `ceh-session-utils`.

Renames are breaking for users who reference plugin names — bundle each rename with a README note
and a repo-tag MINOR bump.

---

## 6. Open questions

- `adr`: keep in `ceh-architecture` or move to `ceh-documentation` (it produces a doc artifact)?
- `ceh-llm-event-backend`: extract as a real niche plugin, or delete outright? Depends on whether
  any downstream project still uses that pattern.
- `ceh-session-utils` merge: worth it, or leave the two tiny plugins as-is?
- Plugin renames break existing user references — acceptable, or provide alias shims?
