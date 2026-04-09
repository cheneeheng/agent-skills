# CI Requirements

All checks must pass before merge. No exceptions.

## Python Backend

```bash
uv run ruff check .           # Lint
uv run ruff format --check .  # Format check
uv run mypy .                 # Type check (strict)
uv run pytest --cov=app       # Tests + coverage gate
```

Coverage gates: 80% for `app/`, 95% for core business logic.

## TypeScript Frontend

```bash
bun run lint          # ESLint
bun run format:check  # Prettier
bun run check         # svelte-check (template + a11y)
bun run typecheck     # tsc --noEmit
bun run test          # Vitest
```

Coverage gate: 70% for `src/lib/`.

## Both

- Docker images (`backend/Dockerfile`, `frontend/Dockerfile`) must build successfully
- No committed secrets (Gitleaks or equivalent)

## Branch Protection Rules

- Direct pushes to `main` are blocked
- All required CI checks must pass before merge is allowed
- At least 1 approved review required
- Branch must be up-to-date with `main` before merge
- No force-push to `main`
