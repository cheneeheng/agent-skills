---
name: first-run-walkthrough
description: >-
  Load this skill to find out whether a stranger with no context can get from "just arrived" to
  "first real success" on their own — install, sign-up, setup, onboarding, or the first task.
  Dispatches cold persona-constrained subagents that are given only what a newcomer actually has
  (README, landing page, --help) and told to stop at the first thing they cannot proceed past, then
  ranks the stall points by observed outcome and loops fix/re-run until a 5-point gate passes.
  Trigger on "can a new user figure this out", "is the setup clear", "test the onboarding", "try
  this with fresh eyes", "would a beginner get stuck", "nobody can install this", "first-run
  experience", "is this intuitive", or before shipping a README, install guide, or sign-up flow. Not
  for auditing an interface the walker already got into (audit-interface) or WCAG conformance
  (ceh-web-frontend:accessibility).
effort: xhigh
---

# First-Run Walkthrough

The question is not "is this documented". It is **"can someone who knows nothing reach a first
success using only what we actually gave them"** — and the only honest way to answer it is to hand
the artifacts to a reader with no context and watch where they stop.

You cannot run this audit on yourself. You already know the answers, and every gap you would hit
gets silently bridged by what you know. The whole protocol below exists to buy back that ignorance
by putting the walk in cold subagents and constraining what they are allowed to know.

## Honest limits — state these in the report

An LLM playing a novice is a proxy, not a user test. It **reliably** catches undefined jargon,
missing prerequisites, steps that reference things that do not exist yet, dead ends, silent
failures, and unlabeled destructive actions. It **cannot** measure motor precision, reading fluency,
patience, or emotional response. Never write "validated with users" — write "walked cold by N
persona-constrained agents".

## Protocol

### 0. Write the success goal

One sentence, observable, in the user's words. Not "the app is installed" — **"they can see their
own data on a page they navigated to themselves"**.

If you cannot state the goal, stop: the audit has no pass condition and every finding will be
arguable.

### 1. Freeze the artifact set

List **exactly** what a newcomer has, and nothing else. This is the single most important step —
everything after it is only as honest as this list.

| Surface | Typical frozen set |
|---|---|
| Repo / library | `README.md`, the landing section of the docs site, `--help`, the install command, the package page |
| Web app | The public landing page, the sign-up flow, in-product empty states, whatever the email says |
| CLI | `--help`, `<cmd> help`, the man page, the README quickstart |
| Internal tool | The wiki page the newcomer was sent, plus the tool itself |

Record the list verbatim in the report. **Source code is not in the frozen set** unless the target's
audience is people reading the source. Neither is anything you explained in this conversation, an
issue thread, or a commit message.

### 2. Dispatch cold walkers

Spawn one `ceh-usability-audit:novice-walker` agent **per persona** (below), in parallel — they are
independent. Each gets exactly four things:

1. The success goal from step 0.
2. The entry point (a path, a URL, a command).
3. Its persona constraint, verbatim.
4. The frozen artifact set, as an explicit allowlist of paths/URLs.

And one hard rule, which the agent restates back: **stop at the first point you cannot proceed
without information that is not in the frozen set, and report exactly where.** Do not infer the
missing step from how tools like this usually work. Do not fix anything.

Browser caveat: **subagents lose the Chrome tools** (background subagents keep a reduced tool set).
For a live web UI, run the walk yourself in the main session, holding one persona at a time and
narrating the stall points into the same format — or hand the walker screenshots and page text
instead of a URL.

### 3. The personas

Five constraints, each catching a distinct failure class. Run all five unless a surface makes one
meaningless (`Small Screen` on a library API); skipping one is recorded as a skip, not omitted.

| Persona | Holds this constraint the whole way | Catches |
|---|---|---|
| **Blank Slate** | No domain vocabulary and no prior product knowledge. Reads only what is on the screen or page. Assumes nothing is safe to click until told. *(the 5-year-old proxy)* | Undefined jargon, invisible affordances, "obvious" next steps that are not, assumed prerequisites |
| **Cautious Returner** | Will not take any action whose outcome is not stated in advance. Needs to see what happened after every action. Afraid of losing work. *(the 95-year-old proxy)* | Missing confirmation, silent success, irreversible actions, no undo, no way to check state |
| **Interrupted** | Leaves for ten minutes mid-task and may close the tab or terminal. Comes back and must resume. | Lost state, expired sessions/tokens, multi-step flows with no progress marker or resume path |
| **Wrong Turn** | Does the wrong thing first — wrong button, wrong value, skips a required step — then tries to recover. | Dead ends, unrecoverable errors, blame copy, no back, validation that fires too late |
| **Small Screen** | 360px viewport, slow link, or an 80-column terminal. Keyboard only. | Offscreen primary action, layout collapse, hover-only affordances, no loading feedback, truncated output |

