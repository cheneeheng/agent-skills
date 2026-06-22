---
artifact: SKILL_EVAL
status: draft
created: 2026-06-21
updated: 2026-06-21
target: ceh-agent-coding-contract/skills/write-less-code/SKILL.md
target_kind: skill
eval_gate: 4/6
iterations: 1
---

## §01 Verdict

`write-less-code` is a minimalism-reflex skill: before writing code, climb a 6-rung ladder (YAGNI →
stdlib → native platform → installed dep → one line → minimal custom), mark deliberate shortcuts
with `// less-code:` ceiling comments, keep prose shorter than code, and leave one runnable check
behind non-trivial logic — without simplifying away validation/security/a11y. It is structurally
clean, content-rich (explains *why*, 65 lines), and **never over-triggers** (0/10 near-miss
false-positives; it correctly declined to push laziness on a "do it properly" OAuth2 request and
routed dep-removal to `dependency-management`). Behavioral lift is **real but modest**: a capable
model is already minimalist by default, so the skill's measurable delta is the repo *house-style
artifacts* (ceiling comments, the `skipped: X, add when Y` Output pattern, an embedded runnable
check) and a harder push to native-over-library — not raw "less code." No correctness regression.

**The one failing criterion is triggering (criterion 2): the skill severely under-invokes — 3/10
positive prompts loaded it, despite ~7/10 recognizing it as the most-relevant skill.** Cold
subagents repeatedly said, in effect, "the answer is short enough that pulling the skill in adds
nothing." The description summarizes the whole approach so completely that loading the body feels
redundant — so the body's unique artifacts (which *are* the lift) often never reach the model. The
highest-leverage fix: **make the description advertise the body's concrete deltas** (ceiling-comment
format, Output pattern, test-leaving rule) rather than re-summarizing minimalism, giving the model a
reason to load it. See §03/§08.

> **Reframing caveat (matters for how hard criterion 2 should bite).** The skill is hook-supplemented
> (see the dual-delivery note below): the always-on `UserPromptSubmit` hook already carries the
> *reflex* on every main-session turn, so under-invocation of the skill does **not** mean the user
> loses minimalism in practice — only that the *deeper* body artifacts are delivered inconsistently.
> Under that lens the generic ≥8/10 threshold is arguably the wrong bar for this skill. The report
> scores criterion 2 as unmet by the default threshold but flags this as a judgment call for the
> user (criterion 6).

> **Loop status — stopped by user at iteration 1.** The user chose to leave this as an honest draft
> rather than apply the criterion-2 fix or re-threshold. Status stays `draft`, `eval_gate: 4/6`.
> No edits were made to the skill; the proposed description rewrite remains an advisory in §08 A1'.
> The skill is well-built and safe to ship as-is (0 false-positives, no regression) — the open item
> is that its on-demand body artifacts reach the model on only ~3/10 substantive coding moments.

> **Architectural note that reshapes this eval — dual delivery.** The skill ships *two* delivery
> paths (see `ceh-agent-coding-contract/hooks/hooks.json`): a `UserPromptSubmit` hook
> (`less-code-payload.sh`) injects a **condensed ladder on every prompt** in the main session, and
> the **full SKILL.md loads on-demand** via description triggering. Consequences:
> - The *reflex* (ladder + the "never simplify away" line) reaches the main agent on every turn
>   regardless of skill triggering. So the skill's triggering only governs the **deeper delta**:
>   the Rules block, the `// less-code:` ceiling-comment format, the Output pattern, and the
>   test-leaving discipline.
> - Subagents (Agent-tool invocations) do **not** receive the `UserPromptSubmit` hook, so a cold
>   subagent battery cleanly isolates the *skill alone*. The baseline subagent has neither hook nor
>   skill — which means measured behavioral lift over-states the skill's *marginal* real-world value
>   (where the hook already carries the reflex). This limit is stated in §04.

## §02 Derived criteria

**Claim.** Before writing code for a non-trivial task, reach for the smallest thing that actually
works by climbing the ladder; refuse unrequested abstractions; mark deliberate shortcuts with
`// less-code:` (naming ceiling + upgrade path); keep the explanation shorter than the code; leave
one runnable check behind non-trivial logic — while never simplifying away trust-boundary
validation, data-loss handling, security, accessibility, or anything explicitly requested.

**Trigger intent.**
- *Should fire:* about to implement a non-trivial feature; user says "write less code", "be lazy",
  "lazy mode", "simplest/minimal solution", "yagni", "do less", "shortest path"; user complains of
  over-engineering, bloat, boilerplate, or unnecessary dependencies.
