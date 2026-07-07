---
artifact: SKILL_EVAL
status: draft
created: 2026-07-07
updated: 2026-07-07
target: ceh-fabled/skills/fabled/SKILL.md
target_kind: skill
eval_gate: unscoped   # scoped run — behavioral lift only, per user request; gate not scored
iterations: 1
run_type: scoped-behavioral-lift-only
model: sonnet
note: >
  Independent from the concurrent run-001 evaluation under .agents_workspace/skill-evals/fabled/
  (a colleague's parallel session, different task design, model Opus). This folder is the
  Sonnet-side check, kept separate by the user's explicit request to avoid collision.
---

## §01 Verdict

On this single N=1 probe, **fabled produced no measurable correctness lift** over the baseline: both
the with-skill and no-skill subagent reached the identical correct root-cause diagnosis (the 3.00–3.05s
clustering is timeout truncation, not provider flakiness), the identical recommendation (raise the
timeout, don't retry blindly), and the identical key risk call-out (double-charge risk without
idempotency keys). The with-skill answer was more *legible* about its own process — an explicit
steelmanned counterargument for retry, and an explicit differentiated confidence statement — but this
didn't change what shipped. This is a scoped sanity check (user asked "does it help," explicitly waived
triggering); it is **not** a gate-passing evaluation and `status` stays `draft`. See §04 for why this
particular task may have been too easy to discriminate on, and what a sharper follow-up probe would
look like.

## §02 Derived criteria (scoped to what was measured)

- **Claim:** applying fabled's process (effort triage → understand → generate alternatives → work at
  depth → adversarial self-review → verify → deliver with calibrated conviction) closes most of the
  quality gap between a rushed answer and an excellent one, on non-trivial analysis/decision/debugging
  tasks.
- **Intended outcome vs. baseline:** an agent following fabled should be less likely to commit to the
  first plausible fix, more likely to surface the disconfirming evidence in the prompt, and more likely
  to deliver a single calibrated verdict rather than a hedged menu — where a baseline agent might not.
- **Scope of this run:** behavioral lift only (dimension 4). Triggering, structure, and content-rubric
  dimensions were explicitly out of scope per the user's request and are unmeasured here — see
  `ceh-evaluation:evaluate-skill-lite` for those, or the full `evaluate-skill` loop for the 6-point gate.

## §03 Trigger battery

Not measured — out of scope for this run (user: "no need to worry about trigger").

## §04 Behavioral task & assertions (N=1)

**Task:** a fintech incident-triage question with one competing-fixes decision (retry-with-backoff vs.
raise timeout), where the log evidence (failures clustered at 3.00–3.05s, uniform across payment method
and hour) is a fairly strong "smoking gun" for the correct answer if the agent actually reasons over it
rather than picking a fix by default preference. Both subagents were `general-purpose`, spawned in the
same turn. With-skill was instructed to invoke `Skill(skill="fabled")` first and follow its process;
baseline was explicitly instructed not to invoke any skill. Full task text and both transcripts:
`../../../../generated/sonnet/with-skill-answer.md`, `../../../../generated/sonnet/baseline-answer.md`
(repo-root `generated/sonnet/`, per user instruction).

| # | Assertion | With-skill | Baseline |
|---|-----------|:---:|:---:|
| 1 | Explicitly ties the 3.00–3.05s clustering to timeout truncation, not provider flakiness | PASS — *"That's not 'the provider is broken,' that's 'our client is hanging up on a call that was still in progress.'"* | PASS — *"That's not 'occasionally the provider is slow' — that's 'the timeout is cutting off requests that were about to succeed.'"* |
| 2 | Recommends raising the timeout as the primary today-fix, not retry-as-a-complete-fix | PASS — *"raise the timeout, don't add retry — at least not today"* | PASS — *"Raise the timeout (option 2) — but treat it as a stopgap"* |
| 3 | Delivers one concrete verdict, not a hedged menu | PASS — leads with a bolded verdict line | PASS — leads with a bolded recommendation line |
| 4 | Flags a second-order/follow-up risk beyond the immediate fix (double-charge/idempotency risk if retry added later, and/or a monitoring step to confirm the diagnosis) | PASS — explicit idempotency-key gating on any future retry, explicit "watch the new failure distribution" step, explicit follow-up to get the provider's real P99 | PASS — same idempotency-key call-out, same "watch checkout error rate and p99" step, same "if failures reappear at ~9-9.5s" follow-up |

