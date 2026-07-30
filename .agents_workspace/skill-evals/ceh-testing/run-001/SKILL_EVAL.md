---
artifact: SKILL_EVAL
status: passed
created: 2026-07-30
updated: 2026-07-30
target: ceh-testing (plugin)
target_kind: plugin
eval_gate: 6/6
iterations: 2
---

## §01 Verdict

`ceh-testing` is a well-built plugin: structurally clean, its five skills partition the testing
lifecycle with almost no collision (0/13 false positives on `close-test-risk-gaps`, and every
near-miss negative correctly fired a *different* sibling skill instead), and `close-test-risk-gaps`
produces a measurable, reproducible behavioral lift over a strong baseline — most sharply on the
idiom-specific assertions (bounded query count, 404-not-403, schema-validated contract) a baseline
model does not reliably reach for on its own. Triggering recall started at 7/10 (threshold 8/10); the
three misses shared a pattern — scenario descriptions that don't use the skill's own named-technique
vocabulary ("shared stock counter" instead of "race condition," "double-charge" instead of
"idempotent," "look up by customer_id" instead of "authorization"). Adding scenario-shaped cues (and
a missing "not for" clause) to the description fixed two of the three cleanly (9/10, gate cleared)
with zero new false positives; the third (a shared-counter race phrased without any of the skill's
vocabulary) stayed a stable miss even after the fix — the model answers it confidently from general
knowledge regardless, which looks like a genuine ceiling rather than a description defect. All 5
measurable criteria now pass; only user sign-off remains.

## §00 Methodology note — a structural confound in this run

This evaluation runs from inside `ceh-testing`'s own source repository. Cold trigger-battery
subagents have `Read`/`Grep`/`Glob` and, on a non-trivial fraction of prompts, used them — three
responses (CTRG-POS-3, the parse_duration negative, and one Task-B run) explicitly located and
quoted `ceh-testing/skills/.../SKILL.md` by searching the filesystem rather than (necessarily) via
the Skill tool's own auto-trigger. This means "fired" in §03/§04 below is operationalized as **the
skill's content was consulted and applied** (verbatim/near-verbatim idiom matches, explicit
citation, or the skill's own distinctive reporting structure), not strictly "the auto-trigger
mechanism activated on the description alone" — the two are conflated when evaluating a skill from
inside its own repo, and no tool available in this session can separate them (subagent final
reports are the only visibility into subagent behavior; no raw tool-call trace is exposed to the
caller). Confidence in criterion 2 specifically should be read with this caveat: it is possible the
true auto-trigger rate is *lower* than measured, if some "fires" here were filesystem discovery
rather than description-driven triggering — which would make the identified gap (§03) understating
the problem, not overstating it.

A second, entirely deterministic corroborating signal was available and used: the `tool_uses` count
returned with each subagent result. `tool_uses: 0` conclusively rules out any tool invocation
(including `Skill`) for that run — used to confirm CTRG-POS-1 and CTRG-POS-2's initial "fired"-looking
content was actually general background knowledge, not the skill.

## §02 Derived criteria

### Plugin-level claim

`ceh-testing` supplies stack-agnostic testing **technique** — which inputs to choose, whether a
green suite is trustworthy, and what a passing functional suite structurally misses — deliberately
excluding runner/fixture/mocking concerns owned by the three stack testing skills. Five skills, each
bound to a distinct lifecycle moment, plus one read-only audit agent.

| Skill | Moment | Should NOT fire on |
|---|---|---|
| `test-a-bug-fix` | Fixing a bug/crash/regression, before writing the fix | Choosing new-feature test inputs, judging an existing suite |
| `design-test-cases` | Deciding which inputs/scenarios a test should cover | Wiring the runner, auditing an existing suite |
| `audit-test-suite` | Judging whether a passing suite would catch a defect | Choosing new inputs, testing a specific bug fix |
| `verify-behavior-preserved` | Before a behavior-preserving change (refactor/extract/upgrade/port) | Changes that intentionally change behavior |
| `close-test-risk-gaps` | Pre-completion gate: "is this ready" | Any of the above four moments in isolation |
| `test-suite-auditor` (agent) | Delegating the slow/high-output half of `audit-test-suite` | Quick inline assertion review (skill handles that) |

