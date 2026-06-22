---
artifact: SKILL_EVAL
status: draft
mode: lite
created: 2026-06-22
updated: 2026-06-22
target: ceh-agent-coding-contract/skills/write-less-code/SKILL.md
target_kind: skill
eval_gate: 4/6
iterations: 1
---

## §01 Verdict

`write-less-code` is the positive half of a minimalism reflex: before writing code, climb the 6-rung
ladder (YAGNI → stdlib → native platform → installed dep → one line → minimal custom), mark
deliberate shortcuts with `// less-code:` ceiling comments, keep prose shorter than code, and leave
one runnable check behind non-trivial logic. **Lite scope: this is a dev-loop check, not a ship
verdict.** Structure (validate.py clean), content (delta-rich, moment-framed, explains *why*), and —
*under lite's framing* — triggering all read clean: 6/6 positives fired, 1/6 borderline near-miss.

**The honest open question is triggering, and lite cannot settle it.** This run's 6/6 positive rate
directly contradicts the prior full eval (run-001: 3/10, severe under-trigger). The difference is
method: lite's subagent prompt asked agents to *deliberate and report which skills they'd load*,
priming skill-consideration; run-001 observed *natural* cold invocation. Lite's own rule applies —
N=1 with carried context is a sanity read, not a statistic — so the run-001 cold result is the more
trustworthy signal and the under-trigger problem likely stands. **Path to a real verdict:
`ceh-evaluation:evaluate-skill`** (N=3 cold natural-invocation triggering + behavioral lift).

## §02 Derived criteria

- **Claim:** Before writing code, reach for the smallest thing that works via the 6-rung ladder;
  produce house-style artifacts (ceiling comments, `skipped: X, add when Y` output, native-over-lib,
  embedded runnable check) — without simplifying away validation/security/a11y/explicit requests.
- **Trigger intent — should fire:** implementing a feature; "write less code / be lazy / yagni /
  simplest / shortest path / minimal"; complaints about over-engineering, bloat, boilerplate,
  unnecessary dependencies.
- **Trigger intent — should NOT fire:** PR review (→ code-review); dependency *removal*
  (→ dependency-management); plain bugfix; "do it properly / full version, no shortcuts"; test
  authoring; large refactor requested for its own sake.
- **Intended outcome (recorded, NOT measured in lite — that is behavioral lift):** vs a no-skill
  baseline, the agent emits ceiling comments and the `skipped/add-when` pattern, prefers native
  platform features over libraries, and leaves a runnable check behind non-trivial logic.

## §03 Trigger battery (lite, N=1)

6 positives / 6 near-miss negatives. Raw transcripts and the full table in
`iteration-1/triggering-results.md`. Summary:

- **Positive trigger rate: 6/6.** All six fired write-less-code (P1 native date input, P2 dep-free
  CSV, P3 explicit "write less code", P4 over-engineering complaint, P5 "yagni mode", P6 "lazy
  version first").
- **Near-miss false-positive rate: 1/6** (N6 refactor). N1/N2 correctly routed to code-review /
  dependency-management; N3/N4/N5 loaded nothing. N6 is borderline-legit (minimalism genuinely
  applies to a refactor), so effective FP is 0–1/6.

**Contradiction with run-001 (full eval): 6/6 here vs 3/10 there.** N=1 + a deliberate-choice
prompt frame inflated positives. This dimension is NOT settled by lite; flagged for the full eval's
N=3 cold natural-invocation re-check. Do not read 6/6 as a triggering pass.

## §04 Behavioral tasks & assertions

**Skipped by design (lite).** Criterion 5 (behavioral lift) is unproven. run-001 found lift "real
but modest" (the house-style artifacts, not raw less-code) with no regression — informative but not
re-measured here. Run `ceh-evaluation:evaluate-skill` for the paired with/baseline battery.

## §05 Structural findings

| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter parses | PASS | valid YAML, `name`/`description`/`license` present (SKILL.md:1-13) |
| `name` matches directory | PASS | `name: write-less-code` == dir `skills/write-less-code` |
| Description non-trivial + states when | PASS | lists explicit trigger phrases (SKILL.md:7-11) |
| Body non-trivial | PASS | 65 lines, ladder + rules + output + guardrails |
| `references/` discipline | PASS (N/A) | no references dir; all content inline (appropriate at 65 lines) |
| Repo validator cross-check | PASS | `python tools/validate-plugins/validate.py` → "OK: all plugin checks passed" |

## §06 Content findings

Judged against `../evaluate-skill/references/eval-rubric.md`, with cited lines:

- **Delta, not restatement — PASS.** Carries repo-specific artifacts the model wouldn't default to:
  the `// less-code:` ceiling-comment convention with upgrade path (SKILL.md:42), the
  `[code] → skipped: [X], add when [Y]` output pattern (SKILL.md:50), "leave ONE runnable check …
  the smallest thing that fails if the logic breaks" (SKILL.md:58-60). The ladder ordering +
  native-platform examples (SKILL.md:28) are opinionated, not generic.
- **Moment, not topic — PASS.** Description frames moments: "Load proactively before implementing a
  feature, and whenever the user says…" (SKILL.md:7-11).
- **Explains the why, not ALL-CAPS MUSTs — PASS.** "clever is what someone decodes at 3am"
  (SKILL.md:39); "every paragraph defending a simplification is complexity smuggled back as prose"
  (SKILL.md:48). Reasoning the model generalizes from.
- **Size / progressive disclosure — PASS.** 65 lines, far under ~500; no split needed.
- **Names what it's NOT for — PASS.** "When NOT to be lazy" guardrails (SKILL.md:52-61) and explicit
  hand-off of the negative half to `agent-coding-contract` (SKILL.md:17-20).

No content red flags. Minor advisory in §08.

## §07 Gate scorecard (lite — max 4/6)

Thresholds used: positives fire ≥ 5/6; near-miss FP ≤ 1/6.

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Structurally valid | **MET** | all §05 checks pass; validate.py clean |
| 2 | Triggers on intent | **MET (lite) — CONTESTED** | 6/6 positives, but contradicts run-001's cold 3/10; lite framing inflated it. Authoritative re-check pending in full eval. |
| 3 | Does not over-trigger | **MET** | 1/6 near-miss (N6, borderline-legit) ≤ threshold |
| 4 | Content is delta + moment-framed | **MET** | §06 rubric pass, cited lines, within size norms |
| 5 | Behavioral lift | **UNPROVEN** | skipped by design (lite); see §04 |
| 6 | User confirms | **UNPROVEN** | not a lite concern |

`eval_gate: 4/6` — the four lite-measurable criteria read as met, with criterion 2 carrying an
explicit contradiction flag. Criteria 5–6 are unproven, not met. Lite never sets `status: passed`.

## §08 Advisory backlog

- **Criterion 2 is the real agenda, and it's out of lite's rigor.** Do not trust 6/6. The
  highest-leverage next step is the full eval's N=3 cold natural-invocation triggering. run-001's fix
  hypothesis stands: the description so completely summarizes the approach that loading the body
  feels redundant to a cold agent — make the description advertise the body's *concrete deltas*
  (ceiling-comment convention, the skipped/add-when pattern) so the body's unique value pulls the
  skill in.
- N6 (refactor) firing write-less-code is arguably correct, not a defect — if the full eval also sees
  it, reclassify from near-miss to legitimate trigger rather than tightening the description.
