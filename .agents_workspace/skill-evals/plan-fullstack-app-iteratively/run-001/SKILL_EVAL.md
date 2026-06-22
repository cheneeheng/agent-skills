---
artifact: SKILL_EVAL
status: passed
created: 2026-06-22
updated: 2026-06-22
target: ceh-plan-build-review/skills/plan-fullstack-app-iteratively/SKILL.md
target_kind: skill
eval_gate: 6/6
iterations: 2
---

# SKILL_EVAL — plan-fullstack-app-iteratively

> **Scope:** behavioral lift (iteration 1) + triggering (iteration 2, description-routing proxy).
> All four dimensions now measured. Only user confirmation (criterion 6) remains.

## §01 · Verdict

The skill plans one release at a time and produces a machine-resolvable artifact (numbered
§01–§06 sections, frontmatter contract, `depends_on`/pointer chain, Mermaid diff). **Behavioral lift
is real and stable**: across N=2 on both a greenfield-skeleton and an iteration task, the with-skill
arm passed every discriminating assertion (12/12) while the no-skill baseline missed the same
convention assertions every time — zero variance, no regression. The lift is *conformance to the
plan-build-review artifact contract*, not raw planning IQ. **Triggering is accurate**: 9/10 positives
route to the skill, 0/10 near-misses false-fire, and the headline risk — the to-mvp collision — held
at 3/3 routing to to-mvp with zero variance. Gate is **5/6**; only user confirmation (criterion 6)
is open. The one wrinkle is P4 ("help me think through the *architecture* for the next release"),
which routes 3/3 to `document-architecture` — a fair secondary boundary, not a failure, addressable
with a one-line "not for writing ARCHITECTURE.md" pointer.

## §02 · Derived criteria

**Claim.** Produce a *minimal, scoped* plan for the next development intent only — one artifact per
session, never the finished product. Greenfield → a `SKELETON.md`; existing app → an `ITER_NN.md`
scoped to one release. It is the incremental counterpart to `plan-fullstack-app-to-mvp`.

**Trigger intent.**