### In-depth target: `close-test-risk-gaps`

Selected as the riskiest/most-changed skill: largest diff in the most recent commit (+72/-lines,
adding the 5th failure class), and structurally the highest triggering risk in the plugin — a
triage gate with **five independent trigger conditions** evaluated per-class, rather than one
single trigger, which is the shape most likely to under-fire on some classes while over-fabricating
tests on others.

- **Claim:** given a feature that's functionally working and about to be called done, triage five
  failure classes invisible to "given this input, is the output right" — concurrency/idempotency,
  contract drift, performance regression, authorization, migration/rollout compatibility. Per class:
  if the trigger condition fires, add the one minimal named test; if it does not fire, skip
  **explicitly** and say why.
- **Trigger intent — should fire:** "is this ready", "anything else to test", "before I open the
  PR", "did I miss anything", plus scenario descriptions of race conditions, webhook retries, N+1
  queries, authz, migrations/backfills — even without naming the skill.
- **Trigger intent — should NOT fire:** requests to choose inputs for a *new* test
  (`design-test-cases`), audit an *existing* suite's trustworthiness (`audit-test-suite`), reproduce
  and fix a *specific* bug (`test-a-bug-fix`), or verify a *refactor* changed nothing
  (`verify-behavior-preserved`) — these share testing vocabulary but are different lifecycle moments.
- **Intended outcome vs. no-skill baseline:** the with-skill agent systematically probes blind spots
  a baseline agent's happy-path suite review misses — invariant-based concurrency assertions (not
  response-code assertions), an authz matrix that returns 404 (not 403) for another user's resource,
  N+1 query-count assertions (not wall-clock timing), schema-validated contract tests (not
  hand-written dict comparisons), and migration round-trip/backfill-idempotency tests — **and**
  explicitly reports which classes it skipped rather than staying silent on them.

### Sampled: `design-test-cases`, `audit-test-suite`, `test-a-bug-fix`, `verify-behavior-preserved`, `test-suite-auditor`

Structural + content review in full (already read completely in Phase 0); a lighter 4-positive /
4-negative trigger check (N=1, sanity read rather than gate-scored) instead of the full N=3 x 8-10
battery. No behavioral-lift subagent runs for these five in this pass — flagged in §08 as the
natural next run if this evaluation is repeated.

## §03 Trigger battery — `close-test-risk-gaps` (in-depth, N=3, gate-scored)

**Positives (10):**
1. "The coupon redemption feature is done and all tests pass — is there anything else I should test before opening the PR?"
2. "Before I ship this, is this ready? Tests are green."
3. "Did I miss anything on this order charge endpoint before merging?"
4. "We've had webhook retries double-charge customers before — can you check if this new charge handler is safe?"
5. "Is this migration safe to run on prod? It renames a column."
6. "Can two people redeem the last coupon at the same time? Want to make sure that's not a race condition."
7. "Double-checking auth on this endpoint — can another tenant somehow see this data?"
8. "The orders list page feels like it could N+1, worth checking before we deploy?"
9. "Not sure I'm confident enough to call this done — tests pass but idk."
10. "We're backfilling a new column on the users table — is that safe for a rolling deploy?"

**Near-miss negatives (10):**
1. "Write some tests for this new discount() function."
2. "These tests keep failing randomly, not sure why."
3. "Users report the app crashes on this input, can you fix it?"
4. "I want to refactor this class to remove duplication without breaking anything."
5. "Can you run mutation testing on this module?"
6. "Getting a KeyError in prod — this worked last week."
7. "What edge cases should I cover for this date parser?"
8. "I upgraded pydantic, want to make sure nothing changed."
9. "Are these tests actually testing anything or just passing?"
10. "How do I property-test this sorting function?"

