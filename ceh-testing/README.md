# ceh-testing

Stack-agnostic testing **technique** — which tests to write, and whether the ones you have are worth
anything.

Your stack's testing skill owns the runner, fixtures, and mocking library
(`ceh-python-service:python-service-testing`, `ceh-python-library:python-library-testing`,
`ceh-web-frontend:frontend-testing`). This plugin owns the questions those do not answer: which
inputs, which scenarios, does a green suite actually catch a defect, and what does a passing
functional suite structurally miss. Load it alongside a stack plugin, not instead of one.

## Skills

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Test a Bug Fix | `/ceh-testing:test-a-bug-fix` | A bug, crash, regression, or incident is being fixed — write the failing test before the fix |
| Design Test Cases | `/ceh-testing:design-test-cases` | Deciding which inputs and scenarios to cover: partitions, boundaries, decision tables, state transitions, pairwise, properties |
| Audit Test Suite | `/ceh-testing:audit-test-suite` | Finding out whether a passing suite would catch a defect: assertion quality, mutation testing, flakiness |
| Verify Behavior Preserved | `/ceh-testing:verify-behavior-preserved` | Before a change meant to alter no observable behavior: refactor, extraction, dependency or runtime upgrade, port |
| Close Test Risk Gaps | `/ceh-testing:close-test-risk-gaps` | Pre-completion gate: triage concurrency, contract drift, performance, and authorization gaps |

### `test-a-bug-fix`

**Auto-triggers on:** "fix this bug", "this is broken", "getting an error", "regression", "hotfix",
a pasted stack trace, or reviewing a bug-fix PR that ships no test.

Reproduce-first protocol: smallest failing test before any source edit, read the failure to confirm
it fails for the real reason, fix, then prove coupling by reverting the fix (`git stash`) and
watching the test go red again. A test that stays green without the fix is not testing the fix.

### `design-test-cases`

**Auto-triggers on:** "write tests for this", "what should I test", "cover the edge cases", "is this
tested enough", "property-based", "hypothesis", "fast-check", or a test file with only a happy path.

A seven-rung input-selection ladder — equivalence partitions, the boundary checklist, decision
tables for interacting flags, state transitions including the illegal ones, pairwise for large
config spaces, properties that hold over all inputs, and forced failure of every dependency. Walk it
in order and stop when the remaining rungs have no trigger; most functions need rungs 1, 2, and 6.

### `audit-test-suite`

**Auto-triggers on:** "are these tests any good", "audit the tests", "mutation testing", "mutmut",
"stryker", "why did the tests not catch this", "flaky test", "tests pass but the bug shipped", or
right after a batch of tests was generated.

Six checks, cheapest first: assertion audit (AST scan for tests that assert nothing), the
delete-the-code check, mutation testing scoped to the diff, flakiness and order dependence, level
and speed, then coverage — used only to name regions at zero, never as a headline number. The
highest-value defect (a test computing its expectation with the code's own logic) is invisible to
every automated check and has to be read for.

### `verify-behavior-preserved`

**Auto-triggers on:** "refactor this", "clean this up", "extract this", "simplify without changing
behavior", "upgrade this dependency", "rewrite this module", "shrink the diff", "make sure nothing
broke".

A refactor is the one change where the correct answer is known in advance — it is whatever the code
does today. Establishes that oracle before the edit: coverage check on the region, characterization
tests that pin current behavior (including the odd rounding), golden files for large output, and a
differential run of old versus new over the same inputs via `git worktree`.

### `close-test-risk-gaps`

**Auto-triggers on:** "is this ready", "anything else to test", "before I open the PR", "did I miss
anything", "race condition", "idempotency", "webhook retries", "N+1 query", "authorization test",
"the tests pass but I am not confident".

A triage gate, not a checklist. Four failure classes are invisible to "given this input, is the
output right" — concurrency and non-idempotent retries, contract drift across a process boundary,
performance regression, and broken authorization. Each has a trigger condition and one minimal test
to add; a class whose trigger does not fire is skipped **explicitly**, and the gate reports the
skips.

## Agents

### `test-suite-auditor`

Runs the slow, high-output half of `audit-test-suite` in an isolated subagent and hands back a
ranked report. Read-only — it never edits source, tests, or config, and never installs a tool.

**Invoke:** `@"ceh-testing:test-suite-auditor (agent)"`

**Auto-triggers on:** "audit the test suite", "run mutation testing", "are these tests any good",
"find the flaky tests", "why did the tests not catch this bug", or after a batch of tests was
generated.

**Use the agent when** the suite is large, the run is slow, or the output would flood the session.
For a quick inline assertion review, the skill handles it in the main conversation. Writing the
missing tests is delegated to the stack's own tester agents.

## Relation to the stack testing skills

| Question | Owner |
|----------|-------|
| Which runner, fixtures, mocks, CI wiring | `ceh-python-service` / `ceh-python-library` / `ceh-web-frontend` testing skills |
| Which inputs and scenarios | `design-test-cases` |
| Is this suite trustworthy | `audit-test-suite` + `test-suite-auditor` |
| Did this bug get a test | `test-a-bug-fix` |
| Did this refactor change behavior | `verify-behavior-preserved` |
| What does a passing suite still miss | `close-test-risk-gaps` |

## Installation

```
/plugin install ceh-testing@ceh-plugins --scope user
```

Or manually in `~/.claude/settings.json`:

```json
{ "plugins": [{ "path": "~/agent-skills/ceh-testing" }] }
```
