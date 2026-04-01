# SvelteKit Conventions

## Route File Naming

| File | Purpose |
|------|---------|
| `+page.svelte` | Page UI component |
| `+page.server.ts` | Server-only load function and form actions (access to private env vars and DB) |
| `+page.ts` | Universal load function (runs on server + client) |
| `+layout.svelte` | Layout wrapper applied to child routes |
| `+layout.server.ts` | Server-only layout load |
| `+error.svelte` | Error page for this route segment |

Use `+page.server.ts` when the load requires server-side credentials or direct database access. Use `+page.ts` for public data that can be fetched client-side.

## Load Functions

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

## Svelte Stores

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

## Components — Props Only, No Direct Store Writes

```svelte
<!-- src/lib/components/ReasoningPanel.svelte -->
<script lang="ts">
  import type { Challenge } from '$lib/types';

  export let challenges: Challenge[];         // Typed props
  export let onChallengeClick: (id: string) => void;  // Callback, not direct store write
</script>
```

Components receive data via props and communicate upward via callbacks or dispatched events. They do not write to stores directly.

## Centralized API Client

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

## Environment Variables

```ts
// Public — safe to expose to the browser
import { PUBLIC_API_BASE_URL } from '$env/static/public';

// Private — server-only (SSR and load functions only)
import { DATABASE_URL } from '$env/static/private';
```

Never use `import.meta.env.VITE_*`. Always use SvelteKit's typed `$env` imports.

## Reactive Declarations

```svelte
<script lang="ts">
  export let challenges: Challenge[];
  $: openCount = challenges.filter(c => c.status === 'open').length;
</script>
```

Do not put complex logic in `$:` blocks — extract it to a named function.
