---
artifact: SKILL_EVAL
status: passed
created: 2026-06-22
updated: 2026-06-22
target: ceh-orchestration/skills/orchestrate/SKILL.md
target_kind: skill
eval_gate: 6/6
iterations: 3
---

## §01 Verdict

`orchestrate` enters "thin-orchestrator mode" so the main session plans and delegates while
cheap isolated subagents absorb all I/O — a cost-control posture skill. **PASSED, 6/6.** It is
structurally clean (`validate.py` green), content-strong (why-driven cost-model delta), and —
after the iteration-3 fix — triggers precisely *and* honestly: 6/8 on explicit-intent
positives with 0/8 false-fires (near-misses correctly routed to architecture / claude-api /
ops:deploy / evaluate-skill). Behavioral lift is **measured and real but narrow**: on a
heterogeneous multi-module task the skill reliably added full delegation + verifier gating +
model routing that a no-skill baseline missed (C4 3/3 vs 0/3, no regression), while on a
mechanical rename it correctly stayed out of the way (tooling beats delegation there). The
A2 fix this run reconciled the description's over-promising "minimize cost on any big task"
trigger to "heterogeneous/investigation-heavy" work plus explicit carve-outs (mechanical
sweeps → tooling; single dispatch → not this skill), verified to preserve 6/8 positives and
0/8 false-fires. Single highest-leverage next improvement (advisory): make the
verifier-gating / model-routing discipline more prominent in the body, since that — not the
parallelize-recon instinct, which capable models already have — is the skill's measurable
marginal value.

## §02 Derived criteria