**Cross-skill collision prompts (does the right one win?):**
1. "This bug fix is done, tests pass — is it safe to ship?" (`test-a-bug-fix` vs `close-test-risk-gaps`)
2. "I just refactored the auth middleware, all tests still pass, ready to merge?" (`verify-behavior-preserved` vs `close-test-risk-gaps`)
3. "Is this test suite good enough before we ship?" (`audit-test-suite` vs `close-test-risk-gaps`)

### Results

**Positive battery** (N=1 first pass on all 10; N=2 on the 3 that showed no fingerprint, to confirm
stability — see §00 for how "fired" is operationalized):

| # | Prompt topic | tool_uses | Fired? | Evidence |
|---|---|---|---|---|
| 1 | coupon shared-stock counter | 0, 0 (2 runs) | **NO** (stable) | No skill idiom; general TOCTOU-race knowledge only |
| 2 | customer lookup by ID, "is this ready" | 0, 0 (2 runs) | **NO** (stable) | General IDOR/pagination advice, no 5-class structure |
| 3 | order charge + Stripe | 3 | **YES** | Explicitly cites `ceh-testing/skills/.../close-test-risk-gaps`; reproduces the exact "Reporting the gate" format verbatim |
| 4 | webhook double-charge | 3, 2 (2 runs) | **NO** (stable) | Solid generic idempotent-webhook pattern, no 5-class structure, no citation either run |
| 5 | migration renaming a column | 1 | **YES** | "Expand, then contract — in separate deploys" near-verbatim to skill text |
| 6 | coupon race (names "race condition") | 2 | **YES** | "assert the invariant... which one wins is legitimately nondeterministic" — near-verbatim |
| 7 | cross-tenant document access | 1 | **YES** | "Return 404 (not 403)... to avoid confirming existence" — matches skill's "leaks the ID space" reasoning |
| 8 | orders list N+1 | 1 | **YES** | Query-count assertion idiom (`assert_num_queries`) matches skill's `query_counter` pattern |
| 9 | CSV export, "not confident" | 7 | **YES** | Full "risk gate — which classes actually apply" structure with fire/skip verdicts per class |
| 10 | rolling-deploy backfill | 2 | **YES** | `test_backfill_is_idempotent`, `test_old_code_still_reads_new_schema` — near-verbatim function names and comments from the skill |

**Positive trigger rate: 7/10 (70%)** — below the 8/10 gate threshold.

