---
name: "typescript-frontend"
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

# TypeScript Frontend

Engineering standards for the Bun + SvelteKit + Vitest + Playwright stack. Covers Bun package
management, TypeScript strict mode, type vs interface conventions, four required lint checks,
Vitest and Testing Library patterns, MSW API mocking, Playwright E2E tests, SvelteKit routing
and load functions, Svelte store rules, centralized API client, and accessibility requirements.

## References

Load the relevant file for the topic at hand.

| File | Topic |
|------|-------|
| [references/environment.md](references/environment.md) | Bun commands, tsconfig strict mode requirements |
| [references/coding-style.md](references/coding-style.md) | type vs interface, const assertions, naming, imports, JSDoc |
| [references/linting.md](references/linting.md) | Four required checks: ESLint, Prettier, svelte-check, tsc |
| [references/testing.md](references/testing.md) | Vitest, Testing Library, MSW mocking, Playwright E2E, coverage target |
| [references/sveltekit.md](references/sveltekit.md) | Route files, load functions, stores, components, API client, env vars |
| [references/error-handling.md](references/error-handling.md) | ApiRequestError type, component error handling pattern |
| [references/accessibility.md](references/accessibility.md) | Keyboard access, semantic HTML, svelte-check a11y rules |
