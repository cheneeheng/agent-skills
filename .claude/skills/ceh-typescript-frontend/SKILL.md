---
name: "ceh-typescript-frontend"
description: >
  Load this skill when writing, reviewing, or debugging TypeScript and SvelteKit frontend code
  using the Bun + SvelteKit + Vitest + Playwright stack. Covers the full development loop:
  managing dependencies with Bun, enforcing TypeScript strict mode, using type vs interface and
  const-assertion enum patterns, running all four required lint checks (ESLint, Prettier,
  svelte-check, tsc), writing unit tests with Vitest, component tests with Testing Library,
  mocking API calls with MSW (not direct fetch mocking), writing Playwright E2E tests, structuring
  SvelteKit routes with server vs universal load functions, managing reactive state with Svelte
  stores (updated only from API responses), organizing typed components with props and callbacks,
  and centralizing all fetch calls through a typed API client. Use this skill any time you touch
  frontend TypeScript — new components, store logic, routing, API integration, testing, or PR review.
---

# TypeScript and SvelteKit Frontend Engineering Standards: Bun Runtime and Package Management, TypeScript Strict Mode Configuration, type vs interface Convention and const-assertion Enum Pattern, ESLint with typescript-eslint Recommended Type-Checked Rules, Prettier Formatting, svelte-check Template and Accessibility Validation, Vitest Unit Testing, Testing Library Component Tests, MSW API Request Mocking, Playwright End-to-End Testing, SvelteKit File-Based Routing and Server vs Universal Load Functions, Svelte Stores Updated Only From API Responses, Centralized Typed API Client, Typed Component Props and Callback Pattern, Error Handling in Components

---

## Environment

- Runtime and package manager: **Bun**
- Framework: **SvelteKit**
- Lockfile: `bun.lockb` — authoritative, never edit manually

| Action | Command |
|--------|---------|
| Install all dependencies | `bun install` |
| Add a production dependency | `bun add <package>` |
| Add a dev dependency | `bun add -d <package>` |
| Start dev server | `bun run dev` |
| Production build | `bun run build` |
| Run unit + component tests | `bun run test` (delegates to Vitest) |
| Type check (tsc) | `bun run typecheck` |
| Svelte template check | `bun run check` (svelte-check) |
| Lint | `bun run lint` (ESLint) |
| Format | `bun run format` (Prettier) |
| Format check only | `bun run format:check` |

**`strict: true` in `tsconfig.json` is non-negotiable. Never commit `.env`.**

---

## TypeScript Configuration

`tsconfig.json` must include:

```json
{
  "compilerOptions": {
    "strict": true,
    "moduleResolution": "bundler",
    "target": "ES2022"
  }
}
```

Do not disable strictness to silence errors. Fix the underlying type issue. Never use `// @ts-ignore` — fix the type error instead.

---

## Coding Style

- Line length: **100 characters**
- Never use `any` — use `unknown` with type narrowing if the type is truly unknown
- Prefer `undefined` over `null` for optional values
- Use optional chaining `?.` and nullish coalescing `??`
- Do not use `||` for default values on falsy inputs — it collapses `0`, `''`, and `false`

### `type` Is the Default — `interface` Is the Exception

```ts
// Good — use type for data shapes, unions, and aliases
type Status = 'active' | 'archived' | 'deleted';
type SessionState = { sessionId: string; challenges: Challenge[] };

// Only use interface when you intentionally need declaration merging (rare)
interface PluginExtension {
  onLoad(): void;
}
```

### No TypeScript `enum` — Use `const` Assertions

TypeScript enums produce surprising runtime behavior and inflate bundle size. Use `const` assertions instead:

```ts
// Good
const ChallengeStatus = {
  Open: 'open',
  Resolved: 'resolved',
  Reframed: 'reframed',
} as const;
type ChallengeStatus = typeof ChallengeStatus[keyof typeof ChallengeStatus];

// Bad
enum ChallengeStatus { Open = 'open', Resolved = 'resolved' }
```

