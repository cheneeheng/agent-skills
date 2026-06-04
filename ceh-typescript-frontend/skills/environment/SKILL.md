---
name: "environment"
description: Load this skill when setting up the project, running scripts, or managing dependencies in a Bun + SvelteKit project. Auto-load whenever bun install, bun add, bun run, or package.json scripts are being used or referenced.
---

# Environment

- Runtime and package manager: **Bun** | Framework: **SvelteKit**
- Lockfile: `bun.lock` — authoritative, never edit manually
- Never commit `.env`

## Commands

| Action | Command |
|--------|---------|
| Install all dependencies | `bun install` |
| Add a production dependency | `bun add <package>` |
| Add a dev dependency | `bun add -d <package>` |
| Start dev server | `bun run dev` |
| Production build | `bun run build` |
| Run unit + component tests | `bun run test` |
| Type check (tsc) | `bun run typecheck` |
| Svelte template check | `bun run check` |
| Lint | `bun run lint` |
| Format check | `bun run format:check` |
