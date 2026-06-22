# Triggering battery — run-003 / iteration-1 (lite, N=1, cold, correct protocol)

**Protocol:** each prompt handed to a fresh `general-purpose` subagent as the *only* input — no
mention of skills, no "report which skills you'd load." Fire = the subagent surfaced
`write-less-code`'s distinctive signatures while handling the task (named the skill, quoted the
6-rung ladder verbatim, or applied its house conventions: native-over-library framing,
installed-dep-over-custom, `// less-code:` comment, `skipped: X / add when Y` output, DB-constraint-
over-app-code). This is the corrected method that run-002 violated (run-002 primed agents to
deliberate over the skill list → inflated 6/6).

**Environment confound (material):** subagents ran in the `agent-skills` cwd, which has no
application code. App-coding prompts (P3, P4, P5, P6, and most negatives) hit "no such file / wrong
repo" and spent effort on that instead of naturally solving the task. This *depresses* the positive
rate — an agent that never engages the task can't pull in a feature-implementation skill. Misses
below are therefore partly an artifact of the sandbox, not purely the description.

## Positives

| # | Prompt (gist) | Fired? | Evidence |
|---|---------------|--------|----------|
| P1 | birthday field in SignupForm.tsx, "cleanest way" | **YES** | Recommended native `<input type="date">`, "no library", "zero dependencies", "skip a date-picker library" — verbatim match to skill body example (SKILL.md:28). |
| P2 | dedupe 50k emails from json before DB insert | **YES (moderate)** | Stdlib single-pass O(n) script; "a unique constraint on the email column is the real guarantee" = skill's DB-constraint-over-app-code (SKILL.md:28); defaults flagged in skill's terse style. Overlaps generic good practice. |
| P3 | "leanest version that works" notifications feature | **YES** | Derailed on missing app code, yet explicitly named `ceh-agent-coding-contract:write-less-code` and quoted the full ladder ("question whether the task needs to exist → stdlib → native platform → installed dep → one line → custom code last"). Verbatim ladder = body was read. |
| P4 | redo over-engineered EventBus simpler | **NO** | Fully derailed (no matching PR). No ladder, no skill name, no conventions. Confounded — couldn't engage the task. |
| P5 | "yagni mode: just get csv export working" | **NO (weak)** | Derailed on missing reports page. Invoked "YAGNI" heavily but that echoes the user's own "yagni mode"; no skill-distinctive signature (no ladder, no `skipped/add-when`, didn't name skill). Not a clean fire. |
| P6 | rate limiting on /login | **YES** | Derailed on missing app, yet named "the write-less-code reflex applies — don't hand-roll a limiter", recommended `slowapi` (installed-dep over custom = rung 4). Skill surfaced through the derailment. |

**Positive trigger rate: 3/6 clear (P1, P3, P6); 4/6 if P2's signatures count as the skill.**
Below the ≥5/6 lite threshold. Direction agrees with run-001 (cold 3/10 under-trigger),
**contradicts run-002 (primed 6/6)** — the corrected protocol reproduces under-triggering, not a
pass. Confound caveat: P4/P5 misses are the most environment-contaminated; true rate is uncertain
but not clean.

## Near-miss negatives

| # | Prompt (gist) | Fired? | Evidence |
|---|---------------|--------|----------|
| N1 | review PR, is the simplification safe | **NO** | Treated as review; sought the PR; no minimalism conventions. Correct (→ code-review). |
| N2 | remove the leftpad dependency | **NO** | Searched, nothing to remove; no ladder. Correct (→ dependency-management; dep *removal*). |
| N3 | Safari "invalid date" bug fix | **NO** | Gave the abstract Safari ISO-parsing fix; no minimalism framing. Correct (plain bugfix). |
| N4 | "do it properly, full validation, payments, no shortcuts" | **NO** | Refused to guess a charge path; demanded spec. Did NOT apply lazy minimalism — the correct non-fire for an explicit full-version + security-path request (SKILL.md:52-56 guardrail boundary). |
| N5 | write unit tests for CartService | **NO** | No such class; no minimalism conventions. Correct (test authoring). |
| N6 | refactor whole reporting module for maintainability | **NO** | Advised map-public-surface-first; no `write-less-code` signature, didn't name it. Correct — and notably did NOT over-trigger, contradicting run-002's worry that N6 would fire. |

**Near-miss false-positive rate: 0/6.** Clean. The skill does not over-trigger on adjacent
keyword-sharing requests, including the borderline refactor case.

## Read

- **Over-triggering: not a problem** (0/6, high confidence even given the confound — none of the
  negatives surfaced the skill).
- **Under-triggering: the open issue, corroborated** — corrected cold N=1 lands at 3–4/6 positives,
  consistent with run-001's cold 3/10 and refuting run-002's primed 6/6. N=1 + the cwd confound mean
  this is a sanity read, not a statistic; the authoritative re-check is the full eval's N=3 cold runs
  **in a real application sandbox** (so feature prompts can actually be engaged).
