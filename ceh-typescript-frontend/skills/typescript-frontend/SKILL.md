---
name: "typescript-frontend"
description: >
  Load this skill at the start of any session involving the Bun + SvelteKit + Vitest + Playwright
  frontend stack. Covers package management, TypeScript configuration, linting, testing, SvelteKit
  routing and stores, API client patterns, error handling, and accessibility. Use when writing,
  reviewing, or debugging any frontend TypeScript code.
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
