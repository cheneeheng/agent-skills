# Environment

- Runtime and package manager: **Bun**
- Framework: **SvelteKit**
- Lockfile: `bun.lockb` — authoritative, never edit manually

Use the `Bash` tool to execute all commands in this table.

| Action | Command |
|--------|---------|
| Install all dependencies | `bun install` |
| Add a production dependency | `bun add <package>` |
| Add a dev dependency | `bun add -d <package>` |
| Start dev server | `bun run dev` |
| Production build | `bun run build` |
| Run unit + component tests | `bun run test` (delegates to Vitest) |
| Type check (tsc) | `bun run typecheck` |
| Svelte template check | `bun run check` (svelte-check) |
| Lint | `bun run lint` (ESLint) |
| Format | `bun run format` (Prettier) |
| Format check only | `bun run format:check` |

**`strict: true` in `tsconfig.json` is non-negotiable. Never commit `.env`.**

## TypeScript Configuration

`tsconfig.json` must include:

```json
{
  "compilerOptions": {
    "strict": true,
    "moduleResolution": "bundler",
    "target": "ES2022"
  }
}
```

Do not disable strictness to silence errors. Fix the underlying type issue. Never use `// @ts-ignore` — fix the type error instead.
