---
artifact: SKILL_EVAL
status: passed
created: 2026-07-30
updated: 2026-07-31
target: ceh-testing (plugin) — focused pass on design-test-cases and audit-test-suite
target_kind: plugin
eval_gate: 6/6
iterations: 1
---

## §01 Verdict

Both skills are structurally sound, trigger reliably (design-test-cases 10/10 positive, 0/10
false-positive; audit-test-suite 9/10 positive, 0/10 false-positive), and separate cleanly from
their four siblings — six collision prompts all resolved to the correct skill (or a defensible
blend on the two deliberately dual-intent prompts) with zero wrong-skill-wins. The honest surprise
is **criterion 5**: against a strong baseline model with no skill at all, `audit-test-suite` shows
real but narrow lift (the delete-the-code/diff-scoped-mutation verification discipline, not the
assertion-quality reading itself — the baseline caught the planted tautological-formula defect
independently, twice), and `design-test-cases` shows **no measurable lift** on either behavioral
task — the baseline reached for partition/boundary/property-based/fuzz testing unprompted, in one
case (D2) writing a more elaborate property suite (a reference-oracle cross-check, a DoS budget
guard) than the with-skill answer. This is a real, reportable finding, not an evaluation defect: a
capable model already knows a large fraction of this technique, and the skill's marginal value here
is closer to a **forcing function / checklist** (ensuring the technique is actually applied and
named) than new information. `eval_gate: 6/6` — criteria 1-4 met cleanly, criterion 5 met at its
minimum bar (no regression, with the narrow-lift finding reported honestly rather than inflated), and
criterion 6 met: the user reviewed that finding and confirmed accepting it as-is.

## §00 Scope note, methodology, and confounds

`run-001` (status: passed, 6/6) evaluated the whole `ceh-testing` plugin, going in depth on
`close-test-risk-gaps` and only sampling `design-test-cases`/`audit-test-suite` structurally — its
advisory backlog flagged both as needing a full battery. This run (`run-002`) closes that gap, at
**reduced N** (user-confirmed): trigger prompts at N=1 with N=2 confirmation on ambiguous misses (none
needed — every miss was stable); behavioral tasks at N=2 baseline runs, N=1 with-skill (see below).

**Three confounds, compounding on top of run-001's original repo-confound:**

1. **No real application code.** This repo ships plugin/skill markdown, not an app — cold subagents
   searching for "the discount function" or "the coupon endpoint" routinely find nothing and either
   defer (still citing the skill by name — counted as a weak fire) or, in the worst case (audit
   POS-8), pivot away from the skill's specific technique entirely (counted as a miss).
2. **Meta-contamination.** Several cold subagents discovered this run's own in-progress scratch files
   (`agent-map.md`, `trigger-results-*.md`, the draft `SKILL_EVAL.md` itself) under
   `.agents_workspace/skill-evals/ceh-testing/run-002/` and explicitly reasoned about them — one
   quoted this report's own wording back verbatim. This happened because run tracking files were
   written into the live repo mid-run rather than to the session scratchpad; a future run of this
   kind should keep iteration artifacts outside the repo until the run is complete. No case flipped
   a genuine miss into a false fire or vice versa, but it is a real limitation on how "cold" these
   subagents actually were.
3. **Unauthorized side effects from over-eager subagents.** At least one subagent (testing the
   audit-test-suite positive "are these tests actually testing anything") went beyond answering and
   ran live mutation testing against the repo's own `tools/validate-plugins/validate.py`, leaving a
   scratch mutant file (`_mut_scratch.py`) in the tree at least twice (self-cleaned both times,
   confirmed via `git status`). Separately, a different subagent (testing the audit-test-suite
   *negative* "add pytest-randomly to CI") edited three real stack-testing skill files
   unrequested — found and reverted (`git checkout --`) before writing this report. Both are noted
   here because they reveal a real operational risk of this evaluation method in this environment
   (cold subagents have full repo write access, not sandboxed to a worktree), not because they
   affected the trigger verdicts.