- *Should NOT fire (near-misses sharing keywords):* refactoring existing code for readability
  (adjacent, not new-code minimization); debugging / bugfix with no new code; reviewing someone's PR
  (→ `code-review`); performance optimization (often *adds* code); removing a dependency
  (→ `dependency-management`); writing tests as the primary task; project scaffolding
  (→ `scaffolding`); a knowledge question about a library; an explicit request for the
  full/production/"do it properly" version.

**Intended outcome vs no-skill baseline.** On a task a naive agent would over-build (custom class,
new dependency, abstraction layer), the with-skill agent ships a markedly smaller solution
(stdlib/native/one-liner, no new dep, no speculative abstraction) and states what it skipped and when
to add it — while preserving validation/security where the task crosses a trust boundary.

## §03 Trigger battery

Threshold (defaults): positive fires if ≥2/3 runs trigger; pass = ≥8/10 positives fire;
over-trigger pass = ≤1/10 near-misses fire. **Status: RUN, N=3 positives / N=2 negatives** (raw:
`iteration-1/run1-raw.md`, `runs2-3-raw.md`). "Fires" = skill *invoked* via the Skill tool;
"recognized" = named most-relevant but not invoked.

**Result — positives: 3/10 fire (FAIL vs ≥8).** P2 (3/3), P1 (2/3), P3 (2/3) fired; P4 (1/3) and
P5–P10 (0/3) did not. Recognition was far higher (~7/10 named write-less-code most-relevant) — the
gap is *invocation*, not relevance. Representative non-invoke rationale (P3): *"the answer is short
enough that pulling it in adds nothing."*

**Result — negatives: 0/10 false-positives by threshold (PASS).** One soft hit: N9 (scaffold a
python service) invoked write-less-code in 1/2 runs while naming scaffolding most-relevant. Strong
correct-decline evidence: N7 (production OAuth2 "do it properly") did **not** push laziness in any
run; N5 (remove lodash) routed to `dependency-management`; N3 (review PR) named `code-review`.

**Diagnosis.** Under-invocation, not over- or mis-triggering. Recognition is high, so broadening
phrasings won't help. The description telegraphs the entire method, so the model concludes the body
is redundant. Fix = advertise the body's *non-obvious artifacts* so loading pays off (see §08 A1').

**Positives (10):**
1. "ok i need to add a feature where users can export their dashboard to csv. can you just write the least amount of code for this"
2. "be lazy on this one — parse the ISO timestamps in this log file and bucket them by hour"
3. "i think this is getting over-engineered, we've got a FieldValidatorFactory and three strategy classes for what's basically trimming whitespace. help"
4. "yagni — do i really need a whole settings module for these two flags?"
5. "add a debounce to the search input"  *(feature; native-vs-lib decision territory)*
6. "we need to dedupe a list of dicts by the 'id' key before inserting. what's the simplest way"
7. "before you build this rate limiter, what's the shortest path that actually works?"
8. "implement a function that returns the nth fibonacci, but don't gold-plate it"
9. "this PR adds 400 lines of boilerplate to register one new event type. there has to be less"
10. "i want to validate that an uploaded file is a real PNG before saving. keep it minimal, no new deps"

**Near-miss negatives (10):**
1. "this function is 200 lines and impossible to follow, can you refactor it into smaller pieces"  *(refactor for readability; 'smaller' is the trap)*
2. "the checkout endpoint is throwing a 500, can you figure out why"  *(debugging, no new code)*
3. "review my PR and tell me if the approach is sound"  *(→ code-review)*
4. "this query is slow, can you optimize it"  *(perf; often adds code)*
5. "remove the lodash dependency, we only use it in one place"  *(→ dependency-management)*
6. "write comprehensive unit tests for the payment module"  *('comprehensive' is anti-lazy)*
7. "i need a production-grade, fully validated OAuth2 flow with refresh-token rotation — do it properly, don't cut corners"  *(explicit full version; deliberately ambiguous — may trigger-then-defer)*
8. "explain how Python's functools.lru_cache works"  *(knowledge question)*
9. "set up the directory structure and config for a new python service"  *(→ scaffolding)*
10. "the build is failing on CI with a mypy error in models.py, fix it"  *(bugfix, no minimization intent)*

## §04 Behavioral tasks & assertions

**Status: RUN, N=2 per arm, neutral task phrasing** (raw: `iteration-1/behavioral-raw.md`).
Baseline = no skill, no hook. Limit: baseline lacks the always-on hook, so this measures
skill+reflex vs nothing — it *over*-states the skill's real-world marginal value (where the hook
already supplies the reflex), yet lift still came out modest.

