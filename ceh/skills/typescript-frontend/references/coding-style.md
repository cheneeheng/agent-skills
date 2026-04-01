# Coding Style

- Line length: **100 characters**
- Never use `any` — use `unknown` with type narrowing if the type is truly unknown
- Prefer `undefined` over `null` for optional values
- Use optional chaining `?.` and nullish coalescing `??`
- Do not use `||` for default values on falsy inputs — it collapses `0`, `''`, and `false`

## `type` Is the Default — `interface` Is the Exception

```ts
// Good — use type for data shapes, unions, and aliases
type Status = 'active' | 'archived' | 'deleted';
type SessionState = { sessionId: string; challenges: Challenge[] };

// Only use interface when you intentionally need declaration merging (rare)
interface PluginExtension {
  onLoad(): void;
}
```

## No TypeScript `enum` — Use `const` Assertions

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

## Naming Conventions

| Kind | Convention | Example |
|------|-----------|---------|
| Variables, functions | `camelCase` | `sessionId`, `sendMessage` |
| Types, interfaces | `PascalCase` | `SessionState`, `ChallengeEntity` |
| Svelte components (filename) | `PascalCase.svelte` | `ReasoningPanel.svelte` |
| Svelte stores | `camelCase` + `Store` suffix | `sessionStore`, `reasoningStore` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `API_TIMEOUT_MS` |

## Imports (Three Groups, Separated by Blank Lines)

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

## JSDoc (Required on All Exported Symbols)

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
