---
name: "scaffold-web-frontend"
description: Load this skill when starting or scaffolding a new web frontend (SvelteKit or React + Vite): creating the source layout, $lib/api client boundary, test folders, and .gitignore. Trigger when the user says "start/scaffold a Svelte app", "scaffold a React app", or sets up a fresh frontend repo. For the backend use scaffold-python-service.
---

# Scaffold a Web Frontend

Bun + Vite. SvelteKit and React share the same layout conventions; only the framework files differ.

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api/            # centralized API client — the only place fetch is called
│   │   ├── components/     # presentational components (PascalCase)
│   │   ├── stores/         # SvelteKit only — shared state, updated from API responses
│   │   └── types.ts
│   ├── routes/             # SvelteKit routes  (React: src/routes or React Router config)
│   └── app.html / main.tsx
├── tests/
│   ├── unit/
│   ├── component/
│   └── e2e/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .gitignore
```

## Initial Config

- `package.json` scripts for dev/build/test/lint/typecheck — see `ceh-web-frontend:environment`.
- `tsconfig.json` with `strict: true`; ESLint + Prettier configured.
- Components are presentational; all `fetch` goes through `src/lib/api`.

## .gitignore

```
node_modules/
.svelte-kit/
dist/
build/
.env
.env.*
!.env.example
.DS_Store
```
