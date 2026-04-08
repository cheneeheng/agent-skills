---
name: "python-testing"
description: >
  Load this skill when writing Python tests: adding unit tests, integration tests, test fixtures,
  or mocks. Auto-load whenever a test file is created or modified, a pytest fixture is written,
  or a decision is made about what to mock vs what to test against a real dependency.
---

# Python Testing

pytest with pytest-asyncio, unit vs integration test structure, real-database integration test
rules (never mock PostgreSQL), LLM API mocking, test naming conventions, and coverage targets.
Each test covers one logical behavior. Integration tests run in a transaction that rolls back
after the test.

Read [../python-backend/references/testing.md](../python-backend/references/testing.md)
and apply the patterns and rules defined there.
