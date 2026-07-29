---
name: design-test-cases
description: >-
  Load this skill when deciding which inputs and scenarios a test should cover — not how to wire the
  runner. Supplies the input-selection ladder: equivalence partitions, the boundary checklist,
  decision tables for interacting flags, state-transition and invalid-transition cases, pairwise for
  large config spaces, property-based tests for rules that hold over all inputs, and forced failure
  of every dependency. Trigger on "write tests for this", "what should I test", "add test cases",
  "cover the edge cases", "is this tested enough", "property-based", "hypothesis", "fast-check", or
  when a test file has only a happy path. Pairs with the stack testing skills, which own the runner,
  fixtures, and mocking library.
---

# Design Test Cases

The runner, fixtures, and mocking library belong to your stack's testing skill
(`ceh-python-service:python-service-testing`, `ceh-python-library:python-library-testing`,
`ceh-web-frontend:frontend-testing`). This skill answers the question those do not: **which inputs,
and which scenarios.**

The default failure mode is one happy path plus a null check. That suite passes on code that is
wrong in every way a real caller will discover.

## The ladder

Walk it in order. Stop when the remaining rungs have no trigger — most functions need 1, 2, and 6.

### 1. Partition the input space

Group inputs into classes where every member is expected to take the same path. **One test per
class, not per value.** Three tests for `5`, `7`, and `12` are one test wearing three hats.

For `discount(order_total, customer_tier)`: the classes are the tier values × {below threshold, at
threshold, above threshold} — not a list of amounts.

Write the classes down before the tests. If you cannot name a class's expected behavior in a
sentence, you do not yet understand the requirement.

### 2. Boundaries — where the bugs actually are

Every partition has edges, and the edge is where off-by-one lives. Test **the boundary and one step
either side**, never the middle of a range.

Run this checklist against every parameter:

| Kind | Cases |
|------|-------|
| Numeric | `0`, `1`, `-1`, min, min−1, max, max+1, the exact threshold and threshold±1 |
| Collection | empty, exactly one, exactly two, at the size limit, over the limit, duplicates, unsorted |
| String | `""`, whitespace-only, single char, at max length, over max length, unicode + emoji, embedded newline, leading/trailing space |
| Optional | absent, present-but-null, present-but-empty — these are three different inputs |
| Time | epoch, DST transition, month/year end, leap day, expiry exactly now, timezone-naive vs aware |
| Pagination | page 0, page 1, last page, page past the end, limit 0, limit above max |

"At the limit" and "one over the limit" are the two highest-yield cases in the table. Include them
whenever a limit exists.

### 3. Decision tables — when flags interact

Two or more booleans/enums that combine to pick an outcome. Enumerate the grid, strike the
impossible rows, test what remains:

| `is_member` | `has_coupon` | `cart ≥ $50` | Expected |
|---|---|---|---|
| F | F | F | no discount |
| F | F | T | free shipping |
| F | T | F | coupon only |
| T | F | T | member rate + free shipping |
| … | | | |

This is how you find the combination nobody implemented. If the grid exceeds ~8 live rows, go to
rung 5.

### 4. State transitions — including the illegal ones

Anything with a lifecycle (order, session, job, connection, feature flag). Test the legal path
once, then spend your effort on:

- **Invalid transitions** — cancel an already-shipped order, pay a refunded invoice, close a closed
  connection. These are where real systems corrupt data.
- **Repeat transitions** — fire the same valid transition twice. Idempotent, or a duplicate charge?
- **Terminal states** — every operation attempted after the terminal state.

### 5. Pairwise — when the config space explodes

Six independent booleans is 64 combinations; nobody writes 64 tests, so most people write two.
Covering all *pairs* catches the large majority of interaction bugs in a fraction of the cases.
Generate the set (`allpairspy` in Python, `@fast-check/…` or a table in TS) rather than picking by
hand — hand-picked sets cluster around the defaults, which is exactly where bugs are not.

### 6. Properties — rules that hold for every input

When you can state a rule that must always be true, assert the **rule** instead of guessing inputs.
The generator picks inputs your imagination would not, and shrinks a failure to a minimal case.

```python
from hypothesis import given, strategies as st

@given(st.text())
def test_encode_decode_round_trips(s):
    assert decode(encode(s)) == s              # round-trip

@given(st.lists(st.integers()))
def test_sort_preserves_multiset(xs):
    assert sorted(sort(xs)) == sorted(xs)      # invariant
```

```ts
import fc from 'fast-check';

it('normalizes idempotently', () => {
  fc.assert(fc.property(fc.string(), s => normalize(normalize(s)) === normalize(s)));
});
```

The four shapes worth reaching for:

| Shape | Assertion |
|-------|-----------|
| Round-trip | `decode(encode(x)) == x`, parse∘format, serialize∘deserialize |
| Invariant | output always sorted / length preserved / total unchanged / never negative |
| Idempotence | `f(f(x)) == f(x)` — normalizers, migrations, retries, upserts |
| Oracle | matches a slow-but-obviously-correct reference, or the old implementation |

Reach for this whenever a function is pure and total: parsers, formatters, serializers, sorting,
money and date arithmetic, sanitizers, diffing, pagination math.

Record any failing case the generator finds as its own explicit test — generators are not
guaranteed to produce it again.

### 7. Force every dependency to fail

Mocks that only ever return success leave every `except` / `catch` branch unexecuted. This is the
most under-tested region of agent-written code.

For each external dependency, make it fail once:

- raises the library's real exception type (not bare `Exception`)
- times out
- returns a malformed / empty / partial payload
- returns success but with a field missing
- fails **after** a partial write — assert the state left behind is consistent

```python
def test_charge_failure_leaves_order_unpaid(mocker, order):
    mocker.patch("app.billing.stripe.charge", side_effect=stripe.error.APIConnectionError("boom"))
    with pytest.raises(PaymentUnavailable):
        pay(order)
    assert order.status == "pending"        # assert the state, not just the raise
```

## Assertion rules

- **Assert the value, not its existence.** `assert result is not None` and
  `expect(x).toBeDefined()` pass on almost every bug. Assert the actual expected value.
- **Use a literal expected value.** If the test computes the expectation with the same logic as the
  code, it will agree with the code no matter how wrong both are. Write `timedelta(minutes=90)`,
  not `parse_duration_reference("1h30m")`.
- **One behavior per test.** The failure message should name the bug without a debugger.
- **Assert the state change too**, not only the return value — what got written, what got emitted.

## How many tests is enough

Not a coverage percentage. Coverage tells you which lines ran, never whether an assertion would
have noticed them being wrong.

The suite is sufficient when: **every partition once, every boundary once, every live decision-table
row once, every invalid transition once, every dependency-failure path once.** Anything past that is
duplication; anything short of it is a gap you can name.

To find out whether those tests would actually catch a defect, use `audit-test-suite`.