Should fire when the user wants to plan *one* slice of build work:
- "help me plan the next feature / version / iteration"
- "what should I build first" / "create a skeleton plan for a new app"
- "help me think through this architecture" (early-stage, pre-code)
- vague/early greenfield descriptions wanting just the first thing to build
- planning the next increment of a new major version (v2's next slice)

Should NOT fire (near-misses that share keywords):
- user wants the COMPLETE build to MVP in one session → `plan-fullstack-app-to-mvp` (**critical collision**)
- user wants to build/implement an existing plan → `implement-from-plan`
- user wants to review a plan/code against a plan → review skill
- create a living architecture doc (ARCHITECTURE.md) → `ceh-architecture`
- non-software planning (sprint/ticket assignment, product roadmap)
- code-level refactor planning, project scaffolding/setup

**Intended outcome vs no-skill baseline.** A baseline agent asked to "plan the next feature"
typically sprawls — it specs the whole feature set in full implementation detail and often drifts
toward a finished-product spec. Following this skill should instead yield: a *single* file scoped to
one release, the fixed §01–§06 numbered section structure, YAML frontmatter (artifact / status /
sections / `depends_on` + pointers for iterations), Mermaid architecture diagram, explicit deferral
of anything not needed now (anti-overplan), and a one-sentence next-iteration suggestion that is
*not* itself planned.

## §03 · Trigger battery

**Measured iteration 2** as a description-routing proxy (cold subagent per prompt picks one skill
from the faithful 7-entry catalog, blind to the answer; target = A). The harness can't expose a
subagent's internal Skill decision, so this measures *what the descriptions route to* rather than
observed auto-fire — sufficient for the collision question. Raw data: `iteration-2/routing-results.md`.

**Positive fire rate: 9/10** (threshold ≥8/10 → MET). **Near-miss false-positive: 0/10**
(threshold ≤1/10 → MET). Collision (N1/N2) → to-mvp 3/3, zero variance.

| # | Positive prompt (should fire) | Fires N/3 |
|---|-------------------------------|-----------|
| P1 | "ok i've got this idea for a habit-tracking app, react front end + python api. before i write any code i wanna map out just the first thing to build — where do i even start?" | — |
| P2 | "we shipped v1 of the invoicing tool last month. now i need to add recurring invoices. can you plan just that next chunk of work?" | — |
| P3 | "plan the next version of our notes app" | — |
| P4 | "help me think through the architecture for the next release — don't over-spec it, just enough to start building the export feature" | — |
| P5 | "what should I build first for a recipe-sharing app? just the bare skeleton so I can see if the idea holds" | — |
| P6 | "create a skeleton plan for a new app — a dashboard that pulls metrics from stripe and renders charts" | — |
| P7 | "starting a side project, a web tool for splitting bills among roommates. plan the first iteration only, i'll iterate after" | — |
| P8 | "we're adding SSO to the existing portal. scope out a plan for just this iteration, fastapi backend" | — |
| P9 | "i want to kick off v2 of the analytics platform — reuses the v1 backend but adds a reporting layer. plan the first slice of v2" | — |
| P10 | "plan this iteration: add comment threads to the blog. dont plan beyond it" | — |

| # | Near-miss negative (should NOT fire) | Routes to | Fires N/3 |
|---|--------------------------------------|-----------|-----------|
| N1 | "i don't want to keep coming back to re-plan — lay out the COMPLETE plan from empty repo all the way to a working MVP for my flashcards app, all the iterations at once" | to-mvp | — |
| N2 | "plan the whole thing end to end to a first usable version, simple todo app, i can foresee the whole build" | to-mvp | — |
| N3 | "i've got planning/ITER_03.md ready — now actually build it" | implement-from-plan | — |
| N4 | "implement the skeleton plan we wrote yesterday" | implement-from-plan | — |
| N5 | "review my ITER_02 plan against the code I wrote — did I follow it?" | review skill | — |
| N6 | "set up a living ARCHITECTURE.md with mermaid diagrams and key decisions for our system" | ceh-architecture | — |
| N7 | "help me plan the sprint — assign these 8 tickets across the team for the next two weeks" | none (PM) | — |
| N8 | "plan out how to refactor this 800-line god class into smaller modules" | none (refactor) | — |
| N9 | "draft a product roadmap with quarterly themes for the next year" | none (roadmap) | — |
| N10 | "scaffold the directory layout and config files for a new python service" | ceh-scaffolding | — |

**Threshold (default):** positive fires ≥8/10 (a prompt counts as firing if ≥2/3 runs);
near-miss false-positive ≤1/10.

## §04 · Behavioral tasks & assertions

**Task A — Greenfield skeleton.** Prompt: "I'm starting a new app: a personal bookmark manager,
React frontend + FastAPI backend on Postgres. Help me plan the first thing to build."

| ID | Assertion (true only if the skill worked) |
|----|-------------------------------------------|
| A1 | Output is a *single* skeleton artifact, not a multi-iteration roadmap |
| A2 | Uses the §01–§06 numbered section structure |
| A3 | YAML frontmatter: `artifact: SKELETON` + `sections` list, and **no** `depends_on` |
| A4 | §02 Architecture uses a Mermaid diagram, not ASCII |
| A5 | Explicitly *defers* non-skeleton concerns (auth / error-handling / deploy) rather than speccing them |
| A6 | Routes/screens are stubs (hardcoded/placeholder data), not full implementations |

**Task B — Iteration on existing app.** Given a minimal existing `SKELETON.md`, prompt: "We've
built the skeleton. Now plan just the next iteration: add tagging to bookmarks (create tags, filter
by tag). Don't plan beyond it."

| ID | Assertion |
|----|-----------|
| B1 | Output is a single `ITER_NN` file scoped to tagging only |
| B2 | Uses pointers ("Unchanged — see SKELETON §0X") for untouched sections instead of restating |
| B3 | Frontmatter has `depends_on: [SKELETON]` + `sections_changed` / `sections_unchanged` |
| B4 | Does NOT plan the iteration after this one |
| B5 | §02 shows what *changed* (new tag entity/route), marked as a diff |

Baseline (no skill) is expected to miss: the numbered-section convention (A2/B-structure), the
frontmatter + `depends_on`/pointer mechanism (A3/B2/B3), deliberate deferral (A5), and the
"don't plan ahead" restraint (B4).

### Results (N=2 per arm, evidence in `iteration-1/`)

**Task A — greenfield skeleton.** with-skill **6/6 both runs**; baseline **2/6 both runs** (passed
only A1, A5).

| ID | with r1/r2 | base r1/r2 | Cited evidence |
|----|-----------|-----------|----------------|
| A1 | PASS/PASS | PASS/PASS | single file each; baselines leak a forward "Next slices" backlog (`baseline_run2.md:82` "Next slices (backlog…)") |
| A2 | PASS/PASS | FAIL/FAIL | with: `## §01 · Concept … §05`; base: ad-hoc `## North Star`, `## First Increment` (`baseline_run2.md:17,22`) |
| A3 | PASS/PASS | FAIL/FAIL | with: `artifact: SKELETON / sections: [01..05]`, no depends_on (`with_skill_run1.md:2-8`); base: no frontmatter |
| A4 | PASS/PASS | FAIL/FAIL | with: ` ```mermaid flowchart LR ` (`with_skill_run1.md:18`); base: ASCII `bookmarks ----` block (`baseline_run1.md:46`) |
| A5 | PASS/PASS | PASS/PASS | both defer auth/etc. explicitly |
| A6 | PASS/PASS | FAIL/FAIL | with: `return [...]  # Stub` / commented fetch (`with_skill_run1.md:74-81`); base: real Alembic migration + persisted writes (`baseline_run2.md:51-56`) — a *built* slice, not a stubbed skeleton |

**Task B — iteration.** with-skill **5/5 both runs**; baseline **2/5 both runs** (passed only B1, B4).

| ID | with r1/r2 | base r1/r2 | Cited evidence |
|----|-----------|-----------|----------------|
| B1 | PASS/PASS | PASS/PASS | single ITER scoped to tagging in all four |
| B2 | PASS/PASS | FAIL/FAIL | with: `> Unchanged — see SKELETON § 01` (`taskB/with_skill_run1.md:14`); base: restates §01 as "Goal & Scope", no pointer (`taskB/baseline_run2.md:17`) |
| B3 | PASS/PASS | FAIL/FAIL | with: `depends_on: [SKELETON]` + `sections_changed/unchanged` (`with_skill_run1.md:6-8`); base: `builds_on: SKELETON`, no section lists (`baseline_run1.md:9`) |
| B4 | PASS/PASS | PASS/PASS | all four name only a one-line next scope / Out-of-scope list |
| B5 | PASS/PASS | FAIL/FAIL | with: `classDef changed` + `class Tag,Link changed` + `%% changed` (`with_skill_run2.md:32-34`); base: ASCII model, no marked diagram |

**Confound noted honestly:** in Task B the baseline looked *closer* to the skill output (it adopted
§-numbering and a frontmatter block) because the supplied `SKELETON.md` fixture already modeled
those conventions in-context — yet the baseline still missed the precise pointer / `depends_on` /
diff-marking mechanisms (B2/B3/B5) every time. The skill's delta survives even when the baseline has
a worked example in front of it.

**Variance:** N=2 is below the schema's N≥3 default, so confidence is moderate — but the signal was
unanimous (12/12 with-skill assertion passes, 0 baseline passes on the 7 distinguishing assertions),
i.e. zero observed run-to-run variance, which raises confidence despite the small N. Criterion 5 is
met with that caveat recorded.

## §05 · Structural findings

| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter parses; `name` present | PASS | `name: plan-fullstack-app-iteratively` |
| `name` matches directory | PASS | dir `plan-fullstack-app-iteratively/` |
| `description` present + non-trivial | PASS | rich, ~14 lines, names what/when + counterpart |
| Body non-trivial | PASS | ~186 lines, 3 steps + families model |
| `references/` discipline | ADVISORY | `section-specs.md` (template) + `audit-checklist.md` (checklist) fit; `implementation-gotchas.md` is reference *prose*, arguably outside the repo's "schemas/templates only" rule |
| Repo `validate.py` cross-check | PASS | "OK: all plugin checks passed" |

## §06 · Content findings

Judged inline against `eval-rubric.md` (no subagent — cheap read, evidence cited).

**Description (trigger mechanism):**
- *States what AND when* — PASS. "Use this skill to plan a software project one release at a time"
  (what) + explicit trigger list "help me plan the next feature, plan the next version, plan this
  iteration…" (when) (SKILL.md:4-10).
- *Moment not topic* — PASS. Framed on verbs/situations, not a noun ("what should I build first",
  "plan the next version").
- *Slightly pushy* — PASS. "ALWAYS use this skill even for vague or early-stage descriptions — it
  handles ambiguity" (SKILL.md:10-11).
- *Names what it is NOT for* — PASS, and unusually strong. Explicit counterpart disambiguation vs
  `plan-fullstack-app-to-mvp` with the deciding rule (SKILL.md:12-15). This is the right *content*
  fix for the collision; whether it *works* at trigger time is criterion 3, untested here.

**Body:**
- *Delta vs restatement* — PASS. The §01–§06 contract, plan-families/versioning model, backward-only
  `depends_on`/pointer resolution, and the anti-overplan filter are repo-specific conventions a base
  model does not invent — confirmed empirically: the §04 baselines reproduced none of them.
- *Progressive disclosure* — PASS. SKILL.md ~186 lines; schemas/checklist/gotchas pushed to
  `references/` with "Read when needed — do not load upfront" (SKILL.md:180-186).
- *Explains the why* — PASS. "Overplanning is a blocking risk: a developer who reads ahead into
  unresolved detail will pause to resolve it before building" (SKILL.md:87) — reasoning over bare MUSTs.
- *Least surprise* — PASS.

**One content nit (advisory):** the "Plan Families and Versions" section (SKILL.md:49-73) is
cognitively dense — cross-version `depends_on`, skeleton-as-terminus, self-contained vs
inherits-across rules packed inline. It is correct delta, but the *common* case (default family,
same-version iteration) is the 95% path and the multi-major-version lineage rules could move to
`references/` to keep the inline body lean. Non-blocking.

Criterion 4 (content delta + moment-framed): **MET** with the density nit as advisory.

## §07 · Gate scorecard

| # | Criterion | Met? | Evidence |
|---|-----------|------|----------|
| 1 | Structurally valid | **MET** | `validate.py`: "OK: all plugin checks passed"; name/dir match; rich description; ~186-line body (§05) |
| 2 | Triggers on intent | **MET** | positive routing 9/10 ≥ 8/10 threshold (§03; `iteration-2/routing-results.md`) |
| 3 | Doesn't over-trigger | **MET** | near-miss false-positive 0/10 ≤ 1/10 threshold; to-mvp collision N1/N2 → to-mvp 3/3 |
| 4 | Content is delta + moment-framed | **MET** | rubric pass with cited lines (§06); one advisory (version-lineage density) |
| 5 | Behavioral lift | **MET** | 12/12 with-skill assertion passes vs 0 baseline passes on 7 distinguishing assertions, N=2 both tasks, no regression, zero observed variance (§04). Caveat: N below the N≥3 default |
| 6 | User confirms | **MET** | user confirmed ready 2026-06-22 |

`eval_gate: 6/6` — all criteria met; status: passed.
Thresholds used: positive ≥8/10, near-miss false-positive ≤1/10. Triggering measured as a
description-routing proxy (see §03 faithfulness note).

## §08 · Advisory backlog

- **P4 architecture boundary (minor)** — "help me think through the architecture for the next
  release" routes 3/3 to `document-architecture`, not this skill. Fair (the user said "think through
  the architecture"), and it neither breaks the positive threshold nor causes a false positive. If
  you want to claim that phrasing, add "not for writing the ARCHITECTURE.md doc — see
  document-architecture" to the description; otherwise leave it, the boundary is reasonable.
- ~~Run a triggering pass~~ — **done** (iteration 2): 9/10 positive, 0/10 false-positive, to-mvp
  collision held 3/3. The tail-prose disambiguation works.
- **Version-lineage density (§06)** — consider moving the multi-major-version `depends_on` rules
  (SKILL.md:49-73) to `references/`, keeping the default-family common case inline.
- **`references/implementation-gotchas.md` is prose**, not a schema/template; the repo CLAUDE.md
  reserves `references/` for "schemas and templates only." It is well-used (the with-skill iteration
  arm cited it — `taskB/with_skill_run1.md:69,95`), so the value is real; the mismatch is
  classification only. Verify intent or relabel the references convention. Non-blocking.
- **Baseline planning quality was high** (vertical-slice thinking, acceptance criteria) — the skill's
  value is the *artifact contract*, not planning IQ. Worth keeping that framing in the skill's own
  pitch so users understand why the conventions matter (they make plans resolvable by
  `implement-from-plan`).
