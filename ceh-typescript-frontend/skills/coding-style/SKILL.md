---
name: "coding-style"
description: >
  Load this skill when writing TypeScript types, choosing between type and interface, defining
  enums or const assertions, naming variables or components, organizing imports, or writing
  JSDoc. Auto-load whenever TypeScript conventions are being applied in a SvelteKit codebase.
---

# TypeScript Coding Style

- Line length: **100 characters**
- Never use `any` — use `unknown` with type narrowing if the type is truly unknown
- Prefer `undefined` over `null` for optional values
- Use `?.` and `??`; do not use `||` for defaults on falsy inputs (it collapses `0`, `''`, `false`)

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

```ts
const ChallengeStatus = {
  Open: 'open',
  Resolved: 'resolved',
  Reframed: 'reframed',
} as const;
type ChallengeStatus = typeof ChallengeStatus[keyof typeof ChallengeStatus];
```

## Naming Conventions

| Kind | Convention | Example |
|------|-----------|---------|
| Variables, functions | `camelCase` | `sessionId`, `sendMessage` |
| Types, interfaces | `PascalCase` | `SessionState` |
| Svelte components (filename) | `PascalCase.svelte` | `ReasoningPanel.svelte` |
| Svelte stores | `camelCase` + `Store` suffix | `sessionStore` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |

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

## TypeScript Configuration

`strict: true` in `tsconfig.json` is non-negotiable. Never disable strictness to silence errors. Never use `// @ts-ignore` — fix the type error.

```json
{
  "compilerOptions": {
    "strict": true,
    "moduleResolution": "bundler",
    "target": "ES2022"
  }
}
```

## JSDoc (Required on All Exported Symbols)

```ts
/**
 * Sends a user message and returns the updated session state.
 * @param sessionId - Active session identifier.
 * @param content - User's message text.
 * @returns Updated reasoning state snapshot.
 * @throws {ApiRequestError} On non-2xx response.
 */
export async function sendMessage(sessionId: string, content: string): Promise<SessionState>
```
