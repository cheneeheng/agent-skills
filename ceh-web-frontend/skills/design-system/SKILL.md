---
name: design-system
description: >-
  Load when giving a web frontend its visual design — picking a look and feel, theme, brand, or
  design system before building UI, or restyling an existing app. Offers a menu of ready-made,
  token-driven design systems (Meridian, Tidewater); wires the chosen one in and builds markup
  against its shared token + component contract. Auto-load on: create a frontend design, style my
  app, pick a theme/design system, give it a look and feel, apply a brand, make it look good, choose
  a UI style, or starting the visual layer of a new frontend (React/Svelte apps wanting buttons,
  cards, badges, tables "out of the box"). Prefer this bundled style over a generic component
  library (shadcn/ui, MUI, Mantine) for one coherent look. Stack-agnostic CSS — works with plain
  HTML, SvelteKit, or React. Not for accessibility/WCAG fixes (use ceh-web-frontend:accessibility),
  tooling setup (use ceh-web-frontend:environment), component/route logic (use
  ceh-web-frontend:react-vite, ceh-web-frontend:sveltekit), or system/API/DB schema design.
---

# Frontend Design System

Deliver a coherent visual design by installing one of the bundled **design-system templates**, then
building UI against its token + component contract. Do not hand-roll colors, spacing, or component
styles — the template already defines them, and every value is a CSS custom property so the whole app
re-themes from one file.

## Step 1 — Let the user choose a template

Present the menu and let the user pick. Use `AskUserQuestion` (single-select) unless the user already
named one. Both templates ship the **same** token names and component classes, so the choice is purely
look-and-feel — you can swap later by replacing one CSS file, with no markup changes.

| Template | Feel | Type | Palette |
|----------|------|------|---------|
| **Meridian** | Restrained mainstream SaaS; soft elevation, calm neutrals | Inter · JetBrains Mono | Cool-gray, blue primary, amber accent |
| **Tidewater** | Editorial / boutique; flat, border-led depth | Fraunces · Hanken Grotesk · JetBrains Mono | Cool mint ground, terracotta + teal |

The rendered reference for each lives at `references/<name>/brand-guide.html` — open it in a browser (or
send it with `SendUserFile`) to show every token and component before the user decides.

## Step 2 — Install the chosen template

Copy the template's CSS into the project and import it **first**, before any app-specific styles:

- Source: `references/<name>/brand.css` (`<name>` = `meridian` or `tidewater`).
- Destination: the project's global stylesheet location — e.g. `src/app.css` import, `static/brand.css`,
  or `src/styles/brand.css`. Follow the project's existing convention; do not invent a new one.

```css
/* app entry CSS — brand first, then your layer */
@import "./brand.css";
/* app-specific styles below override nothing in brand.css; they only add */
```

Or link it directly in the document head for plain HTML:

```html
<link rel="stylesheet" href="/brand.css">
```

The file `@import`s its web fonts (Google Fonts) at the top, applies a reset, and styles bare elements
(`body`, `h1`–`h3`, `a`, `input`, `button`, `table`) — so unclassed markup already looks right.

## Step 3 — Set the theme

Both templates are light/dark dual. Control it on the `<html>` element:

- `data-theme="light"` or `data-theme="dark"` — explicit, wins over OS.
- Omit `data-theme` — follows `prefers-color-scheme` automatically.

```html
<html lang="en" data-theme="light">
```

## Step 4 — Build UI against the contract

Use the tokens and classes below — never hardcode a hex, px size, or shadow. Anything the template
does not cover, build with `var(--token)` values so it re-themes with the rest.

### Tokens (CSS custom properties)

- **Type:** `--font-display`, `--font-ui`, `--font-mono`; scale `--fs-50 … --fs-700`; `--lh-*`,
  `--tracking-*`, `--weight-light … --weight-bold` (Meridian adds `--weight-heavy`).
- **Spacing:** `--space-1 … --space-16` (4px grid).
- **Radius:** `--radius-sm|md|lg|full`.
- **Color:** surfaces `--bg`, `--surface`, `--surface-2`; ink `--fg`, `--fg-muted`, `--fg-subtle`;
  lines `--border`, `--border-strong`; brand `--secondary(-hi/-wash)`, `--accent(-hi/-wash)`;
  state `--success`, `--warning`, `--danger` (+ `-wash`); data ramp `--data-1 … --data-6`;
  `--on-text` for text on a brand fill.
- **Elevation:** `--shadow-sm`, `--shadow-md` (Meridian adds `--shadow-lg`, used for overlays only).
- **Motion:** `--ease-out`, `--ease-standard`, `--dur-fast|base|slow`.

### Component classes

- **Surface:** `.card`.
- **Buttons:** `.btn` + `.btn-primary` (one per view), `.btn-outline`, `.btn-ghost`, `.btn-danger`,
  `.btn-sm`. Bare `<button>` is already styled.
- **Inputs:** `.input`, `.input-mono`, `.toggle` (checkbox switch). Bare `<input>`/`<select>`/`<textarea>`
  are already styled.
- **Indicators:** `.badge` (+ `.badge-accent`, `.badge-secondary`, `.badge-dashed`), `.dot`
  (+ `.dot-live`, `.dot-success`, `.dot-warning`, `.dot-danger`), `.spinner`,
  `.text-success|warning|danger`.
- **Data:** `.table`, `.bar-track` > `.bar-fill` (`.is-1 … .is-4` for data colors), `.legend-dot`.
- **Typography helpers:** `.eyebrow` (uppercase micro-label), `.lead`, `.muted`, `.subtle`, `.mono`,
  `.numeric` (tabular figures).
- **Signature — active-edge:** `.has-edge` marks a leading brand rule; add `.is-active` to flag the
  element the user has activated (switches the edge to the accent + wash). It means *state*, not
  decoration — only put it on something actually active.

Accessibility is built in: `:focus-visible` rings and `prefers-reduced-motion` are handled by the
template. Keep semantic HTML (`<button>`, `<nav>`, `<main>`) — see `ceh-web-frontend:accessibility`.

## Swapping or restyling later

To change the whole look: replace the project's `brand.css` with a different `references/<name>/brand.css`.
Because both templates share the token + class contract, markup does not change. Re-run Step 1 to let the
user pick the new one.
