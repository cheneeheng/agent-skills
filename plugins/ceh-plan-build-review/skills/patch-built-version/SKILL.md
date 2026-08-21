---
name: patch-built-version
disable-model-invocation: true
description: >-
  Patch an already-implemented version of a planned app — a small, non-feature change made after
  that version was built (bug fix, copy/config tweak, validation tightening, small behavioral
  adjustment, dependency bump, and small post-MVP polish items). Records the change as a patch
  ITER_NN.md (frontmatter patch: true) so the plan stays truthful, then implements only the touched
  sections. Routes anything that adds or changes a feature to plan-fullstack-app-iteratively
  instead.
argument-hint: '[what-to-patch]'
---

# Patch Built Version

Make a small change to a version that is already implemented, without inventing a new
iteration's worth of scope and without letting the plan artifacts drift from the code.

Read [references/plan-schema.md](references/plan-schema.md) for the full schema before
starting. File naming, version families, `depends_on` resolution, and the `patch` marker
rules there are authoritative.

A patch is a **change below the size of a feature**. It rides as a normal `ITER_NN.md` that
carries `patch: true` in its frontmatter and may sit past the MVP terminator — it is the only
artifact allowed to. The version bump and release are **not** this skill's job: hand those to
`ceh-git-workflow:release` (a patch is a SemVer PATCH bump).

## Step 1 — Locate the Plan Family and Its Latest Artifact

1. Find the plan files (see `implement-from-plan` Step 1 conventions: default location
   `.agents_workspace/planning/`, version-tagged names allowed). Group into families; if more
   than one family exists, confirm which version is being patched.
2. Identify the family's latest artifact — the `mvp: true` terminator if present, otherwise the
   highest `ITER_NN` reachable through `depends_on`. Any existing `patch: true` ITERs count:
   the latest one becomes the new patch's `depends_on` target.

## Step 2 — The Routing Gate (Patch or Iteration?)

Classify the requested change **before writing anything**. This gate is the point of the skill.

**It is a feature — STOP and route to `plan-fullstack-app-iteratively`** if the change:

- adds or changes a **data-model entity** or an **API route/endpoint** (i.e. touches §02
  Architecture — the data model or API surface), or
- adds a **new screen, page, or top-level component** (a §05 structural addition), or
- changes the **§01 Concept** — what the app does or its primary user flow, or
- is a **deferred item from the terminator's `## Out of MVP scope` block** that meets any of the
  above. Post-MVP *features* are the iterative planner's job, not a patch.

The reliable tell: **if §02 changes, it is an iteration, not a patch.** Do not force a feature
through this skill. Say so in one line and point the user at
`plan-fullstack-app-iteratively`.

**It is a patch — continue here** if the change stays within the existing architecture:

- bug fix, incorrect behavior corrected within an existing endpoint/screen,
- copy, labels, error messages, config values, defaults,
- validation tightening/loosening on an existing field,
- styling/layout tweak on an existing screen,
- dependency bump or small non-structural refactor,
- small post-MVP polish that adds no entity, route, screen, or concept change.

When genuinely on the line, prefer routing out — an over-scoped patch is worse than an
iteration planned properly.

## Step 3 — Write the Patch ITER

Create the next `ITER_NN.md` in the family (continue the family's `NN` counter — a patch does not
restart it) alongside the other plan files. Frontmatter:

```yaml
---
artifact: ITER_NN          # next number in the family
status: ready
created: YYYY-MM-DD
scope: <one line: the small change this patch makes>
patch: true                # marks this as a patch; may follow the mvp terminator
sections_changed: [NN]     # only the section(s) the change actually touches
sections_unchanged: [...]  # everything else — pointers, resolved via depends_on
depends_on: [<latest artifact stem>]   # the terminator, or the prior patch ITER
---
```

Rules specific to a patch ITER:

- **`patch: true`** distinguishes it from a feature iteration and authorizes it to sit past the
  terminator. Never set `mvp` on a patch.
- **`sections_changed` lists only what the change touches** — usually §04 and/or §05 detail, not
  §02. If you find yourself listing §02, re-run the gate (Step 2): it is probably an iteration.
- Everything else stays a pointer. Keep the diff to the plan as small as the diff to the code.
- Write the changed section's body as a focused delta describing exactly the change (what the
  behavior was, what it becomes), the same way an iteration describes its own delta.

## Step 4 — Implement the Patch

Implement only `sections_changed`, resolving pointers through `depends_on` for context. Because a
patch is small, implement it inline following the same discipline as `implement-from-plan`
(§04/§05 notes, `implementation-gotchas.md` check, stay within scope) — or, if the change is
large enough to warrant it, invoke `implement-from-plan` targeting the patch file by name. Do
not implement any section outside `sections_changed`.

## Step 5 — Completion Summary and Hand-off

Report:

- The patch ITER created and the section(s) it changed.
- What changed in the code and any assumptions.
- Items the user should verify manually.

Then hand off the release: state that this is a **SemVer PATCH** and point the user at
`ceh-git-workflow:release` (or `ceh-release-flow`) to bump, tag, and publish. This skill does
not bump versions or tag.
