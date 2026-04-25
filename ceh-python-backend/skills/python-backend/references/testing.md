# Testing

Framework: **pytest** with **pytest-asyncio** (`asyncio_mode = "auto"` in `pyproject.toml`)

HTTP testing: **`httpx.AsyncClient`** (async, preferred) or **FastAPI `TestClient`** (sync)

## Test Structure

```
backend/
├── app/
│   └── services/
│       └── reasoning/
│           └── engine.py
└── tests/
    ├── unit/         # Isolated — no I/O, mock all external dependencies
    ├── integration/  # Real database, mock only external APIs (LLM, payment)
    ├── system/       # Full-stack E2E scenarios — real infra, real HTTP
    └── conftest.py   # Shared fixtures: test DB, async client, mock factories
```

Test files mirror source structure. Naming: `test_<what>_<expected_behavior>.py`. One logical behavior per test.

## Unit Tests — Fast, No I/O

```python
class TestReasoningEngine:
    async def test_validate_rejects_unknown_event_type(self):
        engine = ReasoningEngine()
        event = ReasoningEvent(event_type="invented_type", ...)
        result = await engine.validate(event, state)
        assert result.is_invalid
        assert "invalid event type" in result.reason
```

## Integration Tests — Real Database, Never Mocked

```python
class TestSessionsAPI:
    async def test_post_message_creates_event(
        self, async_client: AsyncClient, test_db
    ):
        response = await async_client.post(
            f"/sessions/{session_id}/message",
            json={"content": "I think we should rewrite in Rust"}
        )
        assert response.status_code == 200
        assert len(response.json()["reasoning_events"]) > 0

        # Verify it actually landed in the database
        row = await test_db.fetchrow(
            "SELECT * FROM event_log WHERE session_id = $1", session_id
        )
        assert row is not None
```

Do **not** mock PostgreSQL in integration tests. PostgreSQL-specific behavior (JSONB, constraints, transactions) must be verified against a real instance. Each test that writes data should run in a transaction that rolls back after the test.

## Mocking

- Mock the LLM API client in all tests (no real API calls in tests)
- Mock external HTTP services
- Do **not** mock PostgreSQL in integration tests
- Use `unittest.mock` or `pytest-mock`

## Coverage Targets

| Area | Minimum |
|------|---------|
| Overall `app/` package | 80% |
| Core business logic services | 95% |

```bash
uv run pytest --cov=app --cov-report=term-missing
```
