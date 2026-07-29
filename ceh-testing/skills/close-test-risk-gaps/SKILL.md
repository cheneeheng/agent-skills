---
name: close-test-risk-gaps
description: >-
  Load this skill as a pre-completion gate when a feature is functionally working and about to be
  called done — it triages the four failure classes a passing functional suite structurally cannot
  catch: concurrency and non-idempotent retries, contract drift across a process boundary,
  performance regression, and broken authorization. Each has a trigger test and one minimal test to
  add; classes whose trigger does not fire are skipped explicitly. Trigger on "is this ready",
  "anything else to test", "before I open the PR", "did I miss anything", "race condition",
  "idempotency", "webhook retries", "N+1 query", "authorization test", or "the tests pass but I am
  not confident".
---

# Close Test Risk Gaps

Unit, integration, and E2E tests all ask the same question: given this input, is the output right?
Four important failure classes are invisible to that question — they depend on *timing*, on *who is
asking*, on *what a different process expects*, or on *how long it took*.

This is a triage gate, not a checklist to complete. Run it when a feature is working and about to be
called done. **For each class: does the trigger fire? If no, skip it and say so.** Adding tests
whose trigger did not fire is ritual, and it is how a suite becomes slow and ignored.

---

## 1. Concurrency and idempotency

**Trigger fires if any of:** two requests can touch the same row; a read-modify-write happens outside
a transaction; there is a retry, webhook, queue consumer, or cron; a counter, balance, or sequence is
incremented; a "check then insert" exists; a background job shares state with a request path.

**The two tests:**

```python
# a) same operation twice — the retry that every queue and webhook will eventually send
async def test_charge_is_idempotent(client, order):
    key = {"Idempotency-Key": "k-1"}
    first  = await client.post(f"/orders/{order.id}/charge", headers=key)
    second = await client.post(f"/orders/{order.id}/charge", headers=key)
    assert second.status_code == first.status_code
    assert await count_charges(order.id) == 1          # the invariant, not the response

# b) N at once — assert the invariant, not the individual results
async def test_concurrent_redeem_never_oversells(client, coupon):   # stock = 1
    results = await asyncio.gather(*(client.post(f"/coupons/{coupon.id}/redeem")
                                     for _ in range(20)), return_exceptions=True)
    assert sum(r.status_code == 200 for r in results if not isinstance(r, Exception)) == 1
    assert await stock_of(coupon.id) == 0              # never negative
```

Assert the **invariant** (a count, a balance, a uniqueness constraint), never the individual
responses — which one wins is legitimately nondeterministic, but "exactly one" is not.

If it passes on the first run, run it 20 times before believing it. A race that reproduces one time
in ten is still a race.

---

## 2. Contract drift

**Trigger fires if:** you changed a shape that crosses a process boundary — an HTTP response body, an
event or message payload, a stored JSON column, a public function signature in a library, or a
database column another service reads.

**The test:** assert the response against the published schema, not against a hand-written dict — a
hand-written expectation drifts along with the code and never fails.

```python
def test_order_response_matches_published_schema(client, order):
    body = client.get(f"/orders/{order.id}").json()
    OrderResponseV1.model_validate(body)               # the schema consumers were given
    assert set(OrderResponseV1.model_fields) <= set(body)   # no field silently dropped
```

Removing or renaming a field, tightening a type, or making an optional field required is a
**breaking change** for anyone already consuming it. Adding an optional field is not. If the change
is breaking and consumers exist, the test is not the fix — versioning is; flag it rather than
quietly updating the schema.

For messages and events, pin one real payload per event type as a fixture and validate it. A
consumer that deserializes strictly will break on a producer's "harmless" rename.

---

## 3. Performance regression

**Trigger fires if:** the change is on a request-serving hot path; a loop iterates something
unbounded or caller-supplied; a query runs inside a loop (the N+1 shape); a new `await`, network
call, or file read landed in a request path; an index was dropped or a `WHERE` clause changed.

**The test: assert a countable bound, never a wall-clock duration.** Timing assertions are flaky on
shared CI and get deleted within a month.

```python
def test_order_list_does_not_n_plus_one(client, query_counter, orders_factory):
    orders_factory(50)
    with query_counter as q:
        client.get("/orders")
    assert q.count <= 3          # constant in the number of orders — this is the real bug
```

Count queries, HTTP calls, or allocations — those are deterministic and they are what actually
regressed. If you must assert on time, use a benchmark harness with a baseline
(`pytest-benchmark`, `vitest bench`) and a ceiling wide enough that only a real regression trips it,
never a bare `assert elapsed < 0.5`.

The highest-value single assertion here is the N+1 count check. Add it once per list endpoint.

---

## 4. Authorization

**Trigger fires if:** an endpoint accepts a user-supplied identifier; a response contains data owned
by someone; there are roles, tenants, teams, or permissions; anything is admin-only.

**The test: the authz matrix.** Functional tests are written from the happy path — the owner
requesting their own resource — so the case that ships broken is always *another user's resource*.

```python
@pytest.mark.parametrize("actor,target,expected", [
    ("owner",     "own",       200),
    ("owner",     "other_user", 404),   # the one that is always missing
    ("teammate",  "own",       200),
    ("anonymous", "own",       401),
    ("member",    "admin_only", 403),
])
def test_order_access_matrix(client, actor, target, expected):
    assert client.get(url_for(target), headers=auth(actor)).status_code == expected
```

Three rules the matrix encodes:

- **Not-yours returns 404, not 403** — a 403 confirms the resource exists, which leaks the ID space.
- **Test the object, not just the route.** Route-level auth passes while the handler happily loads
  any ID it is given. That is the whole IDOR class.
- **Cover write and delete, not only read.** They are usually pasted from the read handler, minus
  the ownership check.

Add one matrix per resource type, not per endpoint.

---

## Reporting the gate

State the verdict for all four classes, including the skips — a silent skip is indistinguishable
from an oversight:

```
Concurrency  — FIRES: /coupons/{id}/redeem decrements shared stock. Added 2 tests.
Contract     — FIRES: OrderResponse dropped `legacy_total`. Breaking; needs v2, flagged not fixed.
Performance  — FIRES: GET /orders loads customer per row. Added query-count test (was 51, now 3).
Authorization— skipped: no user-supplied IDs, endpoint is unauthenticated and public.
```

If nothing fires, say that explicitly. "All four skipped, none apply" is a legitimate and useful
result — it means the risk was considered, not ignored.
