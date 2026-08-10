# Cross-Reference Map

Tracks content duplicated word-for-word across multiple skills. When editing any entry,
update **all listed files**. Each block is intentionally inlined (zero file reads at runtime);
this map exists so edits don't get lost.

---

## Same Skill, Different Plugins (name map)

These skill pairs are the **same foundational standard duplicated into two plugins** per the
Shared-Standards Duplication Policy (see `CLAUDE.md`). Skill names are plugin-qualified so that
every skill name in the repo is unique; this table maps each pair back to its shared standard.
Editing one copy means editing the other in the same session — full file lists and divergence
notes live in the detailed entries referenced below.

| Shared standard | `ceh-python-service` name | `ceh-python-library` name | Detailed entry |
|-----------------|---------------------------|---------------------------|----------------|
| Python environment foundation (uv / ruff / mypy + style) | `python-service-environment` | `python-library-environment` | "Python environment foundation" below |
| Python testing foundation (pytest core) | `python-service-testing` | `python-library-testing` | "Python testing foundation" below |

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

## Auto-merge probe + enable (gh pr merge --auto)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/merge/SKILL.md` | "PR Merge & Cleanup" section | canonical — full probe with the direct-merge fallback |
| `ceh-git-workflow/skills/open-pr/SKILL.md` | "Auto-Merge" section + the `gh pr merge --auto` tail of the "Command" block | enables auto-merge at PR-creation time on repos that allow it |

**What is shared:** the `allow_auto_merge` probe (`gh api repos/{owner}/{repo} --jq .allow_auto_merge`) guarding `gh pr merge --merge --auto --delete-branch`, which queues the PR to land when the gate (CI + approvals) goes green.

**What diverges:**
- `merge` adds the direct-merge fallback (`gh pr merge --merge --delete-branch`) for repos without auto-merge, where the gate must already be green.
- `open-pr` runs only the probe-and-enable half, right after `gh pr create`, so a PR opened on an auto-merge repo lands itself without a separate merge invocation.

**What also references this:** `ceh-release-flow:release-flow` step 9 names the same `--auto` behavior but delegates to the `merge` skill rather than inlining the command — keep its wording consistent if the probe changes.

---

## Reading CI status (gh run, not gh pr checks)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/merge/SKILL.md` | "Reading CI status" under "Pre-Merge Gate" | canonical — full command set plus the three traps |
| `ceh-git-workflow/agents/branch-merger.md` | "Inputs" bullet | one-line echo of the working commands + the `gh pr checks` prohibition, pointing back at the skill |

**What is shared:** read the gate with `gh run list -c "$(git rev-parse HEAD)"` (commit-anchored, Actions API); never `gh pr checks` or `gh pr view --json statusCheckRollup`, which return 403 on a fine-grained PAT lacking `checks=read` — a permissions error, not a red gate.

**What diverges:**
- `merge` adds `gh run watch --exit-status`, `gh run view --log-failed`, the legacy-Commit-Statuses trap (`commits/<sha>/status` returns 200 with `total_count: 0` forever), the third-party-checks blind spot, and the `mergeStateStatus` gate-vs-diagnose distinction.
- `branch-merger` carries only the prohibition and the two commands it needs, since it preloads the merge skill via frontmatter.

---

## PR Checklist Items

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/open-pr/SKILL.md` | two "Checklist" blocks — the rendered template (after the body) and the `--body-file` body template in the "Command" block | canonical — only holder; the seven items appear twice in this one file |

**What is shared:** seven checklist items, repeated word-for-word in both "Checklist" blocks inside `open-pr`: "All CI checks pass", "Tests added or updated for new behavior", "No `any` / `@ts-ignore` / `# type: ignore` introduced", "No secrets or credentials in code", "Migrations (if any) are backward-compatible", "ARCHITECTURE.md Key Decisions updated (if a durable decision was made)", "Attribution included if AI tooling assisted".

**What diverges:**
- The two `open-pr` blocks are identical — keep them in sync when editing.

---