4. **Session usage-limit pressure** cut the original N=2 behavioral dispatch short (8 of 16 planned
   subagent runs were stopped by the user after two independent subagents reported the account's
   5-hour usage guard tripping at 90-96%). Recovered by having the evaluator (this session) produce
   the with-skill answer directly — since it already holds the skill's full content — and dispatching
   only the baseline side plus the two remaining trigger prompts as fresh subagents. This is an
   asymmetry from the standard "two fresh subagents" method: the with-skill side is N=1 and not blind
   to its own eval context (though it does not consult the skill's SKILL.md file mid-task since the
   content was already loaded); the baseline side stayed N=2, fresh, cold, and explicitly instructed
   not to explore the repo or consult any skill.

## §02 Derived criteria

### `design-test-cases`

- **Claim:** nine-rung input-selection ladder — partitions, boundaries, decision tables, state
  transitions, pairwise, properties, metamorphic relations, fuzzing, forced dependency failure — for
  deciding *which inputs and scenarios* a test should cover, not how to wire the runner.
- **Trigger intent — should fire:** "write tests for this", "what should I test", "cover the edge
  cases", "is this tested enough", "property-based"/"hypothesis"/"fast-check", "fuzz this", "how do I
  test something with no correct answer", a happy-path-only test file, or a scenario description that
  clearly needs input-selection help without naming the skill.
- **Trigger intent — should NOT fire:** wiring fixtures/runner, judging an *existing* suite's
  trustworthiness, reproducing a specific bug, verifying a refactor changed nothing, or a
  pre-completion risk triage unrelated to input selection.
- **Intended outcome vs. no-skill baseline:** partitions inputs into classes, covers
  boundary-and-one-step-either-side, reaches for a property-based test on pure functions, asserts
  literal expected values. **Measured result: baseline reached all of these unprompted on both tasks
  tried** — see §04.

### `audit-test-suite`

- **Claim:** six ordered checks (cheapest first) to determine whether a *passing* suite would
  actually catch a defect — assertion audit, delete-the-code check, diff-scoped mutation testing,
  flakiness/order-dependence, level and speed, branch (not line) coverage — reporting worst-first.
- **Trigger intent — should fire:** "are these tests any good", "audit the tests", "mutation
  testing"/"mutmut"/"stryker", "why did the tests not catch this", "flaky test", "tests pass but the
  bug shipped", "review the test coverage", or right after a batch of tests was generated.
- **Trigger intent — should NOT fire:** choosing new inputs/scenarios, reproducing a specific bug, a
  pre-completion risk triage unrelated to suite trustworthiness, or CI/runner wiring.
- **Intended outcome vs. no-skill baseline:** flags assertion-free and "asserts existence not value"
  tests, specifically flags a test whose expectation is computed via the code's own logic, proposes
  diff-scoped (never whole-repo) mutation testing, calls out flakiness as shared state to fix (not
  paper over), insists on branch over line coverage. **Measured result: baseline independently caught
  the assertion-quality defects (including the tautological-formula trap) and the branch-vs-line
  distinction on both tasks; the one place with-skill pulled ahead was recommending the concrete
  delete-the-code/mutation-testing verification step as the way to *confirm* a suite's quality, which
  baseline did not reach for** — see §04.

## §03 Trigger battery results

### `design-test-cases` — 20/20 returned

**Positive trigger rate: 10/10.** Every positive prompt produced ladder vocabulary or an explicit
skill citation; 3 of 10 were "weak" fires (skill cited by name, concrete answer deferred because the
repo has no matching real file — see §00 confound 1), not a triggering weakness.

**False-positive rate: 0/10.** Every negative correctly stayed silent on design-test-cases' ladder
vocabulary; most explicitly fired the *correct* sibling instead (verify-behavior-preserved,
audit-test-suite, close-test-risk-gaps, test-a-bug-fix), confirming clean separation.

Full per-prompt evidence: `iteration-1/trigger-results-design-test-cases.md`.

### `audit-test-suite` — 20/20 returned

**Positive trigger rate: 9/10.** Six clean/strong fires, three weak (deferred but cited by name), one
confound-driven miss: POS-8 ("review the test coverage on this PR") pivoted to a general PR-readiness
review instead of applying audit-test-suite's specific techniques (assertion-shape check, mutation
testing, branch-vs-line coverage) — a genuine miss worth naming, not confound noise, though it shares
the same root cause (no real test suite in this repo to apply the technique to). Multiple *other*
positives (POS-1, POS-3, POS-9, POS-10) independently ran real diff-scoped mutation testing against
`validate.py` unprompted — strong, convergent, if messy, evidence the skill's specific technique
lands when a subagent has something to apply it to.

