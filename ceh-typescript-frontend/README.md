# ceh-typescript-frontend

Engineering standards for the **Bun + SvelteKit + Vitest + Playwright** stack.

## Skills (auto-trigger)

| Skill | Invoke | Triggers when |
|-------|--------|---------------|
| Environment | `/ceh-typescript-frontend:environment` | Setting up the project, running scripts, or managing Bun dependencies |
| SvelteKit | `/ceh-typescript-frontend:sveltekit` | Editing routes, stores, components, or the API client |
| Frontend Testing | `/ceh-typescript-frontend:frontend-testing` | Writing `.test.ts` or `.spec.ts` files, or MSW handlers |
| Accessibility | `/ceh-typescript-frontend:accessibility` | Writing Svelte component markup |
| Coding Style | `/ceh-typescript-frontend:coding-style` | Applying TypeScript type conventions, tsconfig, or import ordering |
| Linting | `/ceh-typescript-frontend:linting` | Configuring or running ESLint, Prettier, or svelte-check |

## Hooks

This plugin ships a `SessionStart` hook (`hooks/hooks.json` → `hooks/load-invariants.js`) that
injects the **frontend invariants** as always-on context. It fires on the `startup`, `clear`, and
`compact` events and activates automatically when the plugin is enabled.

**Why a hook and not just skills:** the load-bearing rules here (no `any`, `type`-default, the
data-flow rules — shared state updated only from API responses, components never call `fetch` or
mutate stores directly — and the accessibility baseline) are *invariants* that must hold on every
relevant change. But skill auto-loading is evaluated against the user's prompt at the start of a
turn, so the invariant skills (`coding-style`, `accessibility`, and the data-flow half of
`sveltekit`) reliably under-fire — nothing in "add a panel component" signals "this is
accessibility/data-flow sensitive." The action skills (`environment`, `frontend-testing`,
`linting`) trigger fine and stay on-demand. The hook injects a compact version of the invariants
every session; each rule is tagged with the skill (e.g. `[accessibility]`) that documents it in
depth, loadable as `ceh-typescript-frontend:<name>`. Stack: Svelte 5 (runes).

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
