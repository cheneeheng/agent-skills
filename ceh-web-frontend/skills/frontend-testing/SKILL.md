---
name: "frontend-testing"
description: Load this skill when writing Vitest unit tests, Testing Library component tests, MSW mocks, or Playwright E2E tests for any web frontend. Auto-load whenever a .test.ts, .test.tsx, or .spec.ts file is created or modified, or MSW handlers are being written. Framework-agnostic — Vitest, Testing Library, MSW, and Playwright serve SvelteKit and React alike.
---

# Frontend Testing

Frameworks: **Vitest** (unit + component), **@testing-library/svelte**, **MSW** (API mocking), **Playwright** (E2E)

> The examples below use Vitest APIs. If the project already uses Jest or Mocha instead, adapt the equivalent calls and match the runner in the repo — the `ts-unit-tester` agent detects which one applies.

| Folder | Contents |
|--------|---------|
| `tests/unit/` | Pure function tests — no DOM, no fetch |
| `tests/component/` | Svelte component render and interaction tests |
| `tests/e2e/` | Full browser tests against the running application |

Naming: `<subject>.test.ts` for unit/component, `<scenario>.spec.ts` for E2E. One behavior per test.

## Unit Tests — No DOM, No Network

```ts
import { describe, it, expect } from 'vitest';
import { deriveGraphFromState } from '$lib/reasoning/graph';

describe('deriveGraphFromState', () => {
  it('creates a node for each challenge', () => {
    const state = buildTestState({ challenges: [mockChallenge()] });
    const graph = deriveGraphFromState(state);
    expect(graph.nodes).toHaveLength(1);
  });
});
```

## Component Tests — Test What the User Sees

Use `@testing-library/svelte` (SvelteKit) or `@testing-library/react` (React). Do not test implementation details. No snapshot tests — explicit assertions only.

```ts
import { render, screen } from '@testing-library/svelte';
import ReasoningPanel from '$lib/components/ReasoningPanel.svelte';

it('renders open challenges', () => {
  render(ReasoningPanel, { props: { state: buildTestState({ challenges: [mockOpenChallenge()] }) } });
  expect(screen.getByRole('status', { name: /open/i })).toBeInTheDocument();
});
```

## API Mocking with MSW — Do Not Mock `fetch` Directly

```ts
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.post('/sessions/:id/message', () =>
    HttpResponse.json({ chat_message: '...', reasoning_events: [] })
  )
);

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## E2E with Playwright — Critical Paths Only

```ts
import { test, expect } from '@playwright/test';

test('user can start a session and receive a challenge', async ({ page }) => {
  await page.goto('/');
  await page.fill('[data-testid="topic-input"]', 'We should rewrite in Rust');
  await page.click('[data-testid="start-session"]');
  await expect(page.locator('[data-testid="reasoning-panel"]')).toBeVisible();
});
```

Do not duplicate unit or component test coverage in E2E tests.

**Coverage target:** 70% for `src/lib/`
