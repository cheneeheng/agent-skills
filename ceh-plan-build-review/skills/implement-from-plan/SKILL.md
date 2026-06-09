---
name: implement-from-plan
description: Load when the user has a SKELETON.md or ITER_NN.md planning document — including version-tagged variants like SKELETON_v2.md or v2_ITER_03.md — and wants to implement it. Reads plan frontmatter to determine artifact type and scope, then implements each in-scope section in order (§01–§06), resolving iteration pointers and depends_on chains to find authoritative specs. Trigger when the user says "implement from plan", "implement this spec", "implement SKELETON", "implement ITER", "implement the v2 plan", "implement v2 iter plans", "build the v3 skeleton", "build from the plan", "start implementing", or points to a SKELETON.md or ITER_NN.md (any version tag) and asks to build, implement, or execute it. Also trigger when the user opens a planning doc and says "let's go" or "let's build this".
---

# Implement From Plan

Translate a SKELETON.md or ITER_NN.md into working code, section by section, without
inventing scope beyond what is written.

Read [references/plan-schema.md](references/plan-schema.md) for the full schema before
starting. The section table, pointer rules, and resolution order there are authoritative.

## Step 1 — Locate and Parse Plan Docs

1. Find the target plan files. If the user didn't specify, look for `SKELETON` and `ITER_NN`
   files (`.md`) in the project root or a `docs/` directory. Filenames may carry a version tag
   as a prefix or suffix — e.g. `SKELETON_v2.md`, `v2_ITER_03.md`. See "File Naming and Version
   Variants" in [references/plan-schema.md](references/plan-schema.md) for the matching rules.
2. Group the discovered files by version tag into plan families (untagged files are the default
   family). If more than one family exists, confirm with the user which version is the target.
   Within a version, the iteration whose frontmatter has `mvp: true` is the sequence terminator —
   the plan runs SKELETON → ITER_01 → … → that terminator.
3. Read the YAML frontmatter to determine:
   - `artifact` — is this SKELETON or ITER?
   - For ITER: `sections_changed` (implement these), `sections_unchanged` (resolve via pointer),
     `depends_on` (the prior artifacts whose content this iteration relies on — its dependency chain)
   - For SKELETON: `sections` (implement all listed sections)
4. By default the target is the whole sequence up to and including the `mvp: true` iteration:
   implement the SKELETON, then each ITER_NN in `depends_on` order. Never implement past the mvp
   terminator. If the user named a single iteration, target only that one and use its `depends_on`
   chain to resolve unchanged sections for context.

## Step 2 — Resolve Pointers Before Starting

For any section in `sections_unchanged`, find its authoritative spec now (before writing any
code) by following the resolution order in `plan-schema.md`. Load that content into context
so you don't have to interrupt implementation to look it up.

## Step 3 — Implement Section by Section

Work through sections in numerical order. For each section:

1. State which section you're starting and what it covers (one line).
2. Read the section spec. Implement exactly what is specified — no more, no less.
3. When you finish a section, confirm it is done before moving to the next.

Section-specific notes:

**§01 Concept** — No code output. Load the concept as context. Confirm your understanding
in one sentence so the user can catch misreads early.

**§02 Architecture** — Create the project scaffold (directories, empty modules), stub data
model classes/types, and stub route handlers. Do not fill in logic yet unless the spec
includes it.

**§03 Tech Stack** — Install/configure the specified stack. Pin versions only if the spec
specifies them.

**§04 Backend** — Check whether an `implementation-gotchas.md` file exists in the project
(e.g. `docs/references/implementation-gotchas.md`). If it does, read it before implementing
any backend code. Implement the endpoints/services described for this section only.

**§05 Frontend** — Same as §04: check for `implementation-gotchas.md` first. Implement only
the screens and components listed in this section's spec.

**§06 LLM/Prompts** — Only present if the app has LLM integration. Implement the model
wiring, system prompt, and input/output handling as specified.

## Step 4 — Stay Within Scope

- Do not implement sections outside `sections_changed` (ITER) or `sections` (SKELETON).
- Do not add features, routes, components, or dependencies not in the spec.
- If ambiguous, state your assumption and use the simplest interpretation. Never guess silently.
- If a section spec is missing or incomplete, stop and ask rather than inventing.

## Step 5 — Completion Summary

After all sections are done, report:

- Sections implemented and key artifacts created
- Assumptions made
- Sections skipped and why (e.g. §06 absent because no LLM integration)
- Items the user should verify manually (e.g. env vars needing real values)
