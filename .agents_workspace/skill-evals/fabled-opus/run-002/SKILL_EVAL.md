---
artifact: SKILL_EVAL
status: draft
created: 2026-07-07
updated: 2026-07-07
target: ceh-fabled/skills/fabled/SKILL.md
target_kind: skill
eval_gate: partial (behavioral-lift only; scoped run)
iterations: 1
---

# §01 Verdict

Run-002 re-tested `fabled` on **harder, discriminating tasks** than run-001 — a Simpson's-paradox
decision and a planted binary-search edge bug, each with one checkable correct answer and a strong
pull toward a specific wrong one — to force a baseline failure and measure lift *magnitude*.
**It didn't work: the harder tasks didn't break baseline Opus either.** Baseline (no skill) scored
**18/18** across both tasks × 3 runs — all three baseline runs caught the Simpson's reversal and
recommended against Team X, and all three traced the binary-search bug to a concrete breaking input.
With-skill also scored **18/18, zero regressions.** So run-002 *replicates* run-001's core result on
a deliberately harder battery: **no correctness lift, because the base model never fails.** The one
observable delta is modest and non-correctness: on Task 1 the with-skill arm produced sharper
*calibration* — 3/3 explicitly separated "the case for X is unsupported" (certain, arithmetic) from
"Y is genuinely better" (uncertain, small samples), and 2/3 computed an actual significance check
(z≈1.2, p≈0.23); baseline flagged the small sample but 1/3 over-claimed "Y is the better team" and
0/3 computed significance. That is `decision-standards` calibration discipline firing — real, but it
raises *quality of hedging*, not correctness. **Bottom line: on a frontier model, the traps a
grader can easily construct sit inside baseline capability, so measured lift is confined to
calibration-consistency (run-002) and verify-over-refuse (run-001), not corrected answers. This is
exactly the ceiling the skill names for itself: "raises the floor and narrows the gap; does not
transplant capability." To measure correctness lift you must move the baseline below the task — a
weaker base model (see the sibling `fabled-sonnet` run) or genuinely frontier-hard tasks.**

# §02 Derived criteria

**Claim.** Applying fabled's process — effort triage, alternatives-before-committing, full-depth
decomposition, adversarial self-review, verification of the checkable, calibrated delivery — produces
a better *outcome* than a first-pass answer on a non-trivial task, without adding raw capability.

**Scope of this run.** User directive: *"Check whether it helps, use a more complex example, run 001
was too easy, no need to worry about trigger."* → **behavioral-lift-only** (dimension 4), harder task
set. Triggering/structure/content deliberately not measured. Consistent with run-001, the with-skill
arm is *handed* the protocol (told to read + apply SKILL.md and matching references); the baseline
arm gets the raw prompt with no skill and **no "think hard" priming**. This isolates *applied* lift
from triggering.

**Why these tasks are harder than run-001.** Run-001's tasks were judgment/calibration tasks a strong
base model already handles. Run-002's two tasks each have (a) a checkable correct answer and (b) a
*seductive wrong answer* the prompt's framing pushes toward. The design goal was to force a baseline
failure so lift magnitude (not just presence) becomes measurable. **Outcome: the design goal was not
met — the traps were not beyond baseline Opus. That is itself the finding.**

# §03 Trigger battery

Not measured — out of scope (user: "no need to worry about trigger").

# §04 Behavioral tasks & assertions

Model: Opus (all arms). N=3 per arm. Paired with-skill vs baseline, launched same turn.
Generated outputs (per user's path override): `run-002/generated/opus/task{1,2}/{baseline,with_skill}/run{1,2,3}.md`.

## Task 1 — Simpson's paradox decision (statistical trap)

Prompt gives overall rates (Team X 73% = 110/150, Team Y 56% = 84/150) that push "standardize on X,"
plus a subgroup table where Y beats X in **both** strata:

| Difficulty | Team X | Team Y |
|---|---|---|
| Easy | 90/100 (90%) | 19/20 (95%) |
| Hard | 20/50 (40%) | 65/130 (50%) |

Ground truth: **do not standardize on X.** Y is better on both easy (95>90) and hard (50>40); X's
overall edge is a caseload artifact — X handled 100/150 easy tickets, Y only 20/150. Simpson's
reversal. Anti-pattern targeted: sycophantic drift toward the framing; scope drift to "compare the
two big numbers."

- **T1-1** Identifies Y outperforms X within BOTH subgroups (95>90 and 50>40).
- **T1-2** Names/explains the confound: X's overall rate is a case-mix artifact (Simpson's), not real superiority.
- **T1-3** Does NOT recommend standardizing on X on the 73%-vs-56% basis.

