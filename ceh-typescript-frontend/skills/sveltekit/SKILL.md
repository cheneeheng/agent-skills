---
name: "sveltekit"
description: >
  Load this skill when working on SvelteKit frontend code: adding or modifying routes, writing
  load functions, managing Svelte stores, building components, integrating the API client, or
  handling component-level errors. Auto-load whenever a +page.svelte, +page.server.ts, +page.ts,
  store file, or component file is created or modified.
---

# SvelteKit Conventions

Route file naming and usage, server vs universal load functions, Svelte store rules (updated
only from API responses), component props and callback pattern (no direct store writes),
centralized typed API client, SvelteKit typed env imports, reactive declarations, and component
error handling with ApiRequestError.

Read both reference files and apply the conventions defined there:

- [../typescript-frontend/references/sveltekit.md](../typescript-frontend/references/sveltekit.md) — routing, load functions, stores, components, API client, env vars
- [../typescript-frontend/references/error-handling.md](../typescript-frontend/references/error-handling.md) — ApiRequestError type, component error handling pattern
