---
name: "linting"
description: Load this skill when configuring or running ESLint, Prettier, svelte-check, or tsc in a SvelteKit project. Auto-load whenever eslint.config.js, .prettierrc, or tsconfig.json is created or modified, or when lint errors are being diagnosed or resolved.
---

# Linting and Quality Checks

All four checks must pass before a PR is opened:

```bash
bun run lint          # ESLint with typescript-eslint recommended-type-checked + svelte plugin
bun run format:check  # Prettier (does not modify files)
bun run check         # svelte-check — catches .svelte template errors ESLint cannot see
bun run typecheck     # tsc --noEmit
```

`svelte-check` is not optional — catches prop type mismatches, missing required props, and a11y warnings that ESLint cannot see.

## ESLint Configuration

```js
// eslint.config.js
import ts from '@typescript-eslint/eslint-plugin';
import svelte from 'eslint-plugin-svelte';

export default [
  ...ts.configs['recommended-type-checked'],
  ...svelte.configs['flat/recommended'],
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
```

## Prettier Configuration

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "all",
  "plugins": ["prettier-plugin-svelte"]
}
```
