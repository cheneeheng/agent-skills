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
  Follow-up to run-001 (same folder family), rerun per explicit user feedback that run-001's
  task was "too easy" (4/4 assertions passed on both sides there too). This run deliberately
  designs a harder, multi-part task with a subtle bug (TOCTOU under a pessimistic lock) plus a
  buried second-order consequence (a lock-ordering deadlock against an unrelated nightly job).
  Triggering explicitly out of scope again per user request.
---

## §01 Verdict

On this N=1 probe, **fabled again produced no assertion-level correctness lift** over the Sonnet
baseline: both the with-skill and no-skill subagent independently identified the same core defect
(the proposed fix locks the desk row *after* the availability check and never re-validates under
the lock — a TOCTOU bug that leaves the actual race open), the same buried second-order risk (the
fix's new desk→room lock order collides with the nightly reassignment job's room→desk order,
creating a deadlock hazard the on-call engineer wasn't shown), and the same top-line verdict
("ship with changes," not "ship" or "don't ship"). **This is 4/4 both sides on the pre-registered
assertions — the identical shape of result as run-001**, despite deliberately raising task
difficulty. See §04 for why, and for a genuine (if not pre-registered) content difference the
with-skill transcript produced that baseline didn't: a database-isolation-level caveat that is
technically correct and materially affects whether the recommended fix actually works. Status stays
`draft` — this is a scoped sanity check, not a gate-passing evaluation.

## §02 Derived criteria (scoped to what was measured)

- **Claim:** applying fabled's process (effort triage → understand → generate alternatives → work
  at depth → adversarial self-review → verify → deliver with calibrated conviction) closes most of
  the quality gap between a rushed answer and an excellent one, on non-trivial analysis/decision/
  debugging tasks — specifically by chasing second-order consequences (stage 3) and verifying
  claims that are checkable (stage 5) rather than accepting the first plausible fix.
- **Intended outcome vs. baseline:** an agent following fabled should be less likely to accept the
  on-call engineer's "standard, well-understood pattern" framing at face value, more likely to trace
  the proposed fix against the given code rather than pattern-match on "pessimistic locking fixes
  races," and more likely to surface a risk (the lock-ordering collision) that isn't headlined
  anywhere in the prompt.
- **Scope of this run:** behavioral lift only (dimension 4), N=1, per user's explicit request. This
  run's brief was specifically "use a more complex example, run 001 was too easy" — see §04 for
  the design rationale and whether it succeeded at discriminating.

## §03 Trigger battery

Not measured — out of scope for this run (user: "no need to worry about trigger").

## §04 Behavioral task & assertions (N=1)