**Headline:** the **baseline is already strongly minimalist** — stdlib over dependencies, small
functions, no speculative abstractions — without the skill. So raw "less code" is not where lift
lives. Measured, reproducible lift (both runs):
- **Task A (business days):** both arms used stdlib, no dependency (A1/A2/A4 tie). With-skill added
  the `// less-code:` ceiling comment, the `skipped: X, add when Y` line, and an *embedded runnable
  assert*; baseline only gestured at alternatives in prose. → modest lift, artifacts only.
- **Task B (React email):** with-skill shipped native `type="email" + required` only and stated the
  skip; baseline built a regex + error-state + `aria` layer (heavier, but added accessibility the
  lean version leans on the browser for). → real leanness lift, with a UX/a11y trade-off worth
  noting.
- **Task C (CSV sum, guardrail):** both got money right (`Decimal`); baseline volunteered
  malformed-row tolerance the with-skill version documented as a deliberate skip. → no minimalism
  lift; baseline slightly more robust.

**No correctness regression anywhere.** Net: lift is genuine but narrow (artifacts + native-first),
and in two arms the baseline delivered *more* robustness/UX — "less" is not unconditionally
"better." This is the evidence-backed reason the dual-delivery design is sensible: cheap always-on
reflex via the hook, on-demand house-style discipline via the skill.

**Task A — over-build temptation (stdlib over dependency).**
"Add a function that returns the number of business days between two dates, excluding weekends."
- A1: adds **no new third-party dependency** — stdlib `datetime` only (baseline may reach for
  pandas/numpy `busday_count`).
- A2: a single small function, **no class/abstraction**.
- A3: states what was skipped / when to add a lib (e.g. holiday calendars) — the Output pattern.
- A4 (guardrail): weekend exclusion is actually **correct** (lazy ≠ wrong).

**Task B — native over library (frontend).**
"Add validation to our React email field: it must be a valid email and required."
- B1: uses **native HTML5 validation** (`type="email"`, `required`) over adding a validation lib.
- B2: **no new dependency** (no zod/yup/react-hook-form).
- B3: states what was skipped (e.g. custom error UI) and the upgrade path.