### Naming Conventions

| Kind | Convention | Example |
|------|-----------|---------|
| Variables, functions | `camelCase` | `sessionId`, `sendMessage` |
| Types, interfaces | `PascalCase` | `SessionState`, `ChallengeEntity` |
| Svelte components (filename) | `PascalCase.svelte` | `ReasoningPanel.svelte` |
| Svelte stores | `camelCase` + `Store` suffix | `sessionStore`, `reasoningStore` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `API_TIMEOUT_MS` |

### Imports (Three Groups, Separated by Blank Lines)

```ts
// 1. Third-party packages
import { writable, derived } from 'svelte/store';

// 2. SvelteKit built-ins
import { goto, invalidateAll } from '$app/navigation';
import { page } from '$app/stores';

// 3. Local ($lib alias — always, never relative paths)
import type { SessionState } from '$lib/types';
import { apiClient } from '$lib/api/client';
```

Use the `$lib` alias for all local imports. Never use `../../` relative path chains.

### JSDoc (Required on All Exported Symbols)

```ts
/**
 * Sends a user message and returns the updated session state.
 *
 * @param sessionId - The active session identifier.
 * @param content - The user's message text.
 * @returns Updated reasoning state snapshot from the backend.
 * @throws {ApiRequestError} If the backend returns a non-2xx response.
 */
export async function sendMessage(sessionId: string, content: string): Promise<SessionState> {
```

---

## Linting and Quality Checks

All four checks must pass before a PR is opened:

```bash
bun run lint          # ESLint with typescript-eslint recommended-type-checked + svelte plugin
bun run format:check  # Prettier (does not modify files)
bun run check         # svelte-check — catches .svelte template errors ESLint cannot see
bun run typecheck     # tsc --noEmit
```

`svelte-check` is not optional. It catches prop type mismatches, missing required props, invalid reactive declarations, and accessibility warnings that ESLint misses entirely.

### ESLint Configuration

```js
// eslint.config.js
import ts from '@typescript-eslint/eslint-plugin';
import svelte from 'eslint-plugin-svelte';

export default [
  ...ts.configs['recommended-type-checked'],
  ...svelte.configs['flat/recommended'],
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
```

### Prettier Configuration

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "all",
  "plugins": ["prettier-plugin-svelte"]
}
```

---

## Testing

Frameworks: **Vitest** (unit + component), **@testing-library/svelte** (component rendering), **MSW** (API request mocking), **Playwright** (E2E)

### Test Structure

```
frontend/
└── tests/
    ├── unit/       # Pure function tests — no DOM, no fetch
    ├── component/  # Svelte component render and interaction tests
    └── e2e/        # Full browser tests against the running application
```

Naming: `<subject>.test.ts` for unit/component, `<scenario>.spec.ts` for E2E. One behavior per test.

### Unit Tests — No DOM, No Network

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

### Component Tests — Test What the User Sees

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

### API Mocking with MSW — Do Not Mock `fetch` Directly

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

### E2E with Playwright — Critical Paths Only

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

---

## SvelteKit Conventions

### Route File Naming

| File | Purpose |
|------|---------|
| `+page.svelte` | Page UI component |
| `+page.server.ts` | Server-only load function and form actions (access to private env vars and DB) |
| `+page.ts` | Universal load function (runs on server + client) |
| `+layout.svelte` | Layout wrapper applied to child routes |
| `+layout.server.ts` | Server-only layout load |
| `+error.svelte` | Error page for this route segment |

Use `+page.server.ts` when the load requires server-side credentials or direct database access. Use `+page.ts` for public data that can be fetched client-side.

### Load Functions

```ts
// +page.server.ts
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import { apiClient } from '$lib/api/client';

