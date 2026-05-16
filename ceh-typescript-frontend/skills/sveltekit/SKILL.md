---
name: "sveltekit"
description: >
  Load this skill when adding or modifying SvelteKit routes, writing load functions, managing
  Svelte stores, or building components. Auto-load whenever a +page.svelte, +page.server.ts,
  +page.ts, store, or component file is created or modified.
---

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

Use `+page.server.ts` when the load requires server-side credentials or direct database access.

## Load Functions

```ts
export const load: PageServerLoad = async ({ params }) => {
  const session = await apiClient.getSession(params.session_id);
  if (!session) error(404, 'Session not found');  // SvelteKit error(), not throw new Error()
  return { session };
};
```

- Throw `error()` from `@sveltejs/kit` for HTTP errors
- Use `redirect()` from `@sveltejs/kit` for redirects — do not call `goto()` inside load functions
- Load functions return data; they do not directly mutate state

## Svelte Stores

Stores live in `src/lib/stores/`. Updated **only** from API responses — never mutated directly by components.

```ts
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
<script lang="ts">
  export let challenges: Challenge[];
  export let onChallengeClick: (id: string) => void;  // callback, not direct store write
</script>
```

## Centralized API Client

All `fetch` calls go through `src/lib/api/client.ts`. Components and stores never call `fetch` directly.

```ts
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
import { PUBLIC_API_BASE_URL } from '$env/static/public';  // safe for browser
import { DATABASE_URL } from '$env/static/private';         // server-only
```

Never use `import.meta.env.VITE_*`.

## Error Handling

```ts
class ApiRequestError extends Error {
  constructor(public readonly status: number, public readonly error: ApiError) {
    super(error.message);
  }
}
```

Component pattern:
```svelte
<script lang="ts">
  let error: string | null = null;
  let loading = false;

  async function handleSend() {
    error = null; loading = true;
    try {
      const result = await apiClient.sendMessage(sessionId, input);
      onSuccess(result.state);
    } catch (e) {
      error = e instanceof ApiRequestError
        ? e.error.message
        : 'An unexpected error occurred. Please try again.';
    } finally { loading = false; }
  }
</script>

{#if error}<p class="error">{error}</p>{/if}
```

- Never expose internal error codes or stack traces to users
- Map `error.code` values to user-friendly messages in a centralized map
- Always show the `correlation_id` so users can report it

## Reactive Declarations

```svelte
<script lang="ts">
  export let challenges: Challenge[];
  $: openCount = challenges.filter(c => c.status === 'open').length;
</script>
```

Do not put complex logic in `$:` blocks — extract it to a named function.
