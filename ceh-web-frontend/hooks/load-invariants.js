#!/usr/bin/env node
// SessionStart hook — injects the frontend invariants as always-on context.
// These under-trigger as auto-load skills because they fire on implicit mid-turn decisions
// (naming, writing markup, mutating state) with no signal in the user's prompt. The detailed
// patterns and code stay in the skills (load on demand for depth); this block is the compact
// enforcement layer. Self-sufficient. Cross-platform (Node), wired via hooks/hooks.json.

const invariants = `FRONTEND INVARIANTS (ceh-web-frontend) — apply to all frontend work in this project.
Stack: Bun + Vite, SvelteKit or React. These are non-negotiable defaults. For full patterns and
code behind any rule, load the matching skill via the Skill tool as \`ceh-web-frontend:<name>\`,
where \`<name>\` is the tag shown in brackets below (e.g. \`ceh-web-frontend:accessibility\`).

Types & style [environment]:
- Never use \`any\` — use \`unknown\` with narrowing. Prefer \`undefined\` over \`null\`. Use \`?.\`/\`??\`, not \`||\` for defaults (it collapses \`0\`, \`''\`, \`false\`).
- \`type\` is the default; \`interface\` only when you need declaration merging. No TS \`enum\` — use \`as const\` objects. tsconfig \`strict: true\`; never \`// @ts-ignore\`.
- Naming: \`camelCase\` vars/functions, \`PascalCase\` types and component files, \`UPPER_SNAKE_CASE\` constants. Import local code via the path alias, never deep relative paths.

Components & data flow [sveltekit / react-vite]:
- Components are presentational — they render props and call callbacks; business logic lives in services/hooks/stores, not in render.
- Shared state is updated only from API responses — components never mutate shared state directly; pass callbacks/props instead.
- All \`fetch\` goes through the centralized API client (\`$lib/api\`) — components never call \`fetch\` directly.
- SvelteKit: Svelte 5 runes (\`$props\`/\`$state\`/\`$derived\`), \`onclick\` not \`on:click\`, \`error()\`/\`redirect()\` from \`@sveltejs/kit\`. React: Rules of Hooks, exhaustive effect deps, error boundaries.

Accessibility [accessibility]:
- Native semantic HTML first (\`<button>\`, \`<nav>\`, \`<main>\`) — never a \`<div>\` with \`role="button"\`. Add ARIA only when no native element fits.
- Every mouse action must be keyboard-reachable. Never remove the focus indicator. Images need \`alt\` (empty \`alt=""\` for decorative).
- Text contrast >= 4.5:1 (3:1 for large text). Never convey meaning by color alone. Fix all a11y warnings before opening a PR.

Environment [environment]:
- Bun is the runtime and package manager; never edit the lockfile manually. Never commit \`.env\`.`;

const payload = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: invariants
  }
};

process.stdout.write(JSON.stringify(payload));