export const load: PageServerLoad = async ({ params }) => {
  const session = await apiClient.getSession(params.session_id);
  if (!session) error(404, 'Session not found');  // SvelteKit error(), not throw new Error()
  return { session };
};
```

- Throw `error()` from `@sveltejs/kit` for HTTP errors — not plain JavaScript `Error`
- Use `redirect()` from `@sveltejs/kit` for redirects — do not call `goto()` inside load functions
- Load functions return data; they do not directly mutate state

### Svelte Stores

Stores live in `src/lib/stores/`. They are updated **only** from API responses — never mutated directly by components.

```ts
// src/lib/stores/session.ts
import { writable, derived } from 'svelte/store';
import type { SessionState } from '$lib/types';

export const sessionStore = writable<SessionState | null>(null);

export const openChallenges = derived(
  sessionStore,
  ($session) => $session?.challenges.filter((c) => c.status === 'open') ?? []
);
```

- Derived stores are preferred over computed values inside components
- Do not define stores inside components — they live in `$lib/stores/`

### Components — Props Only, No Direct Store Writes

```svelte
<!-- src/lib/components/ReasoningPanel.svelte -->
<script lang="ts">
  import type { Challenge } from '$lib/types';

  export let challenges: Challenge[];         // Typed props
  export let onChallengeClick: (id: string) => void;  // Callback, not direct store write
</script>
```

Components receive data via props and communicate upward via callbacks or dispatched events. They do not write to stores directly.

### Centralized API Client

All `fetch` calls go through a single typed client in `src/lib/api/client.ts`. Components and stores never call `fetch` directly.

```ts
// src/lib/api/client.ts
import { PUBLIC_API_BASE_URL } from '$env/static/public';
import type { SessionState, MessageResponse } from '$lib/types';

export const apiClient = {
  async sendMessage(sessionId: string, content: string): Promise<MessageResponse> {
    const response = await fetch(`${PUBLIC_API_BASE_URL}/sessions/${sessionId}/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    });
    if (!response.ok) {
      const err = await response.json();
      throw new ApiRequestError(response.status, err.error);
    }
    return response.json();
  },
};
```

### Environment Variables

```ts
// Public — safe to expose to the browser
import { PUBLIC_API_BASE_URL } from '$env/static/public';

// Private — server-only (SSR and load functions only)
import { DATABASE_URL } from '$env/static/private';
```

Never use `import.meta.env.VITE_*`. Always use SvelteKit's typed `$env` imports.

### Reactive Declarations

```svelte
<script lang="ts">
  export let challenges: Challenge[];
  $: openCount = challenges.filter(c => c.status === 'open').length;
</script>
```

Do not put complex logic in `$:` blocks — extract it to a named function.

---

## Error Handling

### API Error Type

```ts
type ApiError = {
  code: string;
  message: string;
  correlation_id: string;
};

class ApiRequestError extends Error {
  constructor(
    public readonly status: number,
    public readonly error: ApiError
  ) {
    super(error.message);
  }
}
```

### Component Error Handling

```svelte
<script lang="ts">
  let error: string | null = null;
  let loading = false;

  async function handleSend() {
    error = null;
    loading = true;
    try {
      const result = await apiClient.sendMessage(sessionId, input);
      sessionStore.set(result.state);
    } catch (e) {
      error = e instanceof ApiRequestError
        ? e.error.message
        : 'An unexpected error occurred. Please try again.';
    } finally {
      loading = false;
    }
  }
</script>

{#if error}
  <p class="error">{error}</p>
{/if}
```

- Never expose internal error codes or stack traces to users
- Map `error.code` values to user-friendly messages in a centralized map
- Always show the `correlation_id` when displaying errors so users can report it

---

## Accessibility

- All interactive elements must be keyboard-accessible
- Images must have `alt` attributes
- Use semantic HTML elements (`<button>`, `<nav>`, `<main>`) — not `<div>` for everything
- `svelte-check` runs a11y checks — fix all warnings before opening a PR