**Result: 4/4 both sides, zero delta.** No assertion discriminated between the two conditions on this
task.

**Observed qualitative difference (not assertion-graded, but worth recording):** the with-skill
transcript visibly performed two of the skill's named stages that the baseline transcript didn't make
explicit:
- *Alternative generation / adversarial self-review (stage 2/4):* it steelmans the retry side before
  rejecting it — *"One honest counterargument for retry: if each attempt has an independent 2% chance of
  running long, two attempts naively gets you to 0.04%. But the flat 2% rate... argues against
  independence."* The baseline never states the opposing case before dismissing it.
- *Calibrated conviction (stage 6):* it splits confidence by claim — *"Confidence: high on 'raise the
  timeout, not retry'... Lower confidence on '10s' being the exact right number."* The baseline's
  confidence is implicit in phrasing ("stopgap, not the fix") rather than stated.

Neither difference changed the final recommendation or which assertions passed. This suggests the
lift here (if any) is in reasoning *legibility/rigor-signaling*, not in this task's correctness outcome.

**Confound to flag:** the with-skill transcript ends with a "Security/Dependency risk:" one-line flag,
which matches this repo owner's personal global `CLAUDE.md` response-formatting convention almost
exactly. Since both subagents ran in the same account/environment, this may reflect an inherited
user-level `CLAUDE.md` rather than anything the fabled skill itself specifies — fabled's SKILL.md has no
such flag-line instruction. Treat that one stylistic marker as noise, not skill signal.

**Why this probe likely under-discriminates:** the task's disconfirming evidence (exact-timeout
clustering, uniform across every dimension) is strong enough that a single capable pass — with or
without an explicit process — catches it. Fabled's stated failure modes it exists to prevent
(first-thought commitment, menu hedging, caveat patching) are more likely to separate the two
conditions on tasks where: (a) the "obvious" first fix is subtly wrong and the disconfirming signal is
buried rather than headlined, (b) there's a socially appealing but incorrect answer, or (c) the task
has enough moving parts that skipping the alternative-generation step actually loses a viable option.
This single task doesn't have those properties — it's a good debugging task but not a good
discriminator for *process* lift specifically.

**Reliability caveat:** N=1 is noise by the skill's own standard. Re-run at N≥3, and with a task
designed to be less immediately obvious, before drawing a firm conclusion either way.

## §08 Advisory backlog (non-blocking)

- Re-run this same task at N=3 per condition to check whether the 4/4-both-sides result was a fluke of
  this particular pair of subagent runs, or a stable "task too easy to discriminate" result.
- Design a second behavioral task that specifically targets first-thought commitment or menu-hedging —
  e.g., a decision task where the *popular* answer is wrong and the correct answer requires chasing a
  second-order consequence the prompt doesn't headline. That is a sharper test of what fabled claims to
  add.
- Worth comparing against the parallel Opus run (`.agents_workspace/skill-evals/fabled/run-001/`,
  a colleague's session, tasks A/B/C at N=3) once that completes — different tasks, different model,
  same target skill, so a side-by-side reading may show whether lift is task-dependent, model-dependent,
  or both.
- If a full gate evaluation is wanted later, run `ceh-evaluation:evaluate-skill` (not this scoped
  variant) to also cover structure, triggering, and content-rubric dimensions — this run intentionally
  skipped all three per the user's request.
