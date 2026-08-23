---
name: plan-fullstack-app-iteratively
description: >-
  Plan a software project one release at a time: each session produces a single artifact
  scoped to the next build, never the finished product. Handles vague or early-stage
  descriptions. Covers greenfield skeletons and iterative feature planning for existing
  apps. The incremental counterpart to plan-fullstack-app-to-mvp: choose THIS skill to
  plan one release at a time, and choose plan-fullstack-app-to-mvp when the entire build
  from skeleton to a finished MVP is wanted in a single session.
---

# Plan Fullstack App Iteratively

Produce a **minimal, scoped plan** for the current development intent — no more, no less.
The goal is to unblock the next build, not to specify the finished product.

Plans are iterative. Each planning session produces one artifact scoped to one release.

---

## Step 1 — Assess Intent

Before writing anything, determine:

1. **What is the app?** Capture the core concept in one sentence. If unclear, ask — but only one question at a time.
2. **Greenfield or continuing?** Is this a new project, or adding to / changing something that already exists?
3. **Which plan family?** Is this work part of the current plan set, or the start of a **new major version** (v2, v3, …)? See [Plan Families and Versions](#plan-families-and-versions). When in doubt, ask.
4. **What is the scope of this session?** Skeleton, a specific feature, a rework?

Use the answers to select the output mode:

| Situation | Output |
|-----------|--------|
| New project, nothing built yet | → [Skeleton Plan](#skeleton-plan), default (untagged) family |
| Existing project, same version, adding / changing something | → [Iteration Plan](#iteration-plan), current family |
| New major version that reshapes the scaffolding | → [Skeleton Plan](#skeleton-plan), new `vN` family |
| New major version that builds directly on the prior one | → [Iteration Plan](#iteration-plan), new `vN` family — first iteration `depends_on` the prior family |

Do not proceed to planning until intent is clear. Do not ask more than one clarifying question per exchange.

---

## Plan Families and Versions

A **plan family** is one skeleton/iteration sequence for the app, identified by an optional version tag.

- The first version of the app is the **default family**: untagged filenames `SKELETON.md`, `ITER_01.md`, `ITER_02.md`, …
- A **new major version** is a fresh family with a version tag (`v2`, `v3`, …). Each major version is a new start: the `NN` iteration counter **restarts at 01** within the family, and the version tag goes in the filename — `SKELETON_v2.md`, `ITER_01_v2.md`, … (canonical emit form: `_vN` suffix; the implementation step also accepts a `v2_` prefix on read).

Families are **linked, not isolated**, but how a new version inherits depends on whether
it has its own skeleton — and a skeleton is always a resolution *terminus* (the
implementation step never traces past one):

- **New version with its own skeleton** (`SKELETON_vN`, when the scaffold is reshaped):
  the skeleton is **self-contained** — it re-states every section the version needs,
  because a pointer can't resolve past it into the prior family. Its iterations
  `depends_on` `SKELETON_vN` and earlier `vN` iterations only. Lineage to the prior
  version is conceptual, not a resolution link.
- **New version without a skeleton** (iterations-only, when the prior scaffold is reused):
  `ITER_01_vN` `depends_on` the prior family's terminal artifacts — skeleton plus its
  final iteration, e.g. `depends_on: [SKELETON, ITER_03]` — and inheritance resolves
  *across* that link. This is the case where cross-version `depends_on` does real work.

In both cases `depends_on` names artifacts by **stem** (filename without `.md`, which
carries the version tag), and only ever points **backward** — earlier in this family or
into an earlier version, never forward. Within a family it is simply the same-sequence
chain, e.g. `[SKELETON_v2, ITER_01_v2]`. Skeletons themselves carry **no** `depends_on`.

---

## Step 2 — Anti-Overplan Check

Before writing any section, apply this filter:

> *Is this decision required to build what the developer described right now?*

If no → leave it out. Mark it as deferred in the relevant section with a one-line note.

Do not spec behaviour that hasn't been decided. Do not add features "while we're at it". Do not describe the finished app — describe the next release.

Overplanning is a blocking risk: a developer who reads ahead into unresolved detail will pause to resolve it before building. Keep the plan narrow.

---

## Skeleton Plan

**When:** New project, nothing built yet — **or** the start of a new major version that reshapes the scaffolding.

**Goal:** Produce just enough to build a working skeleton — screens render, routes respond, but functionality is stubbed. The developer should be able to run the app and get a first impression of whether the concept is right.

**Output:** A single file `.agents_workspace/planning/SKELETON.md` for the default family, or `.agents_workspace/planning/SKELETON_vN.md` for a version family (e.g. `SKELETON_v2.md`). Skeletons carry no `depends_on` (see [Plan Families and Versions](#plan-families-and-versions)).

### Sections in SKELETON.md

Include all applicable sections inline. Keep each section brief — stubs and shapes, not full implementation detail. Skip sections that do not apply (e.g. no backend → skip §04; no LLM → skip §06).

```
§01 · Concept
§02 · Architecture
§03 · Tech Stack
§04 · Backend
§05 · Frontend
§06 · LLM / Prompts
```

See `references/section-specs.md` for the expected contents of each section at skeleton level.

### Skeleton Rules

- Every route/endpoint exists but may return hardcoded or empty data.
- Every screen exists but may render with placeholder content.
- No auth, no error handling, no edge cases — unless the concept cannot be understood without them.
- Dependencies listed but not fully justified — rationale comes in iteration plans.
- No deployment, no CI/CD, no production config.

---

## Iteration Plan

**When:** Adding to or changing an existing project, within an existing or new version family.

**Output:** A single file `.agents_workspace/planning/ITER_NN.md` (default family) or `.agents_workspace/planning/ITER_NN_vN.md` (version family), where `NN` is the next available two-digit number **within that family** (the counter restarts per family — `ITER_01_v2.md` is the first iteration of the `v2` family, independent of `ITER_01.md`).

### Sections in ITER_NN.md

Use the same section numbers as the skeleton. For each section:

- **If the section is affected by this iteration:** write the full scoped content for what changes.
- **If the section is untouched:** include a one-line pointer only.

**Pointer format** — reference the artifact by stem (the filename without `.md`, including any version tag):
```markdown
## §03 · Tech Stack
> Unchanged — see SKELETON_v2 § 03
```
or
```markdown
## §04 · Backend
> Unchanged — see ITER_02_v2 § 04
```

Always point to the last artifact where that section was substantively written, not to the skeleton by default. A pointer may cross a version boundary — e.g. a `v2` iteration whose §03 was last written in the `v1` skeleton points to `SKELETON § 03`.

**`depends_on` frontmatter** — every iteration lists the artifacts it builds on, by stem, so the implementation step can resolve pointers by walking the chain backward:

- Within a family, this is the same-sequence chain up to here, e.g. `depends_on: [SKELETON_v2, ITER_01_v2]`.
- The **first iteration of a new version** depends on `SKELETON_vN` if this version has its own skeleton; if it's an iterations-only version reusing the prior scaffold, it points back into the prior family's terminal artifacts instead, e.g. `depends_on: [SKELETON, ITER_03]`. See [Plan Families and Versions](#plan-families-and-versions).
- Every artifact named in a pointer must appear in (or be reachable through) `depends_on`. `depends_on` only points backward — never to a later iteration or version.

### Iteration Rules

- Scope strictly to what this iteration adds or changes.
- Do not restate unchanged decisions — use pointers.
- `depends_on` must list every artifact a pointer relies on, and must point only backward.
- Do not plan the iteration after this one.
- Deferred decisions stay deferred until they become relevant.

---

## Step 3 — Delivery

1. Run the **Anti-Overplan Check** over the draft before delivering — remove anything that isn't required for the current release.
2. Save the file to `.agents_workspace/planning/`.
3. Present the file to the user.
4. Close with a brief summary:
   - What this plan covers
   - What is explicitly deferred
   - Suggested scope for the next iteration (one sentence only — do not plan it)

Do not produce multiple files unless the user asks. Do not produce a `CLAUDE.md` unless the user asks.

---

## Reference Files

Read when needed — do not load upfront:

- `references/section-specs.md` — Expected contents for each section (§01–§06) at skeleton and iteration level
- `references/audit-checklist.md` — Pre-delivery checks
- `references/implementation-gotchas.md` — Common technical traps (read when writing §04, §05, §06)
