---
name: ui-design
description: >-
  Load when making any frontend UI visual design decision — laying out a page or app shell, placing
  navigation, deciding whether a title/section/card appears, establishing hierarchy and spacing, or
  picking a look and feel, theme, or brand before building UI, or restyling an existing app. Covers
  the full visual layer: layout archetypes, hierarchy, navigation placement, color/depth usage,
  empty/loading/error states, density, and a bundled token-driven theme (Meridian, Tidewater).
  Auto-load on: design the UI, lay out this page, where should the nav go, make it look
  good/modern/professional, style my app, pick a theme/design system, apply a brand, review this UI
  design, or starting the visual layer of a new frontend. Framework-agnostic — plain HTML,
  SvelteKit, React, or anything else. Not for accessibility/WCAG fixes (accessibility), tooling
  setup (environment), component/route logic (react-vite, sveltekit), or API/DB schema design.
---

# Frontend UI Visual Design

Deliver a UI that is modern, intuitive, and coherent by working in two layers, in this order:

1. **Design decisions** — layout, hierarchy, navigation, states, density. Made *before* markup,
   using the rules below. These are framework-agnostic: they hold for plain HTML, SvelteKit, React,
   or any other stack.
2. **Theme** — colors, type, spacing values, component styles. Never hand-rolled: install one of the
   bundled token-driven templates (see *Theme layer* below) and build against its contract.

Most bad UI is not a bad theme — it is unexamined defaults: everything centered, everything boxed,
uniform spacing, no visual priority. The design pass exists to force those decisions explicitly.

Worked good/bad markup for the rule sections below lives in `references/examples.md` — consult it
when building, alongside the chosen theme's `brand-guide.html`.

## The design pass

Before writing any markup, answer these five questions and state the answers (one line each) so the
choices are reviewable:

1. **What kind of surface is this?** Data-dense tool, content/marketing page, focused single-task
   flow, or metric overview. This classification drives every later choice.
2. **Which layout archetype fits?** (table below)
3. **What is the one primary action per view?** Everything else is visually subordinate.
4. **Which theme template?** (Theme layer below)
5. **What do empty, loading, and error look like?** Designed now, not retrofitted.

Then build, then run the *Review pass* at the end.

## Layout

### Pick one archetype per surface

| Archetype | Use for | Structure |
|-----------|---------|-----------|
| **App shell** | Data-dense tools, ≥5 nav destinations, daily-use apps | Fixed sidebar (nav) + scrollable content pane; topbar only for global search/account |
| **Top-nav** | Content and marketing sites, ≤5 destinations | Horizontal nav bar + full-width sections below |
| **Focused flow** | Auth, checkout, onboarding, wizards, single forms | Single centered column, minimal or no nav, one action per step |
| **Dashboard grid** | Metric overviews, monitoring | App shell + card grid; cards sized by importance, not uniformly |

Do not mix archetypes on one surface. An app does not get a marketing hero; a login page does not
get a sidebar.

### Content width

- Prose: 65–75 characters per line (`max-width: 65ch`). Never let body text span a wide viewport.
- Forms: 480–640px column, labels above inputs. Full-width forms read as broken.
- Data tables: may use the full content pane — density is the point.
- Page content in an app shell: cap around 1200–1400px and left-align within the pane; do not
  stretch to fill a 4K monitor.

### Alignment and spacing rhythm

- Pick one alignment axis and keep it: **left-align** text-heavy and app UIs. Center only focused
  flows and marketing heroes. Centered body text is the single most common generic-AI tell.
- Proximity encodes relationship: space **within** a group must be visibly smaller than space
  **between** groups. Section gaps run 2–4× element gaps. If all gaps are equal, the page has no
  structure regardless of how many boxes it has.
- Use only the theme's spacing tokens (4px grid). No off-scale values.
- One gutter width per page. Elements that are conceptually aligned must be pixel-aligned.

### Responsive behavior

Decide the mobile form of the archetype up front: sidebar collapses to a drawer or bottom tab bar
(pick one, not both); top-nav collapses to a menu button; dashboard grids stack to one column in
card-importance order; tables either scroll horizontally in their own container or reflow to
key-value cards — never squash columns.

## Hierarchy

- **One primary action per view.** Exactly one filled/primary button; everything else outline,
  ghost, or link. Two primary buttons means no decision was made.
- **Three visible levels max.** Encode importance with size + weight + color *together*
  (large/bold/ink → medium/medium/ink → small/regular/muted). More levels than three and the eye
  ranks nothing.
- **Max ~4 type sizes per view** from the theme scale. Needing a fifth means the hierarchy is
  wrong, not the scale.
- **Boxes are not structure.** Use whitespace and alignment first, a border rule second, a card
  last. A card groups a set of *peer* items that need separation from other sets — it is not a
  default wrapper. **Never nest cards in cards.** If everything is in a box, nothing is grouped.

### When a page title appears — and when it doesn't

- Show a title (`h1`) when the page has an identity beyond its nav label: an entity name
  ("Invoice #1042"), a scope ("Settings — Billing"), or content the user navigated into.
- Skip the standalone title when it would only repeat the active nav item with zero added
  information — in an app shell, the highlighted nav item already says "Dashboard"; a lone
  "Dashboard" `h1` under it is noise. Either add value (count, date range, status) or drop it and
  promote the content.
- Focused flows title the *task*, not the app: "Create your account", not "Signup Page".
- Standard header anatomy when a title exists: optional eyebrow (uppercase micro-label for
  category/context) → title → one-line description → header-level actions right-aligned on the same
  row. One `h1` per page, always.

