# ceh-typescript-frontend

Engineering standards for the **Bun + SvelteKit + Vitest + Playwright** stack.

## Bundle Skill

| Skill | Invoke | When to load |
|-------|--------|--------------|
| TypeScript Frontend | `/ceh-typescript-frontend:typescript-frontend` | Start of any SvelteKit session |

## Micro-Skills (auto-trigger)

| Skill | Invoke | Triggers when |
|-------|--------|---------------|
| SvelteKit | `/ceh-typescript-frontend:sveltekit` | Editing routes, stores, components, or the API client |
| Frontend Testing | `/ceh-typescript-frontend:frontend-testing` | Writing `.test.ts` or `.spec.ts` files, or MSW handlers |
| Accessibility | `/ceh-typescript-frontend:accessibility` | Writing Svelte component markup |
| Coding Style | `/ceh-typescript-frontend:coding-style` | Applying TypeScript type conventions or import ordering |
| Linting | `/ceh-typescript-frontend:linting` | Configuring or running ESLint, Prettier, or svelte-check |

## Agents

| Agent | Use when |
|-------|----------|
| `ts-unit-tester` | Writing isolated unit tests for TypeScript functions or modules |
| `ts-integration-tester` | Testing components wired with real stores and MSW network handlers |
| `ts-system-tester` | Writing Playwright E2E tests or smoke tests against a running stack |

## Scripts

Called by agents via `bash "${CLAUDE_PLUGIN_ROOT}/scripts/<name>.sh"`.

| Script | Purpose |
|--------|---------|
| `detect-test-framework.sh [root]` | Detects Jest / Vitest / Mocha + Playwright / Cypress in the project |
| `run-unit-tests.sh [file]` | Runs unit tests with the detected runner |
| `check-coverage.sh <file>` | Prints coverage delta for a specific source file |
| `run-integration-tests.sh [pattern]` | Runs integration tests with `NODE_ENV=test` |
| `run-e2e.sh {up\|down\|test\|smoke} [pattern]` | Manages the E2E stack and runs Playwright / Cypress |

## Coverage Target

70% for `src/lib/`. Verified by `check-coverage.sh` after each unit test session.
