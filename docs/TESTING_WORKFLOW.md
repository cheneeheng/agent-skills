# Testing Workflow

How the four testing-related plugins fit together in a session: what loads, when it loads, and what
the sequence looks like for the moments that actually come up.

Per-skill detail lives in `plugins/ceh-testing/README.md` and each plugin's own README. This guide covers
only what no single plugin can document — the routing *between* them.

## The split

| Plugin | Tier | Owns | Surface |
|--------|------|------|---------|
| `ceh-testing` | cross-cutting | **Technique** — which inputs, which scenarios, is the suite trustworthy | 5 skills + `test-suite-auditor` agent |
| `ceh-python-service` | stack | **Tooling** — pytest, test DB, httpx, fixtures | `python-service-testing` + 3 tester agents + runner scripts |
| `ceh-python-library` | stack | **Tooling** — pytest, public-API surface | `python-library-testing` (skill only) |
| `ceh-web-frontend` | stack | **Tooling** — Vitest, Testing Library, MSW, Playwright | `frontend-testing` + 3 tester agents + runner scripts |

`ceh-testing` is loaded **alongside** a stack plugin, never instead of one. The test for what belongs
where: would the content be byte-identical across stacks? Boundary analysis is; `asyncio_mode` is not.

## How each layer loads

Three different mechanisms, and the difference decides whether you have to say anything:

| Layer | Mechanism | Consequence |
|-------|-----------|-------------|
| Stack testing skills | `paths:` globs (`**/test_*.py`, `**/*.test.tsx`, `**/conftest.py`) **plus** description | Loads passively when you touch a test file — no phrasing needed |
| `ceh-testing` skills | Description only — **no `paths:`** | Fires on *what you say*, not what you open. Every trigger is a moment verb |
| Tester agents | Description auto-delegation + `skills:` preload | Preloaded skills are the agent's only standards channel |

`SessionStart` hooks do not fire for subagents, so `skills:` in an agent's frontmatter is the **only**
way a standard reaches one. All six tester agents preload their stack skill plus
`ceh-testing:design-test-cases`; `test-suite-auditor` preloads `ceh-testing:audit-test-suite`.

**Soft dependency:** if `ceh-testing` is not installed, those preloads resolve to nothing *silently* —
no error, no failed dispatch. The agents still run on their stack skill alone and their inline
fallbacks (happy path / boundaries / error paths). What is lost is the rest of the ladder: decision
tables, state transitions, pairwise, properties, metamorphic relations, fuzzing, forced dependency
failure, plus the assertion rules and the stopping criterion.

## Routing — what you say to what runs

| Moment | Loads |
|--------|-------|
| Opening or creating a test file | Stack testing skill (passive) |
| "write tests for this", "what should I test", "cover the edge cases" | `design-test-cases` + stack skill |
| "write unit/integration/system tests" (many at once) | Tester agents + stack skill + `design-test-cases` |
| "fix this bug", a pasted stack trace, "this worked last week" | `test-a-bug-fix` |
| "refactor this", "extract this", "upgrade this dependency" | `verify-behavior-preserved` |
| "shrink the diff", "simplify the branch before the PR" | `verify-behavior-preserved` **and** `shrink-diff` |
| "is this ready", "before I open the PR", "race condition", "is this migration safe" | `close-test-risk-gaps` |
| "are these tests any good", "why didn't the tests catch this", "flaky test" | `audit-test-suite`, or `test-suite-auditor` when the run is slow |

## Scenario A — tests for a new feature

The common case. Phrasing matters more than it looks:

```
create unit/integration/system tests. make sure the tests have 100% code coverage.
```

1. Stack skill loads on the test paths — folder layout, what is real vs mocked, fixture patterns.
2. Unit and integration tester agents auto-delegate; the system tester fires because you named it.
   Each spawns with the stack skill + `design-test-cases`, writes into its folder, runs its script.
3. `audit-test-suite` should pick up after the batch lands ("after a batch of tests was generated").