**Task C — guardrail (don't over-simplify a trust boundary).**
"Quickly parse this user-uploaded CSV of bank transactions and sum the amounts — the lazy version is
fine."
- C1: despite "lazy version is fine," **validates/handles malformed or non-numeric input** (trust
  boundary preserved per the skill's "When NOT to be lazy"). Discriminates against a naive-lazy
  baseline that skips validation.
- C2: still minimal — no over-built parsing framework.

## §05 Structural findings

| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter parses; `name`/`description`/`license` present | PASS | lines 1-13 |
| `name` matches directory | PASS | `name: write-less-code` == dir `write-less-code` |
| Description non-trivial | PASS | 8 lines, states what + when (lines 4-11) |
| Body non-trivial | PASS | 65 lines, multiple structured sections |
| `references/` discipline | PASS | no `references/` dir — none needed at this size |
| Repo `validate.py` cross-check | PASS | `OK: all plugin checks passed` |

**Criterion 1 (structurally valid): MET.**

## §06 Content findings

Judged against `references/eval-rubric.md`, with cited lines.

- **States what AND when — PASS.** What: "Reach for the smallest solution that actually works…
  custom code last" (desc lines 4-11). When: "Load proactively before implementing a feature, and
  whenever the user says 'write less code'… 'yagni'… or complains about over-engineering, bloat,
  boilerplate" (lines 7-11).
- **Moment not topic — PASS.** "before implementing a feature" is a moment; trigger phrases are
  situational, not a noun/topic.
- **Slightly pushy — PASS.** "Load proactively" + a long explicit phrasing list (lines 7-11).
- **Names what it is NOT for — PARTIAL.** Body line 18-20 points to `agent-coding-contract` for the
  negative half, but neither description nor body names the *adjacent near-miss* skills (refactor,
  code-review, dependency-management, perf). **Prediction reconciliation:** I initially flagged this
  as the highest-leverage gap, expecting it to drive false-positives. The N=2 negative battery
  **disproved that** — false-positives are 0/10; the model disambiguates the near-misses correctly on
  its own. So this is downgraded to advisory insurance (§08 A2), and the real highest-leverage gap
  turned out to be the opposite failure mode: *under*-invocation from a description that re-summarizes
  rather than advertises the delta (§03 diagnosis).
- **Description re-summarizes the method instead of advertising the body — the confirmed gap.** Lines
  4-11 lay out the entire ladder (YAGNI → stdlib → native → dep → one line → custom). That reads as
  the complete approach, so a model that already knows minimalism concludes the body adds nothing and
  declines to load it (3/10 invocation, §03). The body's genuinely non-obvious artifacts — ceiling
  comment format (line 42), Output pattern (line 50), runnable-check rule (lines 58-61) — are not
  surfaced in the description, so they don't motivate a load.
- **Body is the delta — PASS (with note).** The genuine, non-obvious delta: the `// less-code:`
  ceiling-comment format with upgrade path (line 42), the Output pattern `[code] → skipped: [X], add
  when [Y]` (line 50), the "leave ONE runnable check… an assert-based self-check" discipline (lines
  58-61), the edge-case tie-break (line 41). Note: rungs 2-5 of the ladder (stdlib/native/one-line)
  restate general knowledge a strong model already has — justified here as a *memorable reflex* and
  because the hook, not the skill body, is the reflex's primary carrier.
- **Explains why over MUSTs — PASS.** "clever is what someone decodes at 3am" (line 39); "every
  paragraph defending a simplification is complexity smuggled back as prose" (line 48); "so a
  shortcut reads as intent, not ignorance" (line 42). Reasoning-rich; ALL-CAPS used sparingly.
- **Size / progressive disclosure — PASS.** 65 lines, far under ~500; no reference split needed.
- **Least surprise — PASS.** Nothing deceptive; behavior matches the description.

**Criterion 4 (content is delta + moment-framed): MET, with one advisory (add NOT-for pointers).**

## §07 Gate scorecard

| # | Criterion | Status | Evidence / threshold |
|---|-----------|--------|----------------------|
| 1 | Structurally valid | **MET** | All §05 checks pass; validate.py `OK: all plugin checks passed` |
| 2 | Triggers on intent | **UNMET** | §03 — 3/10 positives invoke (threshold ≥8). Under-invocation, not mis-trigger; recognition ~7/10. The one blocking gap. |
| 3 | Does not over-trigger | **MET** | §03 — 0/10 false-positives by threshold (one soft 1/2 on N9 scaffolding) |
| 4 | Content is delta + moment-framed | **MET** | §06 — delta present, moment-framed, why-driven, 65 lines; advisory: description re-summarizes vs advertises the delta |
| 5 | Behavioral lift | **MET (modest)** | §04 — with-skill clears artifact/native-first assertions baseline misses; no correctness regression; lift narrow because baseline already minimalist |
| 6 | User confirms | PENDING | — |

**eval_gate: 4/6.** Lowest/blocking criterion: **#2 triggering.** The leverage move is **not** more
trigger phrasings (recognition is already high) — it is rewriting the description to advertise the
body's concrete, non-obvious artifacts so the model loads it instead of concluding it already knows
the approach. See §08 A1'. Note the §01 reframing caveat: if the user decides the hook-supplemented
role makes the ≥8/10 default the wrong bar, criterion 2 could be re-thresholded — that is a
criterion-6 judgment, not an evidence change.

## §08 Advisory backlog

- **A1' (highest-leverage, blocks criterion 2):** The description re-summarizes the minimalism method
  the model already knows, so it under-invokes. Reframe it to advertise the *body's* deltas — e.g.
  "…loads the repo's `// less-code:` ceiling-comment format, the `skipped: X, add when Y` output
  pattern, and the leave-one-runnable-check rule." Give the model a reason to open the body. Expected
  effect: raise invocation on substantive coding moments without touching the (already clean)
  false-positive rate.
- **A2 (advisory):** Add a one-line "Not for…" pointer (refactor existing code → simplify/refactor;
  review → `code-review`; dep removal → `dependency-management`). False-positives are already 0/10 so
  this is insurance, not a fix — but it firms up the soft N9 scaffolding hit.
- **A3 (advisory):** State in the SKILL.md body that the always-on hook carries the reflex and the
  skill carries depth, so a reader understands the division (currently only the hook script's shell
  comment explains it). Also clarifies *why* the body can assume the ladder is already in context.
- **A4 (advisory):** The Task B/C trade-off — leaner output occasionally dropped accessibility / a
  robustness affordance the baseline volunteered. The "When NOT to be lazy" section already lists
  a11y and trust-boundary validation; consider sharpening it so the lean path doesn't silently shed
  a volunteered safeguard.
