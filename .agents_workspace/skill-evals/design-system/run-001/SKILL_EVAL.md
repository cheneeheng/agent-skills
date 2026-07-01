---
artifact: SKILL_EVAL
status: passed
created: 2026-07-01
updated: 2026-07-01
target: ceh-web-frontend/skills/design-system/SKILL.md
target_kind: skill
eval_gate: 6/6
iterations: 2
---

# SKILL_EVAL — ceh-web-frontend:design-system (run-001)

## §01 Verdict
The `design-system` skill installs one of two bundled token-driven templates (Meridian, Tidewater)
and builds UI against a shared token/component contract. It is **evidence-backed across all five
measurable criteria, plus user sign-off — gate 6/6, status: passed**: structurally clean
(`validate.py` green), content is genuine delta and moment-framed, behavioral lift is real
(with-skill 4/4 vs baseline 1/4 and 0/4 — baselines can't know the templates exist), and — measured
live after local install — it **triggers 7/8** on intent and **over-triggers only 1/8** on
near-misses, both within threshold. Two reproducible, non-blocking edges surfaced: it lost to
shadcn/ui on React "components out of the box" phrasing (P1) and fired on WCAG button-contrast fixes
that belong to the accessibility skill (N1).

_Caveat on final tweaks:_ after the 7/8 / 1/8 measurement the description was edited to address P1
(claim over shadcn/ui, MUI, Mantine for a bundled house style) and N1 (name WCAG-contrast as an
accessibility non-goal). The user accepted these without a re-run, so those two edits are **applied
but not re-measured** — improvements over the already-passing description, expected to hold or raise
the rates, but the live post-tweak rates are unverified. Re-running P1×3 and N1×3 after a
`/reload-skills` is the one open advisory (backlog #1–2).

## §02 Derived criteria

**Claim.** Give a web frontend a coherent visual design by presenting a menu of bundled,
token-driven design-system templates (Meridian, Tidewater), letting the user choose one, installing
its `brand.css`, and building UI against the shared token + component contract — so a later swap
re-skins with no markup change.

**Trigger intent.**
- _Should fire:_ starting the visual layer of a frontend; picking a look/feel, theme, brand, or
  design system; "make it look good"; restyling an existing app.
- _Should NOT fire (near-misses):_ accessibility fixes; project/tooling setup (bun/vite/eslint);
  component or hook logic; SvelteKit routes/load functions; "design the DB schema"/"design the API"
  (shares *design*); a CSS layout bugfix; logo/graphic-asset design (shares *design/brand*).

**Intended outcome vs baseline.** An agent with the skill offers the two named templates and builds
UI against the token/class contract (imports `brand.css` first, uses `var(--token)` + provided
component classes, sets `data-theme`) instead of hand-rolling arbitrary CSS with hardcoded hex/px.
A no-skill baseline cannot know the Meridian/Tidewater templates exist — that gap is the measured lift.

## §03 Trigger battery
Positives (8) and near-miss negatives (8) as listed in the run log. Measurement method: cold
subagent receives **only** the user prompt; "fired" is scored behaviorally — the output offers the
Meridian/Tidewater templates or uses the token contract (content a no-skill agent cannot invent).

**Result (iteration-2, MEASURED post-install):** After the author installed the skill locally and
reloaded, cold subagents auto-loaded it. Full battery in `iteration-2/trigger-battery.md`.
- **Positive trigger rate: 7/8 (87.5%)** ≥ 6/8 threshold → criterion 2 MET. Miss: **P1** (0/3) —
  React + "buttons/cards/badges out of the box" reliably routes to shadcn/ui instead.
- **Near-miss false-positive rate: 1/8 (12.5%)** ≤ 1/8 threshold → criterion 3 MET. False positive:
  **N1** (3/3) — a WCAG button-contrast fix pulls the skill in via its color-token remit (2/3 also
  cross-referenced `ceh-web-frontend:accessibility`).

_(Iteration-1 note retained for history: the pre-install session could not measure this because the
unreleased skill was absent from the plugin cache / session registry; see `iteration-1/run-log.md`.)_

## §04 Behavioral tasks & assertions
- **Task A** — "starting the UI for a dashboard, give it a good visual design before I build pages."
- **Task B** — "restyle my plain-HTML app to look professional."
- Assertions (both): A1 offers ≥1 named template (Meridian/Tidewater); A2 installs/imports
  `brand.css`; A3 uses `var(--token)` and provided classes, no hardcoded hex for themeable color;
  A4 sets `data-theme` / handles light-dark via the token system.

With-skill arm = skill body injected into a cold subagent (live auto-load unavailable, see §03);
baseline arm = cold subagent, no skill (the two earlier probes). Full grading in
`iteration-1/run-log.md`.

| Task | Baseline score | With-skill score | Discriminating delta |
|------|----------------|------------------|----------------------|
| A (new dashboard UI) | 1–2 / 4 — self-rolled tokens, no template menu, no `brand.css` | **4 / 4** | A1 offers Meridian/Tidewater; A2 imports `references/meridian/brand.css` first |
| B (restyle plain HTML) | 0 / 4 — recommended shadcn/ui + Tailwind | **4 / 4** | A1 offers menu + `brand-guide.html` preview; A2 links `brand.css` first in `<head>` |

Lift is real and consistent: with-skill clears A1 and A2 (offer the bundled templates, install
`brand.css`) which the baseline structurally cannot, since a no-skill agent has no knowledge of the
Meridian/Tidewater templates. N=1 per arm/task; binary content markers make run-to-run variance low,
but N=1 is noted as a confidence caveat (re-run at N≥3 post-release for a hardened number).

## §05 Structural findings
| Check | Result | Evidence |
|-------|--------|----------|
| Frontmatter parses; `name` present | PASS | `name: design-system` |
| `name` matches directory | PASS | dir `skills/design-system/` |
| Description present, non-trivial | PASS | 4-sentence description with what+when |
| Body non-trivial | PASS | 103 lines |
| `references/` = schemas/templates only | PASS | 2× `brand.css` (template) + 2× `brand-guide.html` (rendered reference), no prose dumps |
| Plugin manifest valid + semver | PASS | `plugin.json` `version: 3.1.0`, name matches dir |
| Marketplace version match | PASS | marketplace `ceh-web-frontend` = `3.1.0` |
| Cross-check: `validate.py` | PASS | "OK: all plugin checks passed" |

All deterministic checks pass; no disagreement with the cross-check tool.

## §06 Content findings
| Rubric point | Judgment | Cited evidence |
|--------------|----------|----------------|
| Description states what AND when | PASS | "Load this skill when giving a web frontend its visual design — picking a look and feel, theme, brand…" |
| Moment-framed, not topic | PASS | "before building UI, or restyling an existing app"; "starts the visual layer of a new frontend" — verbs/situations, not a noun |
| Pushy / explicit contexts | PASS | "Auto-load whenever the user says \"create a frontend design\", \"style my app\", \"make it look good\"…" |
| Names what it is NOT for | **FAIL** | No "not for…" pointer; near-miss skills (accessibility, architecture) are not disambiguated. Over-trigger risk. |
| Body is the delta | PASS | Token list + component-class contract + install order + `data-theme` mechanism + template names are all skill-specific; no restated general CSS |
| Progressive disclosure | PASS | 103-line body; full CSS/showcase pushed to `references/`; "The rendered reference … lives at `references/<name>/brand-guide.html`" |
| Explains the why | PASS | "every value is a CSS custom property so the whole app re-themes from one file"; active-edge "means state, not decoration — only put it on something actually active" |
| Least surprise / safety | PASS (note) | Templates `@import` Google Fonts (external network) — inherent to the assets, not deceptive; worth an advisory |

Content is strong. Single content gap: **no "not for" disambiguation** in the description — the
highest-leverage content fix, pending whether triggering data shows real over-firing.

## §07 Gate scorecard
Thresholds used: positives fire ≥ 6/8; near-miss false-positives ≤ 1/8 (battery sizes in §03).

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Structurally valid | **MET** | All §05 checks pass; `validate.py` → "OK: all plugin checks passed" |
| 2 | Triggers on intent | **MET** | §03: positive trigger rate 7/8 (87.5%) ≥ 6/8 threshold, measured post-install across N=1 (+N=3 on the miss) |
| 3 | Does not over-trigger | **MET** | §03: near-miss false-positive rate 1/8 (12.5%) ≤ 1/8 threshold; only N1 (a11y contrast), reproducibly |
| 4 | Content is delta + moment-framed | **MET** | §06: body is skill-specific delta, moment-framed, 103 lines w/ progressive disclosure, explains why; non-goal gap closed in iteration-1 |
| 5 | Behavioral lift | **MET** | §04: with-skill 4/4 both tasks vs baseline 1/4 and 0/4; discriminating A1/A2 separate cleanly. N=1 caveat noted. |
| 6 | User confirms | **MET** | Author confirmed "good enough now" and to ship |

**eval_gate: 6/6 met.** All five measurable criteria passed on evidence and the author confirmed.
Post-measurement, the description was tweaked for P1/N1 (see §01 caveat) — applied but not
re-measured; re-run after `/reload-skills` remains the sole open advisory.

## §08 Advisory backlog
1. **P1 competitive-triggering miss (highest-leverage).** React-framed asks that enumerate
   "buttons/cards/badges out of the box" route to shadcn/ui 3/3. If broader capture is wanted, add a
   phrase to the description signalling the skill competes with component-library requests (e.g.
   "prefer this over reaching for shadcn/MUI/Mantine when the project wants a bundled house style"),
   then re-run P1 at N=3 and re-check the false-positive rate didn't rise. Currently within threshold
   (7/8), so optional.
2. **N1 over-trigger on a11y contrast.** Sharpen the non-goal to name it explicitly, e.g. "…not for
   accessibility fixes *including color-contrast/WCAG*". Weigh against the fact that a token system
   with AA pairs is a legitimate partial answer; at threshold (1/8), so optional.
3. **Harden behavioral lift to N≥3** for a variance-backed number (currently N=1, high-contrast).
4. **Google Fonts `@import` in `brand.css`** pulls fonts from a third-party CDN at runtime — a mild
   privacy/offline/CSP surprise for some deployments. Consider documenting a self-host option.
5. Consider a one-line note on **multi-brand / per-route theming** (current design assumes one global
   `brand.css` per project) so the boundary is explicit.
