---
name: "frontend-testing"
description: >
  Load this skill when writing frontend tests: unit tests for pure functions, component tests
  with Testing Library, API mocking with MSW, or Playwright E2E tests. Auto-load whenever a
  .test.ts or .spec.ts file is created or modified, an MSW handler is written, or a Playwright
  test scenario is defined.
---

# Frontend Testing

Vitest unit tests, @testing-library/svelte component tests (test what the user sees, not
implementation details), MSW for API mocking at the network layer (never mock fetch directly),
Playwright for critical-path E2E tests, test file naming conventions, and the 70% coverage
target for src/lib/.

Read [../typescript-frontend/references/testing.md](../typescript-frontend/references/testing.md)
and apply the patterns and rules defined there.
