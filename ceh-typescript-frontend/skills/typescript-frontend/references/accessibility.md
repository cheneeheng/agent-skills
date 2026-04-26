# Accessibility

- All interactive elements must be keyboard-accessible
- Images must have `alt` attributes (empty `alt=""` for decorative images)
- Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<section>`, `<header>`) — not `<div>` for everything
- `svelte-check` runs a11y checks — fix all warnings before opening a PR

## Keyboard Navigation

- Every action reachable by mouse must be reachable by keyboard
- Visible focus indicator must never be removed (`outline: none` without a replacement is forbidden)
- Tab order must follow the visual reading order
- Modal dialogs must trap focus while open and return focus to the trigger on close

## ARIA

Use native HTML semantics first. Add ARIA only when no native element fits:

```svelte
<!-- Prefer native button — gets role, keyboard, and focus for free -->
<button on:click={handleAction}>Submit</button>

<!-- Use aria-label when text content alone is ambiguous -->
<button aria-label="Close dialog" on:click={close}>✕</button>

<!-- aria-live for dynamic status updates (loading, errors) -->
<p aria-live="polite" aria-atomic="true">{statusMessage}</p>

<!-- aria-expanded for disclosure widgets -->
<button aria-expanded={open} on:click={toggle}>Details</button>
```

Do not add `role="button"` to a `<div>` — use `<button>`. Never use `aria-hidden="true"` on
a focusable element.

## Forms

```svelte
<!-- Always associate labels with inputs -->
<label for="topic">Topic</label>
<input id="topic" type="text" bind:value={topic} />

<!-- Use aria-describedby for inline validation messages -->
<input id="email" aria-describedby="email-error" aria-invalid={!!emailError} />
<span id="email-error" role="alert">{emailError}</span>
```

## Color and Contrast

- Text contrast ratio: 4.5:1 minimum (3:1 for large text ≥ 18px or bold ≥ 14px)
- Do not rely on color alone to convey information — pair with an icon or text label
