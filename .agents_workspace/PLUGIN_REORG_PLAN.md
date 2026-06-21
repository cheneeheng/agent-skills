# Plugin Reorganization Migration Plan

Status: executed (refactor/plugin-reorg, 2026-06-05)
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
                                dependency-management

Tier 2 — use-case workflow (load per activity)
  ceh-blog                      (unchanged — the reference design)
  ceh-documentation             user/operator guides + changelog/readme agents
  ceh-ops                       (rename of release-ops) incidents, rollback, deploy + CI agents
  ceh-summarize-chat            (unchanged) session summary — kept separate, used by other automation
  ceh-lessons-learned           (unchanged) session retrospectives — kept separate

Tier 3 — stack/build (load per project type)
  ceh-python-service            (rename of python-backend) FastAPI/asyncpg/migrations/web service
  ceh-python-library            (NEW) packaging, public API, semver, no web deps
  ceh-web-frontend              (rename of typescript-frontend) Svelte AND React (Vite);
                                shared a11y/TS-style/testing/tooling
  ceh-architecture              (rename of architecture-design) stack-agnostic design moments
  ceh-scaffolding               (NEW) per-project-type setup: directory layout + initial config

Unchanged
  ceh-dev-tools                 repo-tree-mapper agent

Deleted
  event-sourcing, llm-integration   removed (app-specific, not reusable; no niche plugin)
  gitignore                         removed (entries fold into per-type ceh-scaffolding skills)