## Task 2 — planted binary-search edge bug (code-trace trap)

`first_ge(arr, target)` must return the first index `>= target`, or `len(arr)` if all are smaller.
Bug: `hi = len(arr) - 1`, so when `target` exceeds every element it returns `len(arr) - 1` (an index
whose element is `< target`) instead of `len(arr)`. Normal cases pass, so the bug survives casual
reading. Breaking input `arr=[1,3,5], target=9` → returns `2`, expected `3`. Anti-pattern targeted:
verification skipping (ship code untraced); first-thought "standard lower_bound, LGTM."

- **T2-1** Concludes the function is INCORRECT.
- **T2-2** Identifies the failing case — target > all elements returns `len(arr)-1` (root cause `hi = len(arr)-1`).
- **T2-3** Supplies a concrete breaking input (actually traced, not hand-waved).

## Grading

Pass = assertion met with cited evidence from the delivered answer.

| Assertion | Baseline (r1/r2/r3) | With-skill (r1/r2/r3) | Delta |
|-----------|:---:|:---:|-------|
| T1-1 both-subgroups | ✓✓✓ | ✓✓✓ | none |
| T1-2 names confound (Simpson's) | ✓✓✓ | ✓✓✓ | none |
| T1-3 rejects X | ✓✓✓ | ✓✓✓ | none |
| T2-1 concludes incorrect | ✓✓✓ | ✓✓✓ | none |
| T2-2 root cause | ✓✓✓ | ✓✓✓ | none |
| T2-3 breaking input traced | ✓✓✓ | ✓✓✓ | none |
| **Assertion totals** | **18/18** | **18/18** | **0 at assertion level** |

**Both arms cleared every assertion in every run. Zero regressions, zero correctness lift.** Evidence
that baseline needed no help:

- **Task 1 baseline** — run1 named "Simpson's paradox … the cause is caseload mix, not skill" and
  computed the counterfactual (X on Y's caseload ≈47%); run2 titled it "textbook … Simpson's Paradox"
  with a mix-normalized 68% vs 60%; run3 "textbook Simpson's paradox … institutionalize the weaker
  process." All three rejected the plan outright.
- **Task 2 baseline** — run1 traced `[1,2,3],5 → returns 2, correct 3`; run2 gave a step table + a
  5-row verification matrix for the fix; run3 traced `[10,20,30],99`. All three found the `hi`
  root cause and recommended `bisect_left`.

**The one real (non-correctness) delta — Task 1 calibration:**

| | separates "X unsupported" (certain) from "Y better" (uncertain) | computes a significance check | over-claims "Y is the better team" |
|---|:---:|:---:|:---:|
| Baseline | partial (2/3) | 0/3 | 1/3 (run1) |
| With-skill | **3/3** | **2/3** (run2 z≈1.2 p≈0.23; run1 "moderate confidence") | 0/3 |

With-skill run2: *"High that 73/56 doesn't support X (arithmetic); Medium-low that Y is better …
p ≈ 0.23 … directional, not conclusive … most likely way I'm wrong: the labels aren't comparable."*
That is `references/decision-standards.md` (calibrated verdicts, honest confidence) firing — the
with-skill arm consistently produced the more defensible calibration. It is a genuine quality edge,
but it is **not** captured by the pass/fail assertions and it is **not** answer-correction: baseline's
verdict was already right.

- **Task 2** showed no meaningful delta — both arms traced multiple cases and found the bug. With-skill
  runs traced slightly more confirming cases (empty/duplicate/first-element) but baseline run2 also
  produced a full verification table. Parity.

**Variance:** low. The 18/18 vs 18/18 split and the calibration pattern were stable across all 3 runs
per arm — no run-to-run flip-flopping.

# §05 Structural findings

Not measured — out of scope for this run.

# §06 Content findings

Not measured — out of scope for this run.

# §07 Gate scorecard

Only criterion 5 (behavioral lift) is in scope. Threshold: N=3/arm/task, lift = "clears assertions
the baseline misses AND does not regress baseline, stable across runs."

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Structurally valid | not measured | out of scope |
| 2 | Triggers on intent | not measured | out of scope |
| 3 | Doesn't over-trigger | not measured | out of scope |
| 4 | Delta + moment-framed | not measured | out of scope |
| 5 | **Behavioral lift** | **UNPROVEN (correctness) / present (calibration), 0 regressions** | Baseline 18/18 and with-skill 18/18 → "clears what baseline misses" is untestable here (baseline missed nothing) on **harder** tasks than run-001, confirming the base model isn't the bottleneck. Real but modest calibration lift on Task 1 (3/3 vs partial). No regression anywhere. |
| 6 | User confirms | scoped-accepted (2026-07-07) | User accepted the behavioral-lift result as-is; declined the weaker-model and frontier-hard follow-ups. NOT a 6/6 ship pass — criteria 1–4 unmeasured by design, criterion 5 correctness-lift unproven. Status stays `draft`. |

`eval_gate`: n/a as a /6 count for a scoped run. **Criterion 5 verdict: correctness lift remains
unproven — now demonstrated to persist even against deliberately harder traps, because baseline Opus
clears them. Lift is real but confined to calibration-consistency (this run) and verify-over-refuse
(run-001).**

**Load-bearing caveats (carried from run-001, still apply):**

1. **This measures applied lift, not real-world lift.** Triggering was excluded; the with-skill arm
   was *handed* the protocol. Real value = P(triggers) × applied-lift; this isolates the second factor.
2. **No generic-effort control.** The with-skill arm was told to "read and apply a reasoning skill,"
   which primes effort independent of fabled's specific content. Without a third "reason carefully, no
   skill" arm, this run cannot separate "fabled's content helped" from "being told to try hard
   helped." Given the near-zero delta that's moot here, but it would matter the moment a real delta
   appears. Flagged in §08.
3. **The eval is hitting the skill's own stated ceiling.** SKILL.md line 112: *"This skill raises the
   floor and narrows the gap; it does not transplant capability."* On a strong model + non-frontier
   tasks, baseline already sits near the ceiling, so there is little floor to raise. This is consistent
   behavior, not a skill defect — but it means "does it help?" can only be answered *"yes, on tasks
   where the base model is actually at risk of failing"* — which these were not.

# §08 Advisory backlog

- **To prove correctness lift, move the baseline below the task (highest leverage).** Two clean paths:
  (a) **weaker-model baseline** — run this exact battery with Sonnet/Haiku on both arms; a weaker base
  model *will* fall for the Simpson's framing or miss the edge bug, making "with-skill clears what
  baseline misses" measurable. The sibling `fabled-sonnet` folder suggests this is already underway —
  cross-reference it. (b) **frontier-hard tasks** — traps at/just beyond Opus's capability, which are
  hard to construct and grade and where the skill's own thesis predicts limited lift anyway. Path (a)
  is far cheaper and more decisive.
- **Add a generic-effort control arm** ("reason carefully and thoroughly; verify before answering" —
  no skill) to any future run. It's the only way to attribute a real delta to fabled's *content* vs
  mere effort priming.
- **Sharpen the calibration assertion.** The one real delta this run found (separating a certain claim
  from an uncertain one; computing significance) was invisible to the pass/fail rubric. A future
  Task-1-style assertion — "distinguishes the confident sub-claim from the uncertain one AND does not
  over-claim on n=20" — would *score* the calibration lift instead of relegating it to prose.
- **Effort-triage / cost regression check** (unmeasured): does fabled correctly skip the machinery on a
  trivial task (anti-pattern 12)? With-skill runs here used ~1.3× baseline tokens (37–43k vs 32k) —
  modest on these tasks, but the triage behavior is untested.
- Full-battery `evaluate-skill` (triggering + structure + content) before any ship decision.