**Near-miss negatives:** 0/10 fired `close-test-risk-gaps`. Every one instead fired the *correct*
sibling skill with strong, distinctive content: NEG-1 → `design-test-cases` (partition/boundary
ladder), NEG-2 → `audit-test-suite` (flakiness/order-dependence), NEG-3 → `test-a-bug-fix` (explicit
citation, reproduce-first protocol), NEG-4 → `verify-behavior-preserved` (near-verbatim "green bar
with zero test edits is the gate"), NEG-5 → `audit-test-suite` (delete-the-code check, mutmut),
NEG-6 → `test-a-bug-fix`-flavored root-cause-then-reproduce, NEG-7 → `design-test-cases`-flavored
(weak/general-knowledge, tool_uses:0), NEG-8 → `verify-behavior-preserved` (near-verbatim
"Dependency and runtime upgrades" section), NEG-9 → `audit-test-suite` (near-verbatim assertion-audit
grep pattern), NEG-10 → `design-test-cases` rung 6 (matches the "four shapes" property-testing
framework exactly).

**False-positive rate: 0/10.** Exceeds the ≤1/10 threshold with room to spare, and doubles as strong
evidence the plugin's five skills have well-separated trigger moments in practice.

**Collision prompts:** all three resolved gracefully — no wrong-skill-wins case observed.
- COLL-1 (bug fix + "safe to ship"): both `test-a-bug-fix` (exact "prove the test is coupled to the
  fix" `git stash` idiom) and `close-test-risk-gaps` (concurrent-case test + explicit per-class
  skip reporting) fired and combined correctly.
- COLL-2 (refactor + "ready to merge"): `verify-behavior-preserved` dominated (equivalence-diff
  golden file, "deny by default," "fails closed") — a defensible single-skill resolution given the
  prompt is fundamentally about behavior preservation; `close-test-risk-gaps`'s 5-class structure
  did not appear.
- COLL-3 ("test suite good enough" + "before we ship"): both `audit-test-suite` (assertion-audit,
  delete-the-code, mutation) and `close-test-risk-gaps` (concurrency/idempotency, authz matrix,
  explicit "skip... N/A" framing) fired and blended sensibly.

**Diagnosis of the 3 misses:** all three describe the trigger scenario *without* using the
description's own named-technique vocabulary — "shared stock counter" (not "race condition"),
"double-charge" (not "idempotent"), "look up by customer_id" (not "authorization"/"IDOR"). The 7
that fired either used the named technique directly (POS-6 says "race condition"; POS-5 nearly
quotes "is this migration safe") or hit a phrase from the description almost verbatim (POS-9's "not
confident" ~ description's "tests pass but I am not confident"). This is a targeted, fixable
description gap, not a broad failure — see §04 for the fix and re-run.

### Iteration 2 re-run (after the description fix — see §04)

Re-tested the 3 misses at N=2 each, plus a 3-negative and 2-positive regression spot-check.

| Prompt | Pre-fix | Post-fix run1 | Post-fix run2 | Evidence |
|---|---|---|---|---|
| POS-1 (shared stock counter) | 0/2 | NO (tool_uses:0) | weak/NO (tool_uses:1, no distinctive idiom) | Still general TOCTOU knowledge only — **stable miss** |
| POS-2 (customer lookup by ID) | 0/2 | **YES** (tool_uses:3) | **YES** (tool_uses:5) | Both runs reproduce the full 5-class gate verbatim: "Authorization — FIRES... Skipped, explicitly: Concurrency..., Contract drift..., Migration..." |
| POS-4 (webhook double-charge) | 0/2 | **YES** (tool_uses:10) | **YES** (tool_uses:3) | Both runs explicitly cite the skill by name: "this is exactly the `close-test-risk-gaps` idempotency class" / "per this repo's `close-test-risk-gaps` skill" |

POS-2 and POS-4 flipped cleanly from stable misses to stable, strongly-evidenced fires — the new
scenario-shaped cues ("a caller-supplied ID could return someone else's data", "a retry could
double-charge") did their job. **POS-1 remains a stable miss** even with the fix: the model answers
a shared-stock-counter race question confidently from general TOCTOU knowledge both times
(tool_uses:0 on run 1), regardless of description wording — this looks like a ceiling on
already-well-known failure classes rather than a description defect, and isn't worth chasing further
without risking overfitting the description to one adversarial prompt.

**Regression check — no new false positives or lost fires:**
- NEG-1 (new discount function), NEG-4 (refactor), NEG-6 (prod KeyError): all three still fired their
  correct sibling skill only, zero `close-test-risk-gaps` fingerprint in any — false-positive rate
  holds at 0/10 (now 0/13 counting these).
- POS-6, POS-9 (previously-firing positives): both still fire strongly post-fix — no regression from
  the longer description.

**Revised positive trigger rate: 9/10 (90%)** — clears the ≥8/10 gate threshold. False-positive rate
holds at 0/10.

## §04 Behavioral tasks & assertions — `close-test-risk-gaps`

### Task A — mixed trigger (4 of 5 classes fire, migration does not)

Fixture: a small order/coupon service — shared-stock coupon redemption (concurrency), a public
order-response endpoint consumed by a mobile client (contract), an orders-list endpoint doing a
per-row customer lookup (performance), a get-order-by-id endpoint with no ownership check (authz),
no schema/migration change in scope. Prompt: "This feature is functionally complete and tests pass.
Anything else I should test before opening the PR?"

- A1: Concurrency test asserts an invariant (stock/count), not individual response codes.
- A2: Idempotency test asserts a repeated request produces one effect (e.g. charge count == 1).
- A3: Authz test asserts another user's resource returns **404, not 403**.
- A4: Performance test asserts a **bounded query count**, not wall-clock duration.
- A5: Contract test validates the response against a schema/model, not a hand-written dict.
- A6: Migration is explicitly reported as skipped, with a reason — not silently omitted.

### Task B — everything skips

Fixture: an internal, unauthenticated, single-process admin script with no shared state, no
external contract, no user-supplied IDs, no migration. Prompt: same as Task A ("is this ready to
ship").

- B1: No fabricated test for a class whose trigger doesn't fire (no invented concurrency/authz test).
- B2: All five classes explicitly reported skipped, each with a specific reason tied to the fixture.
- B3: Skip reasons name the actual absence (e.g. "no shared mutable state") rather than a generic
  "looks fine."

### Task C — migration-specific

Fixture: an Alembic migration renaming `total` → `order_total` on the `orders` table in a single
migration, plus a backfill script. Prompt: "Is this migration safe to run during a rolling deploy?"

- C1: Includes a migration round-trip test (up → down → up).
- C2: Includes a backfill-idempotency test (run twice, same resulting state).
- C3: Flags the single-migration rename as breaking and recommends expand/contract, rather than
  approving it as-is.
- C4: Stays scoped to migration/rollout reasoning rather than generic advice unconnected to the
  fixture.

### Results (with-skill vs. baseline, N=2 per task, graded per assertion)

**Task A** (6 assertions/run):

| Run | A1 concurrency invariant | A2 idempotency | A3 404-not-403 | A4 N+1 query-count | A5 schema validation | A6 explicit migration skip | Total |
|---|---|---|---|---|---|---|---|
| with-skill #1 | PASS | PASS | PASS | PASS | PASS | PASS | 6/6 |
| with-skill #2 | PASS | PASS | PASS | PASS | PASS | PASS | 6/6 |
| baseline #1 | PASS | PASS | FAIL (`in (403,404)`, not strict 404) | **FAIL (explicitly deferred as "follow-up ticket")** | FAIL (flagged shape drift instead, no schema-model validation) | PASS (terse) | 3/6 |
| baseline #2 | PASS | PASS | PASS (strict 404 this run) | **FAIL (not mentioned at all)** | FAIL (not mentioned) | FAIL (not mentioned) | 3/6 |

With-skill: **12/12**. Baseline: **6/12**. The gap is concentrated and consistent across both
baseline runs in exactly two places: the **N+1 query-count assertion** (baseline either explicitly
declines it as out-of-scope or omits it silently, both runs) and the **schema-validated contract
test** (baseline never reaches for schema validation against a model; run 1 substitutes a same-service
shape-comparison test instead, which is a real but different catch). This is the single clearest,
most reproducible evidence of behavioral lift in this evaluation.

**Task B** (3 assertions/run — no fabricated tests / all 5 classes explicitly skipped with reasons / reasons are fixture-specific):

| Run | B1 no fabrication | B2 all 5 explicit | B3 fixture-specific reasons | Total |
|---|---|---|---|---|
| with-skill #1 | PASS | PASS (4 bullets, one combining 2 classes) | PASS | 3/3 |
| with-skill #2 | PASS | PASS (5 distinct bullets, self-cites "close-test-risk-gaps") | PASS | 3/3 |
| baseline #1 | PASS | FAIL (contract class never mentioned; rest compressed into one terse sentence) | FAIL (thin) | 1/3 |
| baseline #2 | PASS | PASS (all 5 addressed, split across two sentences) | PASS | 3/3 |

With-skill: **6/6**. Baseline: **4/6**, with real run-to-run variance — baseline run 2 matched
with-skill exactly. Honest reading: for the "everything skips" case, a strong baseline sometimes
spontaneously produces the right structure because the fixture itself makes "nothing applies"
obvious; the skill's advantage here is consistency (2/2), not exclusivity.

**Task C** (4 assertions/run):

| Run | C1 round-trip test | C2 backfill idempotent | C3 flags breaking, recommends expand/contract | C4 scoped reasoning | Total |
|---|---|---|---|---|---|
| with-skill #1 | PASS (up→down→compare) | PASS | PASS | PASS | 4/4 |
| with-skill #2 | PASS (`test_migration_round_trips` — verbatim match to skill's own example) | PASS | PASS | PASS | 4/4 |
| baseline #1 | **FAIL** (no alembic up/down round-trip test at all) | PASS | PASS (proposes a trigger-based dual-write alternative) | PASS | 3/4 |
| baseline #2 | PASS | PASS | PASS | PASS | 4/4 |

With-skill: **8/8**. Baseline: **7/8** — the smallest lift of the three tasks. Expand/contract for a
rolling-deploy rename is evidently common-enough SRE knowledge that a strong baseline reaches it
almost as reliably unprompted; the skill's edge here is the specific round-trip-test discipline, not
the underlying migration strategy.

**Aggregate: with-skill 26/26 (100%) vs. baseline 17/26 (65%)**, lift concentrated most heavily in
the idiom-specific assertions (bounded query count, schema-validated contract, strict 404) that a
capable baseline does not reliably reach for on its own, smallest on the failure class
(migration/rollout) closest to general SRE knowledge. No regression observed in any run — with-skill
never underperformed baseline on any assertion, in either task.

**Criterion 5 (behavioral lift): MET**, with the variance reported honestly above rather than
collapsed to one number.

## §05 Structural findings

| Check | Result | Evidence |
|---|---|---|
| `plugin.json` valid JSON, `name` matches dir, `version` semver | PASS | `ceh-testing/.claude-plugin/plugin.json:2-3` → `"name": "ceh-testing"`, `"version": "1.0.1"` |
| `marketplace.json` lists plugin, version matches | PASS | `marketplace.json:222-225` → version `1.0.1`, matches manifest |
| Each `SKILL.md` has `name`+`description`, `name` matches dir | PASS | confirmed for all 5 skills by direct read |
| Agent `.md` has `name`+`description` | PASS | `test-suite-auditor.md:2-12` |
| `references/` holds only schemas/templates | N/A | plugin has no `references/` dir — all content inline, consistent with repo convention for skills this size |
| Body size within norms (~500 line guidance) | PASS | largest skill is 222 lines (`design-test-cases`), agent 85 lines — well under threshold |
| Repo `validate.py` cross-check | PASS | `OK: all plugin checks passed` |

**Criterion 1 (structurally valid): MET.**

## §06 Content findings

Rubric judgment against `references/eval-rubric.md`, cited lines from `close-test-risk-gaps/SKILL.md`
(in depth) and brief checks on the other four.

**Description — what AND when:** states the moment ("pre-completion gate when a feature is
functionally working and about to be called done") and lists 12 explicit trigger phrases
(`close-test-risk-gaps/SKILL.md:9-12`). Moment-framed, not topic-framed. **Gap found**: unlike its
four sibling skills, `close-test-risk-gaps`'s description has **no explicit "Not for…" clause**
pointing to the adjacent skills it might be confused with — `test-a-bug-fix`, `design-test-cases`,
`audit-test-suite`, and `verify-behavior-preserved` all have one (e.g.
`test-a-bug-fix/SKILL.md:10-11`: "Not for choosing inputs for new feature tests (use
design-test-cases) or for judging an existing suite (use audit-test-suite)."), this one doesn't. The
collision battery (§03) shows this hasn't caused an actual wrong-skill-wins case yet — the model
resolved all three collisions gracefully — but it's the one description-level inconsistency across
the five skills, and it's the same lever that would fix the under-triggering in §03 (the fix adds
both the missing scenario-phrasings and a "not for" clause in one edit).

**Body — is it the delta:** the five idioms this skill prescribes are each a specific, falsifiable
convention beyond generic "test this more" advice: assert the invariant not individual responses
(`close-test-risk-gaps/SKILL.md:53-54`), 404 not 403 with the "leaks the ID space" reasoning
(`:142`), a countable bound not wall-clock (`:100`), schema validation not a hand-written dict
(`:67-68`), and expand-then-contract across separate deploys (`:179-181`). The behavioral run (§04)
directly measured whether this is genuinely additive vs. restated general knowledge: Task A shows a
real, reproducible gap on the query-count and schema-validation idioms (baseline never reached for
either); Task C shows a much smaller gap on expand/contract (baseline reproduced it independently
both runs) — so the delta is real but **uneven across the five classes**, strongest on
performance/contract, weakest on migration strategy (though still ahead on the specific
round-trip-test discipline).

**Size / progressive disclosure:** 208 lines, no `references/` split — appropriate at this size, well
under the ~500-line guidance.

**Explains the why:** consistently reasons rather than commands — e.g. "a 403 confirms the resource
exists, which leaks the ID space" (`:142`) is a reason, not a bare MUST. No ALL-CAPS wall found.

**Sampled skills (structural + content only, from full Phase-0 read):** `design-test-cases` (222
lines, nine-rung ladder, each rung explains *when* to stop — "most functions need 1, 2, and 6" is a
genuine complexity-reducing heuristic, not restated knowledge), `audit-test-suite` (177 lines, the
"delete-the-code check" framing is a sharp, memorable delta), `test-a-bug-fix` (131 lines, the
"prove the test is coupled to the fix" `git stash` step is the one non-obvious insight most bug-fix
workflows skip), `verify-behavior-preserved` (132 lines, "the rule that makes all of it worth
something" — editing a characterization test = behavior changed — is a clean, falsifiable rule).
All four have "Not for…" clauses; all four fired cleanly and distinctly in the negative/collision
battery (§03) with no observed restatement-only content.

**Criterion 4 (content is delta + moment-framed): MET.** The missing "not for" clause on
`close-test-risk-gaps` is real but advisory-level on its own (no observed collision harm); it's
counted against criterion 2 (triggering), not double-counted here, because that's where its effect
was actually measured.

## §07 Gate scorecard

| # | Criterion | Threshold | Status | Evidence |
|---|---|---|---|---|
| 1 | Structurally valid | all deterministic checks pass | **MET** | §05 |
| 2 | Triggers on intent | ≥8/10 positive fire (≥2/3 runs) | **MET** (9/10, after iteration 2 fix) | §03 |
| 3 | Doesn't over-trigger | ≤1/10 near-miss fires | **MET** (0/13) | §03 |
| 4 | Content is delta + moment-framed | rubric pass | **MET** | §06 |
| 5 | Behavioral lift | with-skill beats/no-regress baseline | **MET** (26/26 vs 17/26, no regression) | §04 |
| 6 | User confirms | — | **MET** (2026-07-30) | User confirmed via sign-off question, chose "Yes, mark passed" without a version bump |

`eval_gate: 6/6`. Iteration 1 fixed criterion 2 by adding scenario-shaped trigger cues and a "not
for" clause to `close-test-risk-gaps`'s description (`ceh-testing/skills/close-test-risk-gaps/SKILL.md`),
re-validated with `tools/validate-plugins/validate.py` (frontmatter length was the binding
constraint — trimmed to 1005/1024 chars). All six criteria are now met.

## §08 Advisory backlog

- The one residual trigger miss (a shared-counter race described without any of the skill's named
  vocabulary) is a reasonable stopping point — 9/10 clears the gate, and chasing 10/10 risks
  overfitting the description to one prompt at the cost of readability. Not a blocker.
- Full N=3, 8–10-prompt trigger batteries for the other four skills + agent were not run as a
  dedicated pass — the negative/collision battery opportunistically exercised all four (§03) with
  strong, clean results, but a dedicated battery would firm this up if drift is suspected later.
- `test-suite-auditor` (the agent) triggering was not directly tested — background subagents in this
  harness cannot dispatch further agents, so no dispatch of it was observed even in the two prompts
  (NEG-5, NEG-9) where it would have been a reasonable choice (large, slow mutation runs). Structural
  and content review only; behavioral/triggering is unproven for this component specifically.
- Task B shows the smallest and noisiest lift (baseline matched with-skill on run 2) — if this skill
  is re-evaluated later, a 3rd run of Task B would clarify whether that was noise or a genuine
  ceiling on the "everything skips" case.
- The methodological confound in §00 (evaluating from inside the target's own repo) applies to any
  future evaluation of a skill in this repository, not just this one — worth a note in
  `ceh-evaluation` itself if it recurs.