## Navigation

- **Placement follows the archetype:** sidebar for app shells (vertical scan, scales past 5 items),
  top bar for content sites, **tabs** only for peer views of the *same* object or section (they
  switch content in place, never navigate away), **breadcrumbs** only when hierarchy is ≥3 levels
  deep.
- **Order by frequency of use**, never alphabetically. The most-used destination sits first/top;
  Settings, account, and sign-out go last (sidebar bottom or top-bar far right).
- **Max 7 top-level items.** Beyond that, group under labeled sections (sidebar) or consolidate.
- **The active location must be visibly marked** — a filled/edged state on the current nav item
  (the theme's `.has-edge.is-active` exists for exactly this). A user should know where they are
  from the nav alone.
- Icons in nav are optional; if used, every item gets one (no partial icon rows) and each icon is
  paired with its text label. Icon-only nav requires an established, unambiguous icon set.

## Color and depth

- **Neutral-dominant:** roughly 90% of any view is surface + ink + border tokens. Brand color is
  reserved for the primary action, active/selected states, and focus — that scarcity is what makes
  it read as "the important thing".
- **Semantic colors carry meaning only.** Success/warning/danger appear when something *is*
  successful, at risk, or destructive — never as decoration or variety.
- **One depth language.** The templates each pick it (Meridian: soft shadows; Tidewater: borders).
  Do not add both a border and a shadow and a background tint to the same element.
- Data-viz uses the `--data-*` ramp in order; do not invent chart colors.

## States: design the unhappy paths first

Every list, table, and detail view ships with all four states designed:

- **Empty:** not a blank pane — one line of what belongs here plus the primary action to create it.
  First-run empty states are the highest-leverage screen in an app; give them the header anatomy
  (title, one-liner, action).
- **Loading:** skeleton blocks that mirror the real layout for anything structural; a spinner only
  for sub-second, in-place waits (button click). Never a full-page spinner for a partial update.
- **Error:** what happened + what the user can do (retry, go back), in place, using the danger
  token. Never a raw error string as the whole view.
- **Overflow:** long names truncate with ellipsis + title/tooltip; tables cap visible rows and
  paginate; numbers use tabular figures (`.numeric`) so columns align.

## Density

Match density to usage frequency: tools someone uses all day run dense (32–36px table rows,
`--fs-50/-100` in tables, compact `--space-2/-3` padding); occasional consumer flows run airy
(generous `--space-8+` sections, larger type). Choose once per surface and apply consistently —
mixed density inside one view reads as broken.

## Anti-patterns — the generic-AI tells

Reject these on sight, in your own output and in review:

- Everything centered — body text, forms, and headers all on the center axis.
- Every section boxed: border + shadow + background tint on the same element, cards inside cards.
- Uniform spacing everywhere — no proximity grouping, section gaps equal to element gaps.
- Gradient hero / glassmorphism on an app surface, or on every page of a content site.
- Emoji as icons or bullet decoration in product UI.
- Two or more filled primary buttons in one view.
- A lone `h1` that repeats the active nav label verbatim.
- Brand color as background wash for entire sections "to add visual interest".
- Five type sizes or three font families in one view.
- Happy path only — empty/loading/error left as afterthoughts.

## Review pass

Before calling the UI done, verify:

1. **Squint test:** blur your mental view — does the primary action and the page's structure still
   read? If it's a uniform gray blur, hierarchy failed.
2. **Alignment audit:** every element sits on the grid; one gutter; no accidental center/left mix.
3. **Spacing audit:** within-group < between-group everywhere; only token values.
4. **One primary action** per view; active nav state visible; title rule applied.
5. **State coverage:** empty, loading, error, overflow all handled.
6. **Token compliance:** no hardcoded hex, px sizes, or shadows — `var(--token)` everywhere.

---

# Theme layer

Colors, type, spacing values, and component styles come from a bundled template. Do not hand-roll
them — every value is a CSS custom property so the whole app re-themes from one file. Prefer this
bundled style over a generic component library (shadcn/ui, MUI, Mantine) for one coherent look.

## Choose and install

| Template | Feel | Type | Palette |
|----------|------|------|---------|
| **Meridian** | Restrained mainstream SaaS; soft elevation, calm neutrals | Inter · JetBrains Mono | Cool-gray, blue primary, amber accent |
| **Tidewater** | Editorial / boutique; flat, border-led depth | Fraunces · Hanken Grotesk · JetBrains Mono | Cool mint ground, terracotta + teal |

- **Choose:** let the user pick via `AskUserQuestion` (single-select) unless they already named one.
  Both templates ship the same token names and component classes, so the choice is purely
  look-and-feel — swap later by replacing one CSS file, with no markup changes. To preview, open
  `references/<name>/brand-guide.html` in a browser or send it with `SendUserFile`.
- **Install:** copy `references/<name>/brand.css` to the project's global stylesheet location
  (follow the project's existing convention) and load it **first**, before any app styles —
  `@import "./brand.css";` at the top of the entry CSS, or
  `<link rel="stylesheet" href="/brand.css">` for plain HTML. The file brings its own web fonts,
  reset, and bare-element styles, so unclassed markup already looks right.
- **Light/dark:** `data-theme="light"` or `"dark"` on `<html>` forces a theme; omit it to follow
  `prefers-color-scheme`.

## Build UI against the contract

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

To restyle the whole app later: replace the project's `brand.css` with the other template's — the
shared token + class contract means markup does not change.