`Small Screen` covers the *environment*, not conformance. WCAG mechanics — contrast ratios, ARIA,
focus traps — belong to `ceh-web-frontend:accessibility`; delegate rather than re-deriving them
here, and say in the report that you did.

### 4. Score by observed outcome, not by appearance

**This is the anti-inflation rule and it is not optional.** Severity comes from what actually
happened to a walker, never from how bad something looks to you.

| Severity | Assigned when |
|---|---|
| **Blocker** | A persona could not complete the goal — or completed it wrongly believing it was right |
| **Detour** | Completed it, but only after backtracking, guessing between options, or looking outside what they were given |
| **Friction** | Completed it, but with avoidable doubt — "did that work?" |
| **Polish** | No effect on any walker's completion |

Anything you noticed but no walker stalled on is **not a finding**. It goes in a separate
`Hypotheses` list, unranked, and never counts against the gate. Two measurements make the ranking
reproducible:

- **Actions to success** — how many discrete steps the walker took. Compare across personas; the
  spread is where the design is ambiguous.
- **External lookups** — times a walker needed something outside the frozen set. Any count above
  zero is a Detour by definition, and the missing information names its own fix.

Wall-clock time is meaningless for an LLM walker. Do not record it.

### 5. Report

Write `.agents_workspace/ux-audits/<target>/run-<NNN>/UX_AUDIT.md`, where `<NNN>` is a zero-padded
sequential run index so a re-run never overwrites a prior run's evidence. Create missing parents.
Keep raw walker transcripts in that run folder — a finding without its transcript is an opinion.

```markdown
# First-Run Walkthrough — <target>

**Goal:** <the one sentence from step 0>
**Frozen set:** <verbatim list>
**Walkers:** <personas run> (<personas skipped, and why>)
**Method:** cold persona-constrained subagents — proxy for a user test, not a user test
**Gate:** <N>/5

## Results

| Persona | Reached goal | Actions | External lookups | First stall |
|---|---|---|---|---|

## Findings

### <ID> — <Blocker|Detour|Friction|Polish> — <one-line title>
- **Where:** <file:line, screen, or command>
- **Persona:** <who stalled>
- **Expected / got:** <what they thought would happen / what happened>
- **Missing knowledge:** <the fact they needed and did not have>
- **Fix:** <the concrete change>

## Hypotheses (no walker stalled — unranked)

## Not covered
<what this method cannot measure; what was delegated to accessibility>
```

### 6. Loop

Fix the **top Blocker only**, then re-run **only the personas that stalled on it**. A full re-run
after every edit is waste, and re-running a persona that already passed tells you nothing.

Repeat until the gate reads 5/5 and the user confirms. Report the gate honestly at every iteration
— a 3/5 that is stated is worth more than a 5/5 that was argued into place.

## The gate

| # | Criterion |
|---|---|
| 1 | Every persona that was run reached the goal |
| 2 | Zero open Blockers |
| 3 | No step required knowledge outside the frozen set — every walker's external-lookup count is 0 |
| 4 | Every destructive or irreversible step states its consequence *before* the action and names an undo |
| 5 | The spread in actions-to-success across personas is explained — either it is small, or the reason one persona took longer is a recorded finding |

A criterion that cannot be measured on this target is marked **N/A with a reason** and the gate is
reported out of the remaining count (`4/4, 1 N/A`). Never quietly score an unmeasured criterion as
passing.

## Stop conditions

- **The frozen set cannot be established** — nobody can say what a newcomer actually receives. Ask;
  guessing invalidates every finding downstream.
- **The target needs credentials, payment, or a live account** to reach the goal. Report the walk up
  to that boundary and say plainly that the rest is unwalked. Never invent test credentials.
- **A walker's fix requires a product decision** (removing a feature, changing what the thing is
  for). Report it; do not decide it.

## Where this hands off

| Next question | Skill |
|---|---|
| They got in — is the interface itself usable? | `audit-interface` |
| The stall was an error message | `audit-error-messages` |
| The stall was wording | `plain-language-pass` |
| The stall was a missing/incorrect doc | `ceh-documentation:user-operator-guide`, `ceh-documentation:update-readme` |
| The stall was keyboard, contrast, or screen-reader | `ceh-web-frontend:accessibility` |
| The README's first screen does not say what this is | `ceh-seo:text-discoverability` |