## Coverage Targets (test coverage minimum percentages)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-git-workflow/skills/open-pr/SKILL.md` | "Coverage Targets" section (under Definition of Done) | canonical — three rows incl. TypeScript |
| `ceh-python-service/skills/python-service-testing/SKILL.md` | coverage section | two Python thresholds with identical row labels |
| `ceh-python-library/skills/python-library-testing/SKILL.md` | coverage section | two Python thresholds with identical row labels |

**What is shared (identical labels and thresholds):** two rows, word-for-word — `Python application package | 80%`, `Core business logic / domain services | 95%`.

**What diverges:**
- `open-pr` adds a third row (`TypeScript src/lib/ | 70%`) and the `mypy --strict` / `tsc --noEmit` note.
- both testing-skill copies (`python-service-testing` / `python-library-testing`) omit the TypeScript row and add a pytest `--cov` command (`--cov=app` for the service, `--cov=your_library` for the library).

---

## Python environment foundation (uv / ruff / mypy + style)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-python-service/skills/python-service-environment/SKILL.md` | entire file | service copy — web-service deps + uvicorn dev server (style half also injected by the service SessionStart hook) |
| `ceh-python-library/skills/python-library-environment/SKILL.md` | entire file | library copy — no web deps, no uvicorn dev server (style half also injected by the library SessionStart hook) |

**What is shared:** Python 3.12 + uv + `pyproject.toml`/`uv.lock` workflow, the uv command table, the ruff (line-length 88, `select = [E,F,I,UP,N,B]`) + mypy (`strict = true`) + pytest (`asyncio_mode = "auto"`) config, the coding-style rules (type hints, built-in generics, no `Any` without comment), naming table, three-group imports, and the "ruff only / no `# type: ignore` without comment" linting rules.

**What diverges (per the Shared-Standards Duplication Policy):**
- library copy drops `fastapi`/`uvicorn[standard]`/`asyncpg` from the deps example and the uvicorn dev-server command; sets `dependencies = []` and `known-first-party` to the library package; uses a library-flavored docstring example.

---

## Python testing foundation (pytest core)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-python-service/skills/python-service-testing/SKILL.md` | entire file | service copy — real DB / HTTP integration |
| `ceh-python-library/skills/python-library-testing/SKILL.md` | entire file | library copy — public-API tests, no DB/HTTP |

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

## Plan document schema (SKELETON / ITER frontmatter, file naming, version families)

**Files:**

> This duplication is **intentional and sanctioned** (the only such exception in the repo): the
> skills are also used standalone outside the plugin, so each skill folder carries its own copy.

| File | Section | Scope |
|------|---------|-------|
| `ceh-plan-build-review/skills/plan-fullstack-app-to-mvp/references/section-specs.md` | "File Naming" + "Output Frontmatter" + terminator block | **golden standard** — producer copy; emits the whole set incl. the MVP terminator |
| `ceh-plan-build-review/skills/plan-fullstack-app-iteratively/references/section-specs.md` | "File Naming" + "Output Frontmatter" | producer copy — emits one artifact per session |
| `ceh-plan-build-review/skills/implement-from-plan/references/plan-schema.md` | entire file | consumer copy — schema plus pointer rules and resolution order |
| `ceh-plan-build-review/skills/review-against-plan/references/plan-schema.md` | entire file | consumer copy — identical to the `implement-from-plan` copy |
| `ceh-plan-build-review/skills/patch-built-version/references/plan-schema.md` | entire file | consumer copy — identical to the `implement-from-plan` copy |

**What is shared:** file naming and version-tag rules (`SKELETON.md` / `ITER_NN.md`, `NN` two digits; canonical `_vN` suffix, `vN_` prefix also read; tag-sharing files form a plan family with a per-family `NN` counter); SKELETON frontmatter (`artifact`, `status`, `created`, `app`, `stack`, `sections`, no `depends_on`, no MVP fields); ITER frontmatter (`artifact`, `status`, `created`, `scope`, `sections_changed`, `sections_unchanged`, `depends_on` by stem, backward-only, covering both same-family chaining and cross-version inheritance); the MVP terminator convention (`mvp: true` + `mvp_target` + `## Out of MVP scope` body block on the final iteration only; non-terminal iterations omit `mvp` entirely); the patch convention (`patch: true` ITER continuing the family counter, `depends_on` the terminator or a prior patch, allowed past the terminator, never carries `mvp`, `sections_changed` within §04/§05 — produced by `patch-built-version`, consumed by `implement-from-plan` and `review-against-plan`).

