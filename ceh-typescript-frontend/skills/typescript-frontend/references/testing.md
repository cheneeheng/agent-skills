# Testing

Frameworks: **Vitest** (unit + component), **@testing-library/svelte** (component rendering), **MSW** (API request mocking), **Playwright** (E2E)

## Test Structure

```
frontend/
└── tests/
    ├── unit/       # Pure function tests — no DOM, no fetch
    ├── component/  # Svelte component render and interaction tests
    └── e2e/        # Full browser tests against the running application
```

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

Use `@testing-library/svelte`. Test what the user sees and interacts with. Do not test implementation details.

```ts
import { render, screen, fireEvent } from '@testing-library/svelte';
import ReasoningPanel from '$lib/components/ReasoningPanel.svelte';

it('renders open challenges', () => {
  const state = buildTestState({ challenges: [mockOpenChallenge()] });
  render(ReasoningPanel, { props: { state } });
  expect(screen.getByRole('status', { name: /open/i })).toBeInTheDocument();
});
```

Do **not** use snapshot tests — they hide intentional vs unintentional changes. Use explicit assertions on rendered content.

## API Mocking with MSW — Do Not Mock `fetch` Directly

MSW intercepts at the network layer, making tests closer to reality:

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

E2E tests are expensive. Keep them focused on happy paths and critical failure modes. Do not duplicate unit or component test coverage.

**Coverage target:** 70% for `src/lib/`