```

Net: 11 plugins → 13 (+ ceh-python-library, + ceh-scaffolding; no plugins removed, two renamed).
~46 skills → ~30 after merges/deletes.

**Svelte vs React are NOT split into separate plugins.** Framework skills trigger on file type
(`sveltekit` on `.svelte`, `react-vite` on `.tsx`), so they coexist in one plugin without
mis-firing, while the shared frontend standards (a11y, TS style, testing, tooling) stay
single-sourced. Splitting would duplicate those shared standards — the drift problem this reorg
removes. Apply the "split only when too big" rule later if the framework skills bloat the plugin.

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
| gitignore | file-edit | **DELETE** — required-entries list folds into per-type `ceh-scaffolding` skills ✓ | removed |

### ceh-architecture-design → ceh-architecture (T3)
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| adr | moment | KEEP in ceh-architecture (decision-making is closer to the use case than docs) ✓decided | ceh-architecture |
| domain-modeling | moment | TRIM, keep ID-format/status-enum opinions (desc) | ceh-architecture |
| repository-structure | rare moment | MOVE + reframe: merge into per-type `ceh-scaffolding` skills, not a standalone "structure" skill (desc) | ceh-scaffolding |
| rest-api | moment | MOVE + co-locate with fastapi (kills cross-plugin ref) ✓ | ceh-python-service |
| postgresql | topic | TRIM + MERGE into data moments (`domain-modeling` + migrations) (desc) | ceh-python-service |
| event-sourcing | — | **DELETE** — app-specific, not reusable ✓decided | removed |
| llm-integration | — | **DELETE** — app-specific; overlaps built-in `claude-api` ✓decided | removed |

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

### ceh-typescript-frontend → ceh-web-frontend (T3) — now Svelte + React
| Skill | Trigger | Verdict | Target |
|---|---|---|---|
| sveltekit | file-edit (`.svelte`) | TRIM (desc) | ceh-web-frontend |
| react-vite | file-edit (`.tsx`) | **NEW** — React + Vite framework conventions (routing, hooks, state, Vite config) | ceh-web-frontend |
| accessibility | file-edit | KEEP + generalize trigger to `.svelte` AND `.tsx` (a11y is framework-agnostic) ✓ | ceh-web-frontend |
| frontend-testing | file-edit | TRIM; framework-agnostic (Vitest/Testing Library/Playwright/MSW serve both) (desc) | ceh-web-frontend |
| environment | moment | KEEP — consolidation target; cover Bun + Vite for both frameworks ✓ | ceh-web-frontend |
| coding-style | topic | KEEP content (real delta), MOMENTIZE — MERGE into `environment` so it fires on file edits ✓ | ceh-web-frontend |
| linting | topic | MERGE into `environment` (mostly a quality gate + config) ✓ | ceh-web-frontend |

> Normalization note: Python folds env+style+linting into one `python-environment`; TS splits the
> same into three. Consolidate TS to match — fewer, file-triggered skills.
>
> Framework-agnostic skills (`accessibility`, `frontend-testing`, `environment`/style) are
> single-sourced and serve Svelte and React both. Only `sveltekit` and `react-vite` are
> framework-specific, and they trigger on disjoint file types.

### ceh-scaffolding (NEW, T3)
Per-project-type project setup. There is **no generic "structure" skill** — directory layout,
initial config, and the required `.gitignore` entries are merged into the scaffolding skill for
each project type, so "scaffold a Python library" produces the right layout + config + ignore file
in one moment-triggered skill.

| Skill | Trigger | Source |
|---|---|---|
| scaffold-python-library | "start/scaffold a Python library" | repository-structure (python bits) + gitignore (python entries) + packaging layout |
| scaffold-python-service | "start/scaffold a FastAPI service" | repository-structure (API/services/db layers) + gitignore (python entries) |
| scaffold-web-frontend | "start/scaffold a Svelte or React app" | repository-structure (frontend bits) + gitignore (node entries) |
| scaffold-fullstack-web | "start/scaffold a fullstack web app" | composition of service + frontend layouts |

> The per-type duplication of small shared bits (e.g. `.gitignore` entries) is governed by the
> §4 duplication policy — register them in `CROSS_REFERENCES.md`.

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
2. **Delete the app leaks.** Remove `event-sourcing` + `llm-integration` outright (no niche
   plugin). Strip remaining `event_log` references from migrations.
3. **Rename + retarget stack plugins.** `python-backend` → `ceh-python-service` (absorb rest-api,
   postgresql); `typescript-frontend` → `ceh-web-frontend` (consolidate env/style/linting, add
   `react-vite`, generalize a11y/testing); `architecture-design` → `ceh-architecture` (trim to
   `adr` + `domain-modeling`).
4. **Create ceh-python-library.** Duplicate-and-trim environment + testing; author packaging/API/
   semver skills.
5. **Create ceh-scaffolding.** Move `repository-structure` here, split into per-project-type
   scaffold skills; fold the deleted `gitignore` entries into each. Then delete the standalone
   `gitignore` skill from git-workflow.
6. **Description pass (Problem A).** Rewrite every surviving skill's description to the blog-plugin
   standard: action verbs, explicit trigger signals, explicit "not for…" boundaries. Drop the
   `Phase:` prefixes.

`ceh-summarize-chat` and `ceh-lessons-learned` stay separate plugins (used by other automation
workflows — do not merge).

Renames are breaking for users who reference plugin names — this is **accepted**, no alias shims.
Bundle each rename with a README note and a repo-tag MINOR bump.

---

## 6. Resolved decisions

- **`adr` placement** → keep in `ceh-architecture`. Making the decision is closer to the use case
  than filing a doc; it does not move to `ceh-documentation`.
- **`event-sourcing` / `llm-integration`** → delete outright. No niche plugin.
- **Session plugins** → keep `ceh-summarize-chat` and `ceh-lessons-learned` separate. They are
  used by other automation workflows; do not merge into a `ceh-session-utils`.
- **Plugin renames** → breaking changes are acceptable. No alias shims; document in README +
  repo-tag MINOR bump.
- **Svelte vs React** → one `ceh-web-frontend` plugin, not split (see §2 rationale).
- **`gitignore` skill** → deleted; entries fold into per-project-type `ceh-scaffolding` skills.
