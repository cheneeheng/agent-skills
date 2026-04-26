---
name: "linting"
description: >
  Load this skill when configuring or running ESLint, Prettier, svelte-check, or tsc in a
  SvelteKit project. Auto-load whenever eslint.config.js, .prettierrc, or tsconfig.json is
  created or modified, or when lint errors are being diagnosed or resolved.
---

# Linting Conventions

Four checks required before every PR, ESLint configuration with typescript-eslint
type-checked and the Svelte plugin, Prettier configuration for SvelteKit, and svelte-check
for template errors that ESLint cannot catch.

Read [../typescript-frontend/references/linting.md](../typescript-frontend/references/linting.md)
and apply the configuration shown there.
