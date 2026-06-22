---
artifact: SKILL_EVAL
status: draft
mode: lite
created: 2026-06-22
updated: 2026-06-22
target: ceh-agent-coding-contract/skills/write-less-code/SKILL.md
target_kind: skill
eval_gate: 3/6
iterations: 1
---

## §01 Verdict

`write-less-code` is the positive half of a minimalism reflex: before writing code, climb the 6-rung
ladder (YAGNI → stdlib → native platform → installed dep → one line → minimal custom), mark
deliberate shortcuts with `// less-code:` ceiling comments, keep prose shorter than code, and leave
one runnable check behind non-trivial logic. **Lite scope: dev-loop check, not a ship verdict.**
Structure (validate.py clean) and content (delta-rich, moment-framed, explains *why*) pass cleanly.

**Triggering is the gap, and this run resolves the run-001/run-002 contradiction in run-001's
favour.** Using the *correct* cold protocol (bare prompt, no skill-list priming), positives fired
**3–4 of 6** — under the 5/6 threshold and directionally consistent with run-001's cold 3/10, while
refuting run-002's primed 6/6. Near-miss false positives were **0/6** (over-triggering is not a
problem). A material confound depressed positives: subagents ran in this plugin repo's cwd with no
application code, so feature prompts derailed before they could be engaged. **Path to a real verdict:
`ceh-evaluation:evaluate-skill`, run in a real app sandbox** (N=3 cold + behavioral lift).

## §02 Derived criteria

- **Claim:** Before writing code, reach for the smallest thing that works via the 6-rung ladder;
  produce house-style artifacts (ceiling comments, `skipped: X, add when Y` output, native-over-lib,
  embedded runnable check) — without simplifying away validation/security/a11y/explicit requests.
- **Trigger intent — should fire:** implementing a feature; "write less code / be lazy / yagni /
  simplest / shortest path / minimal"; complaints about over-engineering, bloat, boilerplate,
  unnecessary dependencies.
- **Trigger intent — should NOT fire:** PR review (→ code-review); dependency *removal*
  (→ dependency-management); plain bugfix; "do it properly / full version, no shortcuts"; test
  authoring; large refactor for its own sake.
- **Intended outcome (recorded, NOT measured in lite — that is behavioral lift):** vs a no-skill
  baseline, the agent emits ceiling comments and the `skipped/add-when` pattern, prefers native
  platform features over libraries, and leaves a runnable check behind non-trivial logic.

## §03 Trigger battery (lite, N=1, corrected cold protocol)

6 positives / 6 near-miss negatives. Full table + per-probe evidence in
`iteration-1/triggering-results.md`. Summary:

- **Positive trigger rate: 3/6 clear (P1 native date input, P3 named skill + quoted full ladder, P6
  named "write-less-code reflex" + installed-dep-over-custom); 4/6 if P2's stdlib + DB-constraint
  signatures count.** Below the ≥5/6 threshold. P4/P5 missed — both the most contaminated by the
  no-app-code cwd.
- **Near-miss false-positive rate: 0/6.** No negative surfaced the skill, including the borderline
  refactor (N6) that run-002 feared would over-trigger.

**Resolves the prior contradiction:** run-001 (cold, correct) = 3/10; run-002 (primed) = 6/6; this
run (cold, correct) = 3–4/6. The corrected method reproduces **under-triggering**, confirming
run-001 and invalidating run-002's pass. N=1 + cwd confound ⇒ sanity read, not a statistic.

## §04 Behavioral tasks & assertions

**Skipped by design (lite).** Criterion 5 (behavioral lift) is unproven. run-001 found lift "real
but modest" (the house-style artifacts, not raw less-code) with no regression — not re-measured here.
Run `ceh-evaluation:evaluate-skill` for the paired with/baseline battery.

## §05 Structural findings

| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter parses | PASS | valid YAML, `name`/`description`/`license` present (SKILL.md:1-13) |
| `name` matches directory | PASS | `name: write-less-code` == dir `skills/write-less-code` |
| Description non-trivial + states when | PASS | lists explicit trigger phrases + "load proactively" (SKILL.md:6-11) |
| Body non-trivial | PASS | 65 lines: ladder + rules + output + guardrails |
| `references/` discipline | PASS (N/A) | no references dir; all content inline (appropriate at 65 lines) |
| Repo validator cross-check | PASS | `python tools/validate-plugins/validate.py` → "OK: all plugin checks passed" |

## §06 Content findings

Judged against `../evaluate-skill/references/eval-rubric.md`, with cited lines:

- **Delta, not restatement — PASS.** Repo-specific artifacts the model wouldn't default to: the
  `// less-code:` ceiling-comment convention with upgrade path (SKILL.md:42), the
  `[code] → skipped: [X], add when [Y]` output pattern (SKILL.md:50), "leave ONE runnable check …
  the smallest thing that fails if the logic breaks" (SKILL.md:58-60). Native-platform ladder
  examples (SKILL.md:28) are opinionated, not generic.
- **Moment, not topic — PASS.** "Load proactively before implementing a feature, and whenever the
  user says…" (SKILL.md:7-11).
- **Explains the why, not ALL-CAPS MUSTs — PASS.** "clever is what someone decodes at 3am"
  (SKILL.md:39); "every paragraph defending a simplification is complexity smuggled back as prose"
  (SKILL.md:48).
- **Size / progressive disclosure — PASS.** 65 lines, far under ~500; no split needed.
- **Names what it's NOT for — PASS.** "When NOT to be lazy" guardrails (SKILL.md:52-61) and explicit
  hand-off of the negative half to `agent-coding-contract` (SKILL.md:17-20).

No content red flags. One triggering-adjacent advisory in §08.

## §07 Gate scorecard (lite — max 4/6)

Thresholds used: positives fire ≥ 5/6; near-miss FP ≤ 1/6.

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Structurally valid | **MET** | all §05 checks pass; validate.py clean |
| 2 | Triggers on intent | **NOT MET** | 3–4/6 positives < 5/6 threshold; corroborates run-001's cold under-trigger, refutes run-002's primed 6/6. cwd confound depressed it; not a clean pass either way. |
| 3 | Does not over-trigger | **MET** | 0/6 near-miss false positives ≤ threshold |
| 4 | Content is delta + moment-framed | **MET** | §06 rubric pass, cited lines, within size norms |
| 5 | Behavioral lift | **UNPROVEN** | skipped by design (lite); see §04 |
| 6 | User confirms | **UNPROVEN** | not a lite concern |

`eval_gate: 3/6` — criteria 1, 3, 4 met; criterion 2 (triggering) **not met** under the corrected
cold protocol. Criteria 5–6 unproven, not met. Lite never sets `status: passed`.

## §08 Advisory backlog

- **Criterion 2 is the agenda — and the corrected method now agrees with run-001, so the
  under-trigger finding is no longer in doubt about direction.** Highest-leverage next step: full
  eval (`ceh-evaluation:evaluate-skill`) with N=3 cold runs **inside a real application sandbox**, so
  feature prompts can actually be engaged rather than derailing on missing app code. The cwd confound
  is the single biggest threat to a clean triggering number; fix it before trusting any rate.
- **Likely fix once confirmed (run-001's hypothesis, still standing):** the description so completely
  restates the ladder that a cold agent feels loading the body is redundant. The skill DID fire on
  the substantive, engageable prompts (P1, P3, P6) and missed the derailed ones — suggesting the
  description triggers acceptably *when the task is engageable*, and the larger lever may be the
  harness/environment, not the wording. Validate which in the full eval before editing the text.
- **N6 (refactor) did NOT over-trigger** here, retiring run-002's concern. No description tightening
  needed on that axis.
- **No description edit attempted this run.** A blind re-run would face the identical cwd confound
  and couldn't validate the change — the honest move is hand-off to the full eval, not a contaminated
  Phase-4 loop.
