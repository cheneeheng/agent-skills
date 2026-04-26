---
name: "frontend-testing"
description: >
  Load this skill when writing Vitest unit tests, Testing Library component tests, MSW mocks,
  or Playwright E2E tests. Auto-load whenever a .test.ts or .spec.ts file is created or
  modified, or MSW handlers are being written.
---

# Frontend Testing

Vitest unit tests, @testing-library/svelte component tests (test what the user sees, not
implementation details), MSW for API mocking at the network layer (never mock fetch directly),
Playwright for critical-path E2E tests, test file naming conventions, and the 70% coverage
target for src/lib/.

Read [../typescript-frontend/references/testing.md](../typescript-frontend/references/testing.md)
and apply the patterns and rules defined there.