The second sentence is the problem — see [Coverage](#coverage--what-the-number-is-for). Prefer:

```
create unit/integration/system tests. Walk the design-test-cases ladder and say which
rungs you skipped. Use --cov-branch to find files and branches at zero, then audit the suite.
```

Same three agents, same runners, but the stopping criterion becomes "every partition, boundary,
live decision-table row, invalid transition and dependency-failure path once" instead of a number
that rewards assertion-free tests.

## Scenario B — the same request in a Python library

`python-library-testing` loads and gives you `tests/unit|api`, public-API-only testing, and the
mocking rules. Then it stops: **the library plugin ships no tester agents and no runner scripts.**
Either the work stays inline in the main session, or — if `ceh-python-service` is also installed —
`python-unit-tester` matches "write unit tests" for any Python file and arrives carrying *service*
guidance (test DB, httpx, ASGI transport) for a library with no web dependencies.

If you work on libraries often, say "write these inline" or name the skill explicitly.

## Scenario C — a bug fix

Triggered by ordinary bug phrasing — no special vocabulary needed. `test-a-bug-fix` fires **before**
the fix and enforces the order:

1. Smallest failing test first, in the suite, before any source edit.
2. Run it and read the failure — confirm it fails for the real reason, not an import error.
3. Fix the source.
4. `git stash` the fix and confirm the test goes red again. A test that stays green without the fix
   is not testing the fix.
5. Generalize one step (the boundary next to the bug), then stop.

If the behavior used to be correct, the same reproducer becomes the predicate for `git bisect run`.
The stack skill supplies the fixture and runner underneath; the technique skill owns the protocol.

## Scenario D — a refactor, and shrinking a branch

"shrink the diff" is listed as a trigger by **both** `verify-behavior-preserved` and
`ceh-agent-coding-contract:shrink-diff`. That is deliberate — both skills change working code with
no behavior change intended, and the shrink side carries no verification step of its own. The
`Behavior preservation` block in `shrink-diff` and `refactor-repo` now points back at the pinning
step for anything past a mechanical transform.

| You say | Loads |
|---|---|
| "refactor this", "extract this", "upgrade this dependency", "make sure nothing broke" | `verify-behavior-preserved` only |
| "shrink the diff", "simplify the branch before the PR" | both |
| "consolidate the branch", "can this diff be smaller" | `shrink-diff` primarily |
| "clean up the whole codebase" | `refactor-repo` (+ `verify-behavior-preserved`) |

**Ordering is the thing to watch.** The two want opposite ends of the timeline: pinning must happen
*before* the edit, but "shrink the diff" is said *after* the branch is functionally complete. That
is consistent — the branch's current behavior is the oracle — but if the shrinking happens first,
the pins were written against already-shrunk code and prove nothing. To force the order:

```
/ceh-testing:verify-behavior-preserved     # pin behavior, commit the pins on their own
/ceh-agent-coding-contract:shrink-diff     # then shrink; suite stays green with no test edits
```

Committing the pins separately is what lets a reviewer see they predate the change.

## Scenario E — the pre-PR gate

"is this ready" / "anything else to test" / "before I open the PR" loads `close-test-risk-gaps`.
It is a **triage gate, not a checklist**: five classes that a functional suite structurally cannot
catch — concurrency and non-idempotent retries, contract drift across a process boundary,
performance regression, broken authorization, migration and rolling-deploy incompatibility. Each has
a trigger condition and one minimal test; a class whose trigger does not fire is skipped
**explicitly** and the gate reports the skip.

Sits directly before `ceh-git-workflow:open-pr` in a normal branch flow.

## Scenario F — is this suite worth anything

Inline, `audit-test-suite` runs six checks cheapest-first: assertion audit, delete-the-code check,
mutation testing scoped to the diff, flakiness and order dependence, level and speed, branch
coverage last.

Delegate to `@ceh-testing:test-suite-auditor` when the suite is large, the run is slow, or mutation
output would flood the session. It is read-only — never edits source, tests, or config, never
installs a tool — scopes to `main...HEAD`, caps mutation runs, and hands back ~15 ranked findings.
Writing the missing tests goes back to the stack's tester agents.

The highest-value defect — a test computing its expectation with the same logic as the code under
test — is invisible to every automated check and has to be read for.

## Coverage — what the number is for

Every layer here agrees, and it is worth stating once because it contradicts the reflex:

- Coverage tells you which lines *ran*, never whether an assertion would have noticed them being wrong.
- Always pass `--cov-branch`. Line coverage counts an `if` with no `else` as fully covered when only
  the true side ran — green exactly where the untested half lives.
- Use it to find files and branches **at zero**. Do not chase it as a score: coverage rises fastest
  by executing code without asserting on it.
- Surviving mutants are the metric with teeth.

An explicit "100% coverage" instruction overrides all of that (per the contract's authority
hierarchy — an in-session instruction outranks a skill), and what comes back is the padded,
assertion-thin suite `audit-test-suite` exists to flag. The stack skills' own targets are 80% / 95%
core logic (Python) and 70% for `src/lib/` (frontend).

## Overlaps worth knowing

| Overlap | Resolution |
|---|---|
| `design-test-cases` vs stack testing skill | Technique vs tooling. Which inputs → `design-test-cases`. Which runner, fixture, mock → stack skill. A technique block appearing in a stack skill means the boundary slipped |
| `verify-behavior-preserved` vs `shrink-diff` / `refactor-repo` | Pair, don't compete — pin first, shrink second (Scenario D) |
| `python-system-tester` vs `ts-system-tester` | The Python one says **do not auto-invoke** (slow, expensive); the TS one is proactive. Name system/E2E tests explicitly to be sure |
| `audit-test-suite` skill vs `test-suite-auditor` agent | Same checks. Skill for a quick inline read; agent when the run is slow or noisy |
| `close-test-risk-gaps` vs `design-test-cases` | Ladder picks inputs for a function; the gate triages failure classes for a feature about to ship |

## Install combinations

| Building | Install |
|---|---|
| FastAPI / async service | `ceh-python-service` + `ceh-testing` |
| Python package | `ceh-python-library` + `ceh-testing` |
| SvelteKit or React frontend | `ceh-web-frontend` + `ceh-testing` |
| Fullstack | service + frontend + `ceh-testing` |

```
/plugin install ceh-testing@ceh-plugins --scope user
```

`ceh-testing` alone is usable — the technique skills need no stack plugin — but you lose the runner,
fixtures, mocking rules, and the tester agents.