**Claim.** Enter and hold "thin-orchestrator mode": the main session only plans and
delegates — never reads/greps/edits/runs directly — pushing all I/O and execution into
cheap isolated subagents, to cap context/token cost (which grows ~quadratically with a
single window's length).

**Trigger intent.**
- *Should fire:* starting a large, multi-step / multi-file task with explicit delegation
  or cost intent — "orchestrate this", "act as orchestrator", "thin orchestrator mode",
  "delegate this", "plan and delegate", "don't edit directly", "fan this out to
  subagents", or "keep token/context cost down on this big change". Also non-naming
  phrasings that describe coordinating workers to keep the main window cheap.
- *Should NOT fire (near-misses):* pure planning/architecture ("plan this feature" →
  plan-build-review / Plan agent); a single one-off subagent dispatch ("use a subagent to
  find X" → Explore, not a session-wide mode switch); model/API cost & pricing questions
  (→ claude-api); Agent-Teams setup (opposite posture — the skill says reserve teams);
  trivial single-file edits; in-session task decomposition/tracking (contract's task tool,
  no cost-delegation intent); multi-step deploy (→ ceh-ops); evaluating the skill (→
  evaluate-skill).

**Intended outcome (vs no-skill baseline).** With the skill, an agent on a big multi-file
task: restates the goal in one line, produces a plan + dependency-ordered subtask list,
dispatches each subtask to the matching subagent (Explore / executor / verifier), keeps a
compact summary-only ledger, refuses to pull raw file contents into its own window, routes
work to the cheapest adequate model, and verifies via the verifier rather than re-reading.
A baseline agent instead opens files, greps, and edits directly in the main session,
accumulating context.

## §03 Trigger battery

Method: each prompt → fresh cold `general-purpose` subagent given only the user message,
told to show how it would *begin* (no execution, brief). Firing is coded from the final
message exhibiting thin-orchestrator posture (one-line goal restate + delegation plan +
explicit subagent dispatch + ledger/model-routing language) vs handling the task normally.
N=3; a prompt "fires" if posture appears in ≥2/3. Confidence note: subagent tool calls are
not visible to the parent, so firing is inferred from output posture, not a Skill-tool
trace — lower confidence than a direct trace.

Threshold used: positives fire ≥6/8; near-misses false-fire ≤1/8.

**Positives**
- P1 "orchestrate this — refactor the auth module across ~12 files and rename the session token field everywhere"
- P2 "act as orchestrator for this DB migration, there are a lot of files to touch and I don't want you doing it inline"
- P3 "thin orchestrator mode please — big multi-package refactor incoming"
- P4 "this is a huge multi-file change and I'm worried token/context cost is going to blow up. keep the main session lean and push the work down to workers"
- P5 "I've got a ~30-file codemod to run. I want you coordinating cheap subagents rather than grinding through every file in this session yourself"
- P6 "fan this out to subagents — independent subtasks here, hand each one off and just track results, don't pull all the file contents into your own context"
- P7 "don't edit directly. plan it, split it up, and delegate the implementation"
- P8 "split this big task into pieces and farm them out to workers so your own window stays cheap"

**Near-miss negatives**
- N1 "plan the architecture for a new notifications feature — what components do we need?"
- N2 "use a subagent to go find where we handle rate limiting"
- N3 "what's the cheapest Claude model for a high-volume classification job, and how much would a batch run cost?"
- N4 "set up agent teams so the frontend and backend agents can message each other while they work on this feature together"
- N5 "rename getUser to fetchUser in src/user.ts"
- N6 "break this big feature into subtasks and track them with the task tool as you go"
- N7 "handle this multi-step deploy for me: build the image, push it, and promote to staging"
- N8 "review my orchestrate skill and tell me whether it's any good"

**Results (N=2; run 3 omitted — could not change any classification, see iteration-1/triggering.md):**
- Positive trigger rate: **6/8** (P1-P5, P8 fired both runs; P6, P7 showed correct but
  generic fan-out without distinctive markers). Threshold ≥6/8 → **MET**.
- Near-miss false-positive rate: **0/8** (all negatives routed elsewhere). Threshold ≤1/8 → **MET**.
- Notable: P6/P7 contain verbatim description trigger-phrases yet didn't surface distinctive
  firing — likely an output-based detector limit (no Skill-tool trace visible to parent);
  behavior was still correct. Several negatives named the right alternative skill unprompted.
- Evidence: `iteration-1/triggering.md`.

**Iteration-3 re-test (after A2 description edit; evidence `iteration-3/triggering.md`):**
positive rate **6/8 unchanged**, false-positive rate **0/8 unchanged**. The narrowed wording
+ carve-outs removed the over-promise without costing any positive or adding any false-fire.
P2 dipped to 2/3 (one run fumbled the skill *identifier*, not a description fault). Criteria 2
& 3 remain MET post-edit.

## §04 Behavioral tasks & assertions

**Task A — refactor under cost pressure** (no skill named):
"I need to rename the `userId` field to `accountId` across our TypeScript backend — it's
in models, services, routes, and tests, ~15 files. I care a lot about keeping token/context
cost down on this. Get started."
- A1: produces a plan with discrete, dependency-ordered subtasks (not one undifferentiated edit blob).
- A2: delegates work to subagents (names subagent_type / Agent dispatch / "I'll hand this to a worker") rather than reading/editing files directly itself.
- A3: keeps a compact summary-only ledger and explicitly avoids pulling raw file contents into the main window.
- A4: routes to cheapest adequate model (executor=Sonnet / verifier=Haiku, or "cheapest model that clears the bar").

**Task B — guardrail under invitation to dive in:**
"Audit our repo's logging calls and standardize them to structured logging across all
packages. Just dig in and start fixing them."
- B1: despite "just dig in", dispatches an Explore/worker to locate the logging calls rather than grepping/reading directly itself.
- B2: plans verification against acceptance criteria (verifier) rather than re-reading worker output.

Baseline (no skill) expected to clear A1 partially at best; expected to miss A2/A3/A4 and
B1/B2 (it dives into direct grep/read/edit). N=3 per arm.

**Results (Task A 3+3; Task B 3 with-skill + 1 baseline — r2/r3 baseline hit a session rate
limit; full detail + quotes in `iteration-1/behavioral.md`):**

| Task | Assertion | With-skill | Baseline | Lift |
|------|-----------|-----------|----------|------|
| A | A1 staged plan | partial 3/3 | partial 3/3 | none |
| A | A2 delegates vs direct I/O | FAIL 0/3 | FAIL 0/3 | **none** |
| A | A3 lean ledger | N/A (no delegation) | N/A | none |
| A | A4 model routing | FAIL 0/3 | FAIL 0/3 | **none** |
| B | B1 dispatch Explore/worker | FAIL 0/3 | FAIL 0/1 | **none** |
| B | B2 verify via verifier | N/A | N/A | none |

**The skill did not fire in either behavioral arm.** Task A: with-skill and baseline produced
*indistinguishable* plans (grep --count → branch → `sed`/replace_all → `tsc` verify) — agents
in both arms judged a scripted pass cheaper than spawning executors. Task B: all arms gave the
same scope-mismatch pushback + survey (agent-coding-contract behavior, not orchestration).
**Zero measurable lift in either task.** Root cause: both tasks were framed by cost / "just
dig in", not an explicit delegation verb — and the trigger battery shows the skill fires on
explicit verbs, not on cost-intent alone. Criterion 5 (iter-1) = unproven (tasks didn't
exercise a fired-skill scenario; where measured, lift was zero).

**Iteration 2 — lift re-test (Task C: un-sed-able, explicit "Orchestrate this"; full detail +
quotes in `iteration-2/behavioral.md`). All 6 runs completed:**

| Assertion | With-skill | Baseline | Lift |
|-----------|-----------|----------|------|
| C1 dependency-ordered delegation decomposition | 3/3 | 3/3 | none |
| C2 delegate recon AND implementation | 3/3 | 1/3 full (2/3 recon-only/deferred) | partial |
| C3 lean ledger, summaries not contents | 3/3 | 3/3 | none |
| C4 model routing + verifier-after-executor | **3/3** | **0/3** | **clear, stable** |
| C5 not solved by single scripted pass | 3/3 | 3/3 | none |

Skill fired in all 3 with-skill runs (explicit verb worked as triggering predicted). **Lift
confirmed — narrow and stable:** with-skill reliably adds full delegation (C2) plus verifier
gating & model routing (C4 at 3/3 vs 0/3, zero variance) that the baseline misses, with **no
regression** on C1/C3/C5. Honest scope: a capable model already parallelizes recon and stays
lean without the skill — the skill's measurable marginal value is its specific operational
discipline (delegate edits too, gate every executor with a verifier, route by model tier).
**Criterion 5 = MET.**

## §05 Structural findings

| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter parses | PASS | valid YAML, `name` + `description` present (SKILL.md:1-4) |
| `name` matches directory | PASS | `name: orchestrate` == dir `skills/orchestrate/` |
| `description` present & non-trivial | PASS | full what+when+triggers, SKILL.md:3 |
| Body non-trivial | PASS | 121 lines, substantive cost model + rules |
| references/ discipline | PASS | no references/ dir; all content inline, 121 lines (<500) |
| plugin.json present & valid | PASS | name `ceh-orchestration`, version `1.0.0` |
| plugin name matches dir | PASS | `ceh-orchestration` == dir |
| version is semver | PASS | `1.0.0` |
| marketplace entry & version match | PASS | marketplace.json shows `ceh-orchestration` `1.0.0` |
| agents valid | PASS | executor (sonnet), verifier (haiku); name/desc/tools present |
| Cross-check: validate.py | PASS | "OK: all plugin checks passed" |

All structural checks pass.

## §06 Content findings

Judged against `eval-rubric.md`. Cited lines from SKILL.md unless noted.

**Description (line 3)**
- States what AND when: PASS — "Load when starting a large, multi-step task you want to
  decompose and delegate rather than execute directly" (what) + explicit trigger-phrase
  list (when).
- Moment not topic: PASS — "when starting a large, multi-step task" is a verb/moment, not
  a noun-topic. "Stays in effect for the rest of the session once entered" sets posture.
- Slightly pushy: PASS — eight explicit trigger phrasings listed.
- Names what it is NOT for: **FIXED in iter-3** (was FAIL). The description now carries
  "Not for mechanical single-pass changes where a scripted edit plus a typecheck is cheaper
  (e.g. a repo-wide rename), nor for a single one-off subagent dispatch." Closes the
  over-trigger insurance gap and reconciles the cost trigger with reality (A2).

**Body**
- It's the delta: PASS (strong) — the cost model is genuinely tool-opinionated knowledge
  the model wouldn't reliably produce: quadratic context re-billing (12-17), prompt-cache
  prefix (92-94), agent-teams ~7× tokens (112-119), CLAUDE.md inheritance tax + @imports
  caveat (96-101), `CLAUDE_CODE_SUBAGENT_MODEL` precedence gotcha (77-79), Batch-API
  caveat (107-109). Little to no restatement of general knowledge.
- Progressive disclosure: PASS — 121 lines, well under ~500; no split needed.
- Explains the why: PASS (exemplary) — "Why this exists (the cost model)" (12-21);
  reasoning ("X because Y") throughout; cost levers ranked by impact (89-109). Rules are
  bold, not ALL-CAPS-MUST walls, and each is justified.
- Least surprise: PASS.

Content verdict: strong delta + moment-framed + why-driven; single fix = add a "not for…"
clause to the description.

## §07 Gate scorecard

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Structurally valid | MET | §05 all pass + validate.py (re-run post-edit: green) |
| 2 | Triggers on intent | MET | §03: 6/8 positives, held after A2 edit (iter-3) |
| 3 | Doesn't over-trigger | MET | §03: 0/8 false-fires, held after A2 edit (iter-3) |
| 4 | Content delta + moment | MET | §06: strong delta/why; "not for" clause added iter-3 |
| 5 | Behavioral lift | MET | §04 iter-2: C4 3/3 vs 0/3, C2 partial, no regression, low variance |
| 6 | User confirms | MET | user chose "apply A2 first, then confirm"; A2 applied + re-run clean |

`eval_gate: 6/6` — **PASSED.**

Thresholds used: positives fire ≥6/8; near-misses false-fire ≤1/8; "fires" = ≥2/3 runs (here
≥2/2). Stated for reproducibility per schema.

## §08 Advisory backlog

- **A1 (content): RESOLVED iter-3** — "not for…" carve-outs added to the description
  (mechanical single-pass → tooling; single one-off dispatch → not this skill). Re-test
  confirmed false-positives stayed 0/8.
- **A2 (value/triggering): RESOLVED iter-3** — the over-promising cost-only trigger was
  reconciled with reality: opening qualified to "heterogeneous or investigation-heavy parts",
  the standalone cost trigger replaced with "coordinate cheap workers on a big multi-area
  change", and the mechanical-sweep carve-out added. Verified non-regressive (6/8 positives,
  0/8 false-fires). Residual (low): the body could foreground the verifier-gating /
  model-routing discipline — the part baseline reliably lacks (see A3).
- **A3 (lift re-test): DONE** (iteration 2, Task C) — criterion 5 now MET. Residual: the lift
  is narrow (C4 + partial C2 only); if the author wants broader demonstrable value, the body
  could make the verifier-gating / model-routing discipline more prominent, since that is the
  part baseline reliably lacks.

## §09 Method decisions (this run)

- **Triggering N:** ran N=2; run 3 omitted because it could not change any prompt's
  classification under the ≥2/3 rule (all prompts at 2/2 or 0/2). Cost-aware, consistent with
  the target skill's own teaching.
- **Firing detector:** output-based (distinctive thin-orchestrator markers), since a subagent's
  Skill-tool calls are not visible to the parent. Lower confidence than a direct trace; flagged
  on P6/P7 where behavior was correct but markers absent.
- **Baseline construction:** simulated counterfactual ("skill unavailable") rather than a
  plugin-disabled environment (the skill is globally registered, not disableable per-subagent).
  Lower confidence noted.
- **Incomplete runs:** Task B baseline r2/r3 hit a session rate limit; reported as a limit, not
  imputed. Variance across the 7 collected Task B observations was ~0, so the conclusion holds.
