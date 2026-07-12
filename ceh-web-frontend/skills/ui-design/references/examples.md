# UI Design Examples

Worked good/bad markup for each rule section of the `ui-design` skill. All snippets use the
bundled theme contract (tokens + component classes) and plain HTML — they translate 1:1 to
Svelte or JSX.

## Layout — app shell archetype

Skeleton for a data-dense tool (≥5 destinations): fixed sidebar, scrollable content pane, content
capped and left-aligned.

```html
<div style="display: grid; grid-template-columns: 240px 1fr; min-height: 100vh;">
  <nav aria-label="Primary"><!-- sidebar nav, see Navigation example --></nav>
  <main style="padding: var(--space-8); max-width: 1320px;">
    <!-- page header + content -->
  </main>
</div>
```

Focused flow (auth, checkout) is the only archetype that centers:

```html
<main style="max-width: 480px; margin: 0 auto; padding: var(--space-16) var(--space-4);">
  <h1>Create your account</h1>   <!-- titles the task, not the app -->
  <form><!-- one action per step --></form>
</main>
```

## Layout — content width

**Bad** — form and prose stretched across the viewport:

```html
<main style="width: 100%;">
  <p>Body text spanning 1900px is unreadable…</p>
  <form><input class="input" style="width: 100%;"></form>
</main>
```

**Good** — each content type gets its reading width:

```html
<p style="max-width: 65ch;">Prose caps at 65–75 characters per line.</p>
<form style="max-width: 560px;"><!-- labels above inputs --></form>
<table class="table"><!-- tables alone may use the full pane --></table>
```

## Layout — spacing rhythm

**Bad** — uniform gaps, no grouping (label, field, and the next section all equidistant):

```html
<div style="display: flex; flex-direction: column; gap: var(--space-4);">
  <label>Name</label><input class="input">
  <label>Email</label><input class="input">
  <h2>Notifications</h2>
</div>
```

**Good** — within-group < between-group; the section break is 3× the field gap:

```html
<div style="display: flex; flex-direction: column; gap: var(--space-2);">
  <label>Name</label><input class="input">
</div>
<div style="display: flex; flex-direction: column; gap: var(--space-2); margin-top: var(--space-4);">
  <label>Email</label><input class="input">
</div>
<h2 style="margin-top: var(--space-12);">Notifications</h2>
```

## Hierarchy — page header anatomy

Full anatomy when the page has an identity beyond its nav label:

```html
<header style="display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: var(--space-8);">
  <div>
    <p class="eyebrow">Billing</p>
    <h1>Invoice #1042</h1>
    <p class="muted">Issued 3 Jul 2026 · due in 12 days</p>
  </div>
  <div style="display: flex; gap: var(--space-2);">
    <button class="btn btn-outline">Download PDF</button>
    <button class="btn btn-primary">Send invoice</button>  <!-- the one primary action -->
  </div>
</header>
```

**Bad** — title repeats the active nav item with nothing added:

```html
<nav>…<a class="has-edge is-active" href="/dashboard">Dashboard</a>…</nav>
<main><h1>Dashboard</h1>…</main>
```

**Good** — either add value or drop the title and promote the content:

```html
<main>
  <h1>Dashboard <span class="muted">· last 30 days</span></h1>
  <!-- or: no h1, first metric row starts immediately -->
</main>
```

## Hierarchy — boxes are not structure

**Bad** — card nesting and per-item boxes:

```html
<div class="card">
  <div class="card">
    <div class="card">Revenue: $12,400</div>
  </div>
</div>
```

**Good** — one card groups the peer set; whitespace and a rule separate items inside:

```html
<section class="card">
  <h2>Revenue</h2>
  <dl>
    <div><dt class="muted">This month</dt><dd class="numeric">$12,400</dd></div>
    <div style="border-top: 1px solid var(--border);"><dt class="muted">Last month</dt><dd class="numeric">$11,050</dd></div>
  </dl>
</section>
```

## Navigation — sidebar with grouping and active state

Ordered by frequency, grouped past 7 items, settings pinned to the bottom, current location marked:

```html
<nav aria-label="Primary" style="display: flex; flex-direction: column; height: 100%; padding: var(--space-4);">
  <a class="has-edge is-active" href="/inbox">Inbox</a>
  <a class="has-edge" href="/projects">Projects</a>
  <a class="has-edge" href="/reports">Reports</a>
  <p class="eyebrow" style="margin-top: var(--space-6);">Admin</p>
  <a class="has-edge" href="/members">Members</a>
  <a class="has-edge" href="/billing">Billing</a>
  <a class="has-edge" href="/settings" style="margin-top: auto;">Settings</a>
</nav>
```

Tabs switch peer views of the *same* object in place — they never navigate away:

```html
<div role="tablist">
  <button role="tab" aria-selected="true" class="has-edge is-active">Overview</button>
  <button role="tab" aria-selected="false" class="has-edge">Activity</button>
  <button role="tab" aria-selected="false" class="has-edge">Settings</button>
</div>
```

## Color and depth

**Bad** — brand color as decoration, two primaries, semantic color without meaning:

```html
<section style="background: var(--secondary-wash); border: 1px solid var(--border); box-shadow: var(--shadow-md);">
  <h2 class="text-success">Team members</h2>
  <button class="btn btn-primary">Invite</button>
  <button class="btn btn-primary">Export</button>
</section>
```

**Good** — neutral surface, one depth cue, brand only on the primary action, semantic color only on state:

```html
<section class="card">
  <h2>Team members</h2>
  <span class="badge"><span class="dot dot-success"></span> 12 active</span>
  <button class="btn btn-primary">Invite</button>
  <button class="btn btn-ghost">Export</button>
</section>
```

## States

Empty — one line of what belongs here plus the action that creates it:

```html
<div class="card" style="text-align: center; padding: var(--space-12);">
  <h2>No projects yet</h2>
  <p class="muted">Projects group your team's work in one place.</p>
  <button class="btn btn-primary">Create project</button>
</div>
```

Loading — skeleton mirrors the real layout (spinner only for sub-second, in-place waits):

```html
<div aria-busy="true">
  <div style="height: var(--space-6); width: 40%; background: var(--surface-2); border-radius: var(--radius-sm);"></div>
  <div style="height: var(--space-4); width: 100%; background: var(--surface-2); border-radius: var(--radius-sm); margin-top: var(--space-3);"></div>
</div>
```

Error — what happened plus what to do, in place:

```html
<div class="card" role="alert">
  <p class="text-danger">Couldn't load projects.</p>
  <p class="muted">Check your connection, then try again.</p>
  <button class="btn btn-outline">Retry</button>
</div>
```

Overflow — truncation with the full value recoverable; numbers tabular:

```html
<td style="max-width: 24ch; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
    title="Quarterly infrastructure cost reconciliation">Quarterly infrastructure cost…</td>
<td class="numeric">1,204.50</td>
```

## Density

Dense table for a daily-use tool — compact rows, small type, tabular numbers:

```html
<table class="table" style="font-size: var(--fs-50);">
  <tr style="height: 34px;">
    <td>ord_8231</td>
    <td><span class="dot dot-live"></span> Processing</td>
    <td class="numeric">240.00</td>
  </tr>
</table>
```

The same data on an occasional consumer surface would instead run airy: card per order,
`--fs-200` type, `--space-8` section gaps.
