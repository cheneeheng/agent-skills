# Error Handling

## API Error Type

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

## Component Error Handling

Components communicate results upward via callback props — never write stores directly (see SvelteKit conventions).

```svelte
<script lang="ts">
  export let sessionId: string;
  export let onSuccess: (state: SessionState) => void;  // parent updates the store

  let error: string | null = null;
  let loading = false;

  async function handleSend() {
    error = null;
    loading = true;
    try {
      const result = await apiClient.sendMessage(sessionId, input);
      onSuccess(result.state);
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
