# Skill Evaluation Report Schema

The artifact this skill produces. One file, `SKILL_EVAL.md`, written to the target's eval folder
under `.agents_workspace` — `.agents_workspace/skill-evals/<target-name>/SKILL_EVAL.md`, where
`<target-name>` is the skill or plugin name — never next to the target itself. It is a **living
document**: each fix/re-run loop revises it in place, not a fresh copy. Raw run outputs live in that
same folder's `iteration-<N>/` subdirectory
(`.agents_workspace/skill-evals/<target-name>/iteration-<N>/`) and are referenced from the report,
not pasted into it.

## Frontmatter

```yaml
---
artifact: SKILL_EVAL
status: draft              # draft | passed   (passed = gate 6/6 + user confirmed)
created: YYYY-MM-DD
updated: YYYY-MM-DD
target: <path to the evaluated SKILL.md or plugin dir>
target_kind: <skill | plugin>
eval_gate: 0/6             # criteria met out of 6 (see Readiness Gate below)
iterations: 0              # how many measure/fix loops have run
---
```

## Sections

| ID | Title | Content |
|----|-------|---------|
| §01 | Verdict | Two or three sentences: what the target does, whether it is ready, the single highest-leverage gap. Written **last**, regenerated each loop. |
| §02 | Derived criteria | The target's own bar (Phase 1): the **claim**, the **trigger intent** (should-fire / should-not-fire), and the **intended outcome** vs a no-skill baseline. Everything below measures against this. |
| §03 | Trigger battery | The positive (8–10) and near-miss negative (8–10) prompts used, and the measured trigger rate / false-positive rate per run set. |
| §04 | Behavioral tasks & assertions | The 2–3 tasks, each with its discriminating assertions and the with-skill vs baseline grading result across N runs (with variance). |
| §05 | Structural findings | Per-check pass/fail with evidence; any cross-check tool output and how a disagreement was reconciled. |
| §06 | Content findings | Rubric judgments with **cited lines** as evidence — delta vs restatement, moment vs topic, size/progressive-disclosure, why vs MUSTs. |
| §07 | Gate scorecard | The 6 criteria, each met/unmet with its one-line evidence. The `eval_gate: N/6` source of truth. |
| §08 | Advisory backlog | Non-blocking improvements found along the way, so a passed skill still has a to-do list. |

Each finding carries its **evidence inline** — a trigger count, a quoted line, a with/baseline
assertion delta. A finding without evidence is an opinion, not a measurement, and does not move the
gate.

## Readiness Gate

The loop exit condition. The target is **ready** (`status: passed`) only when all six criteria are
met **and** the user explicitly confirms. Each loop, score the gate honestly in frontmatter
(`eval_gate: N/6`) and name the lowest-scoring criterion as the next target.

A criterion is "met" only when **evidence** supports it — a measured rate, a cited line, a graded
delta. Honest "unproven" is not "met"; a fabricated pass is worse than an open criterion.

1. **Structurally valid** — every deterministic structural check passes (frontmatter, name/dir
   match, description present, body non-trivial, references discipline; for a plugin also manifest +
   marketplace version match).
2. **Triggers on intent** — positive trigger rate ≥ **threshold** across N runs (default: fires in
   ≥ 8 of 10 positive prompts, counting a prompt as firing if it triggers in ≥ 2 of 3 runs).
3. **Does not over-trigger** — near-miss false-positive rate ≤ **threshold** (default: fires on ≤ 1
   of 10 near-miss negatives).
4. **Content is delta + moment-framed** — the rubric pass in `eval-rubric.md`: the body is the
   repo/tool-opinionated delta, framed as a moment, within size norms, explains the why.
5. **Behavioral lift** — with-skill clears assertions the baseline misses (or, for a guardrail-style
   skill, holds a standard the baseline violates) **and does not regress** the baseline, with
   acceptable run-to-run variance. If lift cannot be simulated meaningfully, this criterion is
   **unproven** (not met) and the report says so.
6. **User confirms** — the author/user agrees the target is ready to ship.

Thresholds are defaults, not laws — a niche skill with five legitimate trigger phrasings sets its
own positive battery size. State the threshold actually used in §07 so the score is reproducible.

When fewer than 6 are met, the open criteria **are the agenda** — fix the lowest-scoring,
highest-leverage one, re-run only that dimension, re-score.