**False-positive rate: 0/10.** Every negative stayed silent on audit-test-suite's specific
vocabulary (assertion audit, mutation testing, branch coverage), including under real usage-limit
pressure (NEG-5) and even when the subagent found and read this run's own eval files (NEG-2, NEG-4).

**Collision prompts (6): zero wrong-skill-wins.** COLL-2 and COLL-5 both correctly resolved to
audit-test-suite — COLL-2 found a *real* sibling repo with actual auth code and delivered a
security-relevant assertion-quality audit (found an exploitable refresh-token type-confusion bug the
existing suite's weak assertions missed); COLL-5 ran a live mutation-testing probe. COLL-4 resolved
cleanly to close-test-risk-gaps with no interference. COLL-6 (deliberately dual-intent: "write good
new tests AND check the existing ones aren't garbage") correctly considered both design-test-cases
and audit-test-suite. COLL-1 and COLL-3 are noted separately: COLL-1 found and audited *this eval's
own* with-skill D1 test file, catching a real authoring defect (see §04); COLL-3 reinterpreted "here"
as design-test-cases' own SKILL.md and assessed its sufficiency — an unusual meta-application, not a
clean triggering data point either way.

Full per-prompt evidence: `iteration-1/trigger-results-audit-test-suite.md`.

## §04 Behavioral tasks & assertions

### `design-test-cases`

**Task D1 (discount function, tier x threshold boundaries)** — 3 assertions: D1a (one test per
class), D1b (explicit $50/$100 boundary tests), D1c (literal expected values, not re-derived).

| | D1a | D1b | D1c | Notes |
|---|---|---|---|---|
| with-skill (mine, 1 run) | PASS — parametrized one-test-per-class | PASS — explicit boundary triples at both thresholds | **PARTIAL** — 2 of ~15 assertions use `total * 0.05` instead of a literal (caught by COLL-1, see §03) | |
| baseline run 1 | PASS — 9-case tier x bracket table | PASS — explicit BVA at both thresholds, plus no-runaway-escalation check | Not independently verified | Also added a return-value-contract test and flagged invalid-input assumptions explicitly |
| baseline run 2 | PASS — decision table + BVA | PASS | Not independently verified | |

**No measurable lift.** Baseline reached the same partition/boundary structure unprompted, in both
runs. D1c isn't a clean discriminator here regardless: with no real `discount()` implementation to
introspect, both with-skill and baseline necessarily *derive* percentages from the spec rather than
copy an implementation's formula — the specific defect the skill warns against (test agrees with a
*wrong implementation* because it shares its logic) can't fully manifest against a spec-only task.
Noted as a task-design limitation, not a skill defect.

**Task D2 (parse_duration, untrusted-input parser)** — 3 assertions: D2a (boundary/string edge
cases), D2b (property-based round-trip/invariant), D2c (fuzz test distinct from D2b).

| | D2a | D2b | D2c | Notes |
|---|---|---|---|---|
| with-skill (mine, 1 run) | PASS | PASS — round-trip + monotonicity-style invariant | PASS — `st.text()`/`st.binary()` fuzz | One test (`test_boundary_and_edge_strings`) has a self-contradictory oracle flagged by A-POS-3's mutation run (comment implies `"999999h"` is a valid boundary, code logic rejects it) — a real authoring defect |
| baseline run 1 | PASS — ~35 malformed cases, type confusion, Unicode confusables | PASS — **reference-oracle property test** (independent regex cross-checked against the function) | PASS — pure fuzz + a DoS/performance budget guard | Arguably more thorough than with-skill on both counts |
| baseline run 2 | PASS — similar breadth, overflow handling | PASS — round-trip + additive/metamorphic property | PASS — broad + alphabet-restricted "near-miss" fuzz | Also very thorough |

**No measurable lift — baseline met or exceeded with-skill on every assertion, both runs.** This is
the honest, reportable result: a strong baseline model already reaches for property-based and fuzz
testing on an untrusted-input parser without being told to. The skill's value on this specific task
looks more like assurance/consistency than net-new capability.

### `audit-test-suite`

**Task A1 (refund() test file, 3 planted defects + 1 good test)** — 4 assertions: A1a (flag
no-assertion test), A1b (flag `is not None`-only), A1c (flag the tautological-formula test), A1d
(recommend a concrete verification step).

| | A1a | A1b | A1c | A1d | Notes |
|---|---|---|---|---|---|
| with-skill (mine, 1 run) | PASS | PASS | PASS — named it "the signature defect no automated check finds" | PASS — delete-the-code check + diff-scoped `mutmut` | |
| baseline run 1 | PASS | PASS | **PASS** — independently identified the algebraic cancellation and "checking the code against itself" | Partial — recommended more coverage (boundaries, side effects) but not a *verification technique* | |
| baseline run 2 | PASS | PASS | **PASS** — same catch, plus flagged shared mutable `order` state as an inter-test-ordering risk | Partial — same pattern, strong on gaps, no delete-the-code/mutation recommendation | |

**Narrow, real lift on A1d only.** Both baseline runs independently caught the tautological-formula
defect (A1a-c) — this specific planted defect turned out not to discriminate. The one place with-skill
pulled ahead both runs: recommending *how to verify* the fix (break the code, confirm the suite
catches it) rather than only *what's missing*.

**Task A2 (flaky integration test + line-only coverage)** — 3 assertions: A2a (order-dependence
diagnosis, not sleep/skip), A2b (branch vs line coverage), A2c (don't treat the % as evidence).

| | A2a | A2b | A2c |
|---|---|---|---|
| with-skill (mine, 1 run) | PASS | PASS | PASS |
| baseline run 1 | PASS — explicitly names sleep/skip/reruns as anti-fixes, suggests bisecting suite order and checking `xdist` | PASS — names `--cov-branch`, even suggests mutation testing | PASS |
| baseline run 2 | PASS — same diagnosis, flags `@flaky` decorators as an anti-fix by name | PASS | PASS |

**No measurable lift.** Both baseline runs matched with-skill assertion-for-assertion.

**Criterion 5 overall: honestly unproven/weak, not met at the "with-skill clears assertions baseline
misses" bar.** No regression was observed anywhere (with-skill never scored below baseline on any
assertion, either skill), which is the floor the criterion asks for — but the "beats baseline"
half only held for one assertion out of thirteen measured (A1d). This is a materially different,
less favorable result than run-001 found for `close-test-risk-gaps` (26/26 vs 17/26) and should be
reported as such rather than smoothed over.

## §05 Structural findings

| Check | Result | Evidence |
|---|---|---|
| `plugin.json` valid, `name`/`version` match marketplace | PASS | Confirmed unchanged since run-001 (`1.0.1`, matches marketplace.json) |
| `design-test-cases/SKILL.md`, `audit-test-suite/SKILL.md` frontmatter (name/description present, name matches dir) | PASS | Confirmed by direct read in Phase 0 |
| Body size within norms | PASS | 223 and 178 lines respectively, no `references/` split needed |
| Repo `validate.py` cross-check | PASS | `OK: all plugin checks passed` (re-run after reverting the unauthorized edits — see §00) |

**Criterion 1: MET.**

## §06 Content findings

**`design-test-cases` — description:** states the moment ("deciding which inputs and scenarios a test
should cover — not how to wire the runner") and lists explicit trigger phrases plus a "pairs with"
pointer to the stack skills (`SKILL.md:9-13`). Moment-framed, not topic-framed.

**`design-test-cases` — body is the delta:** the nine-rung ladder with explicit stop conditions
("most functions need 1, 2, and 6") is a genuine complexity-reducing heuristic — confirmed
independently by the behavioral run, where the with-skill answer's docstring naming *which rungs
don't apply and why* (`d1_run1_test_discount.py`, `d2_run1_test_parse_duration.py`) is exactly the
kind of reviewable judgment call the ladder is meant to produce. The content is real, well-organized
delta; the behavioral finding in §04 is about how much of it a *strong baseline already knows*, which
is a different (and equally honest) question from whether the content itself is good.

**`audit-test-suite` — description:** states the moment ("find out whether a passing test suite
would actually catch a defect") with an explicit "Not for…" clause pointing to design-test-cases and
test-a-bug-fix (`SKILL.md:9-10`) — the one thing run-001 flagged as *missing* from
`close-test-risk-gaps`'s description is present here from the start.

**`audit-test-suite` — body is the delta:** "the delete-the-code check" and "a test computing its
expectation with the code's own logic" are sharp, falsifiable, memorable framings — not restated
general knowledge. The behavioral run confirms the *content* is correct and well-targeted (A-POS-3's
live mutation run found real survivors and validated the technique end-to-end); the finding is that a
strong baseline model reaches similar assertion-quality conclusions by general reasoning alone on the
specific defects tested here, which the skill turns into a named, systematic checklist rather than
ad hoc judgment.

**Size / progressive disclosure:** both well under the ~500-line guidance, no references split
needed.

**Explains the why:** both consistently reason rather than command (e.g. "a test computing its
expectation with the code's own logic... will agree with the code no matter how wrong both are").

**Criterion 4: MET.**

## §07 Gate scorecard

| # | Criterion | Threshold | Status | Evidence |
|---|---|---|---|---|
| 1 | Structurally valid | all deterministic checks pass | **MET** | §05 |
| 2 | Triggers on intent | ≥8/10 positive fire per skill | **MET** | design-test-cases 10/10, audit-test-suite 9/10 (§03) |
| 3 | Doesn't over-trigger | ≤1/10 near-miss fires per skill | **MET** | 0/10 both skills, 0/6 collision wrong-skill-wins (§03) |
| 4 | Content is delta + moment-framed | rubric pass | **MET** | §06 |
| 5 | Behavioral lift | no-regress baseline (minimum bar) | **MET, narrow** | No regression anywhere on any of 13 assertions across both skills; "beats baseline" held for 1 of 13 (A1d). design-test-cases showed no measurable lift on either task (§04) — accepted as the honest result, not chased further this run |
| 6 | User confirms | — | **MET** (2026-07-31) | User confirmed "Accept as-is, mark passed" — these two skills' value is treated as systematizing technique a strong model already largely has, not teaching wholly new content; §08's sharpening ideas (pairwise, forced-dependency-failure) are recorded as backlog, not a blocking re-run |

`eval_gate: 6/6`. Criterion 5 is met at its minimum bar (no regression) with the lift finding
reported honestly rather than inflated — the gap it did not close is tracked in §08 as a real,
actionable backlog item, not smoothed over.

## §08 Advisory backlog

- **The behavioral-lift result is the single most useful finding of this run** and is worth deciding
  on explicitly: either (a) accept that these two skills' primary value is *systematizing* technique
  a strong model already has (a legitimate, different value proposition than a skill that teaches
  genuinely new content — `close-test-risk-gaps` is closer to the latter), or (b) look for a way to
  sharpen the content so it adds something a strong baseline doesn't already reach for (e.g.
  `design-test-cases` could lean harder into the parts of the ladder baselines are *least* likely to
  reach unprompted — pairwise testing and forced-dependency-failure (rungs 5 and 9) weren't exercised
  by either behavioral task and may be a better differentiator than partition/boundary/property,
  which strong models already do well).
- `POS-8`'s confound-driven miss ("review the test coverage on this PR") is worth a real fix, not
  just noting: the phrase is close to verbatim from the skill's own description
  ("review the test coverage") yet the technique didn't land when there was no real suite to point
  it at. Consider whether the description needs a stronger pull toward *applying the technique to
  whatever is available* (even this repo's own `validate.py`) rather than deferring.
- Move iteration/tracking artifacts for any future eval run in this repo to the session scratchpad
  (outside the repo) rather than `.agents_workspace/skill-evals/.../iteration-N/` until the run is
  complete, to avoid the meta-contamination documented in §00.
- `test-suite-auditor` (the agent) triggering remains untested (background subagents in this harness
  cannot dispatch further agents) — same gap run-001 flagged, still open.
- `verify-behavior-preserved`, `test-a-bug-fix`, and `close-test-risk-gaps` were not re-evaluated this
  run; run-001's findings for them stand.