**Task design intent:** run-001's advisory backlog flagged that its task was too easy to
discriminate because the disconfirming evidence was a headlined "smoking gun." This run's task
(`task-prompt.md`, same folder) was designed to fix that: a desk-booking double-booking incident
where the on-call engineer proposes a *plausible, standard-sounding* fix (`SELECT ... FOR UPDATE`
pessimistic locking) that is subtly incomplete (a TOCTOU bug — the lock is acquired after the
availability check, not before/inside it), plus a second, unrelated risk (a lock-ordering deadlock
against a nightly batch job) that is only derivable by cross-referencing two separate code snippets
given several paragraphs apart, neither flagged as risky in-text ("stable for six months," "low
risk, rarely touches active desks").

Both subagents were `general-purpose`, spawned in the same turn. With-skill was instructed to
invoke `Skill(skill="fabled")` first and follow its process; baseline was explicitly instructed not
to invoke any skill. Full task text and both transcripts: `task-prompt.md`,
`generated/sonnet/with-skill-answer.md`, `generated/sonnet/baseline-answer.md` (all in this run
folder).

| # | Assertion | With-skill | Baseline |
|---|-----------|:---:|:---:|
| 1 | Explicitly identifies the TOCTOU flaw — the lock is acquired after the free/busy decision, not re-validated before insert — naming it as the reason the fix doesn't close the race | PASS — *"This is a textbook TOCTOU (time-of-check-to-time-of-use) bug... The lock changed timing, not outcome."* | PASS — *"The row lock only serialized access to the desks row's metadata; it never guarded the bookings table, which is where the actual conflict lives."* |
| 2 | Reproduces the exact observed symptom via a concrete concurrent-request trace (both requests picking the same desk, second one inserting anyway after the lock is released) | PASS — 5-step numbered trace, A and B both picking desk 41, B inserting post-lock with no recheck | PASS — equivalent prose trace, A and B both picking desk 41, "B never re-runs `has_conflicting_booking` after acquiring the lock" |
| 3 | Identifies the lock-order-inversion deadlock risk against the nightly `reassign_understaffed_rooms` job as a concrete risk of shipping the fix as described | PASS — explicit "New lock-ordering hazard... needs an explicit decision, not silence," traces all three code paths' lock orders | PASS — explicit "textbook lock-order inversion," names both colliding paths by function/purpose |
| 4 | Delivers one direct, committed recommendation (not a hedged menu) naming specific corrective changes rather than only the risks | PASS — "Ship with changes — not as-is," 4 enumerated required/should-have changes | PASS — "Ship with changes (not as-is)," 3 enumerated changes |

**Result: 4/4 both sides, zero delta — same shape of result as run-001**, on a task deliberately
built to be harder. This is itself a finding: the task-design lesson from run-001 (make the
signal less headlined) was only partially applied here. The two code snippets given in "additional
context" spell out the exact lock orders and the unlocked-scan-then-lock sequence explicitly enough
that a capable model doesn't need to *infer* the bug from indirect evidence — it only needs to
*trace* code that's already handed to it in full. Sonnet's baseline is evidently strong enough at
code tracing (fabled's stage-3/stage-5 behaviors) that it does this unprompted. A sharper
discriminator would omit one of the two code snippets and require the model to *ask for it or infer
its likely shape* — or bury the second risk in a much longer prompt so it's easy to miss under time
pressure, rather than presenting it as a clearly delimited second section.

**Observed qualitative difference (not assertion-graded, but worth recording — and arguably more
significant than run-001's):** the with-skill transcript contains one substantive, technically
correct catch that the baseline entirely omits:

- **Database isolation-level dependency of the fix's correctness (with-skill point 3):**
  *"Confirm DB engine and isolation level before shipping — do not assume... MySQL InnoDB,
  REPEATABLE READ (its default): a plain SELECT after acquiring the lock can still return a
  transaction-start snapshot that predates the commit it needs to see. If this is MySQL, the
  re-check query itself must be a locking read... or the fix silently reintroduces the exact bug
  it's meant to close, just harder to reproduce."* This is correct, non-obvious InnoDB behavior
  (a real, documented MVCC/locking-read interaction) and it is directly relevant: it identifies a
  way the *recommended fix itself* could silently fail to close the race, on a common production
  database, for a reason nothing in the prompt states or hints at. The baseline's equivalent
  recommendation ("re-run `has_conflicting_booking`... after acquiring `FOR UPDATE`... inside the
  same transaction") is the *same fix* but stated as unconditionally correct, with no engine/
  isolation caveat. This maps directly to fabled stage 5 ("verify what's verifiable... internal
  consistency: do the numbers, names, and claims agree with each other") and stage 3 ("chase
  second-order consequences") — it is exactly the kind of catch the skill's process claims to
  produce, and it is not present in the baseline's otherwise very strong answer.
- **A second, related catch (with-skill point 2):** *"Retry at the request level, not by looping
  candidates in one open transaction... a single request that walks candidates 41→42→43 in one
  transaction accumulates locks on all of them, which is worse for the deadlock risk."* Baseline's
  equivalent line ("fall through to the next candidate... rather than inserting") is ambiguous on
  this exact point and doesn't flag the lock-accumulation risk explicitly.
- **Calibrated conviction (stage 6), consistent with run-001's finding:** with-skill closes with an
  explicit confidence split and a stated falsification condition — *"The most likely way I'm wrong:
  if the actual implementation... already re-validates availability after acquiring the lock as an
  unstated implementation detail, then finding 1 is moot."* Baseline states its recommendation with
  equal firmness but without this explicit self-falsification framing.

**Why this matters more than a legibility difference:** in run-001, the qualitative differences
(steelmanning, confidence-splitting) didn't change what shipped or what was checkable. Here, the
isolation-level catch is a *checkable, substantive correctness point* — if the team is on MySQL and
ships baseline's version of the fix verbatim, it could reintroduce the exact bug being fixed, silently.
That's outside this run's pre-registered assertions (none of the four tested for it, because the
task prompt never named a database engine), so it isn't scored as an assertion pass/fail — but it's
real, cited, evidence-backed content lift, not a stylistic artifact.

**Reliability caveat (unchanged from run-001):** N=1 is noise by the skill's own standard. A single
pair of transcripts, however carefully read, cannot establish whether the isolation-level catch is
a stable behavior fabled's process elicits or a one-off flourish from this particular run. Re-run
at N≥3 before treating it as a proven, repeatable lift.

## §08 Advisory backlog (non-blocking)

- **Task design for the next iteration:** don't hand both colliding code snippets side-by-side in
  clearly labeled sections. Bury the second risk (or omit the database engine entirely, as this run
  did) and see whether the with-skill process's "verify what's verifiable" stage reliably surfaces
  the missing fact (e.g., "you didn't tell me the DB engine — this matters, confirm before shipping")
  while baseline ships without asking. This run showed once that fabled *can* produce that catch
  unprompted; it did not test whether that's a *stable* difference vs. baseline noticing it too on
  a re-run.
- **Re-run this exact task at N=3 per condition** to check whether the isolation-level catch appears
  reliably in with-skill runs and reliably absent in baseline runs, or whether run-002's single pair
  was itself noise in the other direction from run-001.
- Cross-reference against the parallel Opus evaluation under
  `.agents_workspace/skill-evals/fabled-opus/run-001/` (different model, different task) once
  available — two independent "4/4 both sides on pre-registered assertions" results across two
  different tasks and models would meaningfully raise confidence that Sonnet/Opus-class baselines
  are simply strong enough at this style of explicit-evidence bug-hunting that fabled's *assertion-
  level* lift is hard to demonstrate without deliberately withholding information the model would
  otherwise have to actively chase — which is precisely the design gap named above.
- If a full gate evaluation is wanted later, run `ceh-evaluation:evaluate-skill` (not this scoped
  variant) to also cover structure, triggering, and content-rubric dimensions — both scoped runs to
  date have skipped all three per explicit user request.