**What diverges:**
- the producer copies omit the consumer-only material (pointer formats, resolution order, the absent-terminator fallback).
- the iterative producer copy does not describe the terminator block (one-artifact-at-a-time sessions don't emit it).
- the producer `section-specs.md` copies do not describe the `patch` marker — patches are produced by `patch-built-version`, not by the two planning skills.
- the three `plan-schema.md` consumer copies are word-for-word identical — keep them in lockstep.

---

## §02 Architecture diagram requirement (Mermaid, not ASCII art; iterations visualize the change)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-plan-build-review/skills/plan-fullstack-app-to-mvp/references/section-specs.md` | "§02 · Architecture" | producer copy — golden standard, same wording as the iterative copy |
| `ceh-plan-build-review/skills/plan-fullstack-app-iteratively/references/section-specs.md` | "§02 · Architecture" | producer copy — identical wording |
| `ceh-plan-build-review/skills/implement-from-plan/references/plan-schema.md` | "Sections" table, §02 row | consumer copy — condensed table-cell form |
| `ceh-plan-build-review/skills/review-against-plan/references/plan-schema.md` | "Sections" table, §02 row | consumer copy — identical to the `implement-from-plan` row |
| `ceh-plan-build-review/skills/plan-fullstack-app-to-mvp/references/audit-checklist.md` | "Architecture (§02)" | verification copy — pre-delivery check |
| `ceh-plan-build-review/skills/plan-fullstack-app-iteratively/references/audit-checklist.md` | "Architecture (§02)" | verification copy — identical bullet |
| `ceh-plan-build-review/skills/review-against-plan/SKILL.md` | "Check" table, §02 row | verification copy — post-implementation review check |

**What is shared:** the component diagram must be Mermaid, not ASCII art; at skeleton level it shows what exists and how pieces connect; at iteration level it must additionally visualize what changed (new/modified pieces marked distinctly), not just restate the current state.

**What diverges:**
- the two `section-specs.md` copies carry the full skeleton/iteration prose (word-for-word identical).
- the two `plan-schema.md` copies carry the condensed table-cell form (word-for-word identical).
- the two `audit-checklist.md` copies carry a single checklist bullet (word-for-word identical).
- `review-against-plan/SKILL.md` carries the verification as a clause appended to its existing §02 check-table row, not a standalone bullet.

---

## Blog Voice section (personal voice, banned tells, never-invent rule)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-blog/skills/blog-writer/SKILL.md` | "Voice" section (top of file) | canonical — full section |
| `ceh-blog/skills/blog-interviewer/SKILL.md` | "Voice" section (top of file) | word-for-word copy |
| `ceh-blog/skills/blog-editor/SKILL.md` | "Personal voice, not influencer style" bullet (Core Principles) + "Influencer tells" checklist item | condensed restatement — same banned-tells list, framed for diagnosis |

**What is shared:** personal voice, not influencer style; the reader overhears the reasoning, not a lecture; the `CLAUDE.md` blog-voice override; the prefer list (first person, connected paragraphs, doubt kept in, open inside a moment); the banned tells (one-liner paragraphs, aphoristic closers, imperative lessons, "If you're building X, then Y", bold pseudo-headers, meta-takeaway sign-offs, CTA endings); never invent scenes/feelings/chronology — flag the gap instead; the open-thread endings definition (honest current state; reserved verdict valid; closure only for a finished series' final post); series-as-serials framing; tutorial pitfalls narrated as cost to the author.

**What diverges:**
- writer and interviewer copies are word-for-word identical — keep them in lockstep.
- editor restates the banned tells as diagnostic targets ("never edit toward, never introduce") rather than drafting rules, and omits the prefer/series/tutorial paragraphs; it carries the open-thread definition in its "Closing" checklist item and template preamble instead (it has no Voice section).

---

## Blog Structure by Post Type (six templates, open-thread endings)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-blog/skills/blog-writer/SKILL.md` | "Structure by Post Type" (Phase 3) | canonical — full template lines |
| `ceh-blog/skills/blog-interviewer/SKILL.md` | "Structure by Post Type" (Phase 3) | near-identical; Launch "Origin" line adds "(this IS the problem)" |
| `ceh-blog/skills/blog-editor/SKILL.md` | "Post Type Structures" (Step 3) | abridged middles (shorter Origin/Argument lines); identical endings |

**What is shared:** the six post-type templates (Lessons Learned, How-To, Opinion/Take, Project/Launch, Thought Leadership, Personal Story); every template's "The Open Thread:" closing line (word-for-word identical across all three files); the How-To Hook ("The moment this became a problem for you / what it cost you") and Pitfalls line ("what they cost you — narrated as your experience, not warnings issued to the reader").

**What diverges:**
- writer and interviewer preambles point to the Voice section ("Every template ends on **the open thread** (defined in Voice)."); editor's preamble carries the full open-thread definition since it has no Voice section.
- interviewer's Launch template keeps the "(this IS the problem)" suffix on the Origin line.
- editor's middles are abridged (it targets reordering, not drafting) — but its ending lines match the canonical wording exactly.

---

## Blog repurpose handoff line

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-blog/skills/blog-interviewer/SKILL.md` | end of "Phase 4 — Refine" | canonical |
| `ceh-blog/skills/blog-writer/SKILL.md` | end of "Phase 4 — Refine" | word-for-word copy |
| `ceh-blog/skills/blog-editor/SKILL.md` | end of "Step 4 — Invite Feedback" | word-for-word copy |

**What is shared:** the single handoff sentence pointing a satisfied user at
`/ceh-blog:blog-repurpose` (Twitter/X thread, LinkedIn post, TL;DR, newsletter blurb) — identical
in all three files.

---

## Write-less-code ladder (skill + per-turn digest)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-agent-coding-contract/skills/write-less-code/SKILL.md` | "The ladder" + "When NOT to be lazy" | canonical — full skill, loaded on demand when code is written |
| `ceh-agent-coding-contract/hooks/less-code-payload.sh` | `additionalContext` array | compact digest of the ladder + never-simplify list, injected per-turn by the `UserPromptSubmit` hook |

**What is shared:** the six-rung ladder (YAGNI → stdlib → native platform feature → already-installed
dependency → one line → minimum that works) and the never-simplify-away list (trust-boundary
validation, data-loss handling, security, accessibility, anything explicitly requested). Keep the
digest in sync with the skill when either changes.

**What diverges:**
- SKILL.md is the full guidance (rules, output discipline, the `// less-code:` comment convention); the payload is the compressed per-turn reflex.
- the `agent-coding-contract` skill states the complementary *negative* rules (no new deps, no speculative abstractions, minimal diffs) in its "Universal Non-Goals" — not a copy, but keep the two from contradicting on the dependency stance.

**What also references this:** the "Retroactive ladder + behavior preservation" entry below re-frames the same six rungs for already-written code (`shrink-diff` / `refactor-repo`) — if the ladder's rungs change, keep the retroactive framing aligned.

---

## Retroactive ladder + behavior preservation (shrink-diff / refactor-repo)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-agent-coding-contract/skills/shrink-diff/SKILL.md` | "The retroactive ladder" + "Behavior preservation" | canonical — branch-diff-scoped application |
| `ceh-agent-coding-contract/skills/refactor-repo/SKILL.md` | "The retroactive ladder" + "Behavior preservation" | word-for-word copy — campaign-wide application |

**What is shared:** the six-rung retroactive ladder (delete outright → stdlib → native platform feature → installed dependency → one line → keep as the minimum, collapsing single-implementation abstractions / single-caller wrappers / config-for-a-constant) and the behavior-preservation rules (never mix a behavior change into a refactor; tests before and after where coverage exists, red-before is a finding not a license; mechanical transforms only without coverage; pin behavior with `ceh-testing:verify-behavior-preserved` before anything past a mechanical transform; `refactor:` commits separate from any other change).

**What diverges:**
- `shrink-diff` applies both blocks to the branch's seed set in one pass; `refactor-repo` applies them per approved cluster in Phase 3, with skip-and-report emphasized for uncovered areas.
- the retroactive ladder derives from the Write-less-code ladder entry above (same six rungs, re-framed in hindsight) — a rung change there propagates here.

---

## Evaluate-skill shared blocks (structural checks + triggering note)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-evaluation/skills/evaluate-skill/SKILL.md` | "Structural integrity" check + "Triggering note" blockquote | canonical — full skill |
| `ceh-evaluation/skills/evaluate-skill-lite/SKILL.md` | Phase 2 dimensions 1 & 2 | near-verbatim restatement in the lite variant |

**What is shared:** the deterministic structural-integrity check list (frontmatter parses,
`name` matches dir, `description` present, body non-trivial, `references/` discipline; plugin manifest
+ marketplace version match) and the "Triggering note" blockquote ("the model only consults a skill
for tasks it can't trivially handle alone …").

**What diverges:**
- `evaluate-skill-lite` shares the `references/` directory by relative path (`../evaluate-skill/references/`)
  rather than copying the rubric or report schema — those are not duplicated.
- The lite triggering note drops "behavioral and" (lite has no behavioral dimension) and lite runs
  triggering at N=1 vs the full skill's N=3.

---

## Release-commit message block (step 7 detail)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-release-flow/skills/release-flow/SKILL.md` | "Step 7 detail — the release commit is not subject-only" | canonical |
| `ceh-release-flow/skills/direct-release-flow/SKILL.md` | "Step 7 detail — the release commit is not subject-only" | near-verbatim copy |

**What is shared:** the rule that `chore: release vX.Y.Z` is the subject and not the whole message,
the commit-message template (what shipped / `Bump:` / `Manifests:` / `Docs:` / attribution footer),
the `git commit -F` requirement, and the delegation warning that a subagent handed only the subject
will commit exactly that.

**What diverges:** the direct variant adds one sentence — with no PR, the commit message is the only
durable narrative of the release. Related but *not* duplicated: `ceh-git-workflow/skills/release/SKILL.md`
step 1 states the same "always multi-line, body required" rule in its own command-block comment, and
`ceh-git-workflow/agents/commit-author.md` states that a required subject constrains the subject line
only. Keep all four consistent in intent when the rule changes.

---

## Implementation gotchas (planning skills)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-plan-build-review/skills/plan-fullstack-app-to-mvp/references/implementation-gotchas.md` | entire file | **canonical** — the all-at-once planner's copy |
| `ceh-plan-build-review/skills/plan-fullstack-app-iteratively/references/implementation-gotchas.md` | entire file | copy — byte-for-byte identical |

**What is shared:** the whole file. Both planning skills fold the same gotchas into the artifacts
they emit, and each skill folder carries its own copy so the skill stays self-contained.

**What diverges:** nothing. These two files are byte-identical and must stay that way — if a gotcha
becomes producer-specific, split it out explicitly rather than letting the copies drift.

---

## AGENTS.md interop at scaffold time

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-scaffolding/skills/scaffold-python-service/SKILL.md` | "Agent instruction file" | **canonical** |
| `ceh-scaffolding/skills/scaffold-python-library/SKILL.md` | "Agent instruction file" | copy — identical |
| `ceh-scaffolding/skills/scaffold-web-frontend/SKILL.md` | "Agent instruction file" | copy — identical |

**What is shared:** Claude Code reads `CLAUDE.md` and not `AGENTS.md`; when a repo already has an
`AGENTS.md`, write a `CLAUDE.md` whose first line is `@AGENTS.md` rather than duplicating content;
Claude-specific instructions go below the import; a symlink works but needs Administrator or
Developer Mode on Windows, so the import is preferred.

**What diverges:** nothing — the rule is project-type agnostic. `scaffold-fullstack-web` carries no
copy: it composes the service and frontend skills, which each state the rule.

---

## Test-suite audit findings report (skill / agent)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-testing/skills/audit-test-suite/SKILL.md` | "Reporting" | canonical — in-session report |
| `ceh-testing/agents/test-suite-auditor.md` | "Output to Parent Session" | near-identical copy — subagent report handed back |

**What is shared:** the worst-first ranked finding format (`SEVERITY  file:line  what`) and the five
example rows covering the same defect classes — assertion-free test, expectation computed with the
code's own formula, surviving mutants at a boundary, order-dependent failure under `--random-order`,
and a slow unit test doing real I/O.

**What diverges:**
- the agent caps the list at ~15 findings and adds the commands-run / skipped-checks ledger, the
  zero-coverage list, and a "bugs found in source, reported not fixed" section — it cannot ask the
  parent anything, so the report has to stand alone.
- the skill's version separates what was fixed from what needs a decision, because the main session
  can act on findings immediately.

Note that `ceh-testing` deliberately shares **no** content with the three stack testing skills
(`python-service-testing`, `python-library-testing`, `frontend-testing`): those own runner,
fixtures, and mocking; `ceh-testing` owns technique. Keep it that way — a technique block appearing
in a stack skill is the signal that this boundary has slipped.

---

## Usability persona set + severity scale

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-usability-audit/skills/first-run-walkthrough/SKILL.md` | "The personas" + "Score by observed outcome, not by appearance" | canonical — the five-row persona table and the four-row severity table |
| `ceh-usability-audit/skills/audit-interface/SKILL.md` | "Run the persona battery" + "Rank by observed outcome" | verbatim copy of both tables |
| `ceh-usability-audit/README.md` | "The personas" + "Severity — assigned by outcome, not by appearance" | condensed copies for the reader; column wording differs, the five personas and four severities must not |
| `ceh-usability-audit/agents/novice-walker.md` | "Holding the persona" | the same five personas restated as **second-person instructions to the walker**, not as a table |

**What is shared:** the five personas (Blank Slate, Cautious Returner, Interrupted, Wrong Turn,
Small Screen) with their constraints and the failure class each catches; the four severities
(Blocker, Detour, Friction, Polish) with their assignment conditions; and the rule that severity
comes from an observed walker outcome, with anything unobserved demoted to an unranked `Hypotheses`
list. Adding, removing, or renaming a persona or severity means editing all four files.

`Blank Slate` is scoped by the **audience baseline** declared at dispatch, in all four copies —
without that qualifier the persona stalls on "terminal" and returns a Blocker on every target. If
the baseline wording changes anywhere, change it everywhere.

**What diverges:**
- `first-run-walkthrough` adds the actions-to-success and external-lookups measurements, which are
  first-run-specific (external lookups are meaningless once the user is already inside).
- `audit-interface` keeps the persona table but supplies an in-product goal instead of a setup goal.
- `novice-walker` phrases each persona as a rule the agent obeys ("take no action whose outcome was
  not stated") rather than a constraint it is described by — it never sees the severity scale at
  all, deliberately: the walker reports stalls, the caller ranks them.
- Both skills append the same delegation note sending WCAG mechanics to
  `ceh-web-frontend:accessibility`; `Small Screen` covers environment, never conformance.

---

## Explanation honesty rules (evidence, no code dumps, present tense)

**Files:**

| File | Section | Scope |
|------|---------|-------|
| `ceh-dev-tools/skills/explain-codebase/SKILL.md` | "Rules" section | canonical — the full list, including the accounting and regeneration rules that only apply to a generated file |
| `ceh-agent-coding-contract/skills/explain-until-understood/SKILL.md` | "Rules" section | the three rules that hold for a spoken explanation too |

**What is shared:** three bullets, word for word — "Evidence over inference" (unclear purpose is
written as "purpose unclear — checked imports and call sites, no references found", never guessed
at; never invent a responsibility), "Don't paste code" (a signature or a three-line snippet is the
ceiling, with a literal that *is* the behavior quoted verbatim outside that ceiling), and "Describe
what exists today, not what was planned or is half-built".

**What diverges:**
- `explain-codebase` adds four rules bound to producing a file: not a code review, depth follows
  weight, regenerate rather than patch, and the accounting requirement over the whole inventory.
- `explain-until-understood` adds the rule that has no meaning without a live reader: "not
  documented" and "I did not check" are different answers, and only a grep earns the first.
- The two skills also cross-link in prose (a "Not the same as" row each way) — that pointer is not
  a shared block and does not need mirroring when these rules change.

---

## Update Protocol

When changing a shared block:
1. Find the canonical file (marked above).
2. Edit it first — that's the source of truth for the rule.
3. Propagate the change to every other listed file in the same commit.
4. Update this file if the scope of sharing changes.
