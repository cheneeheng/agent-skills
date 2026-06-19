---
name: review-against-plan
description: Load when the user wants to audit or verify that the current codebase matches a SKELETON.md or ITER_NN.md planning document — including version-tagged variants like SKELETON_v2.md or v2_ITER_03.md. For each in-scope section, checks the actual implementation against the spec, identifies gaps, deviations, and errors, then fixes them. Trigger when the user says "review against plan", "check implementation", "audit the spec", "verify the plan is implemented", "review the v2 plan", "audit v2 iter plans", "did I implement everything", "plan compliance check", or points to a plan file (any version tag) and asks to check, review, audit, or verify whether the implementation matches it.
---

# Review Against Plan

Audit the codebase against a SKELETON.md or ITER_NN.md — find gaps, deviations, and errors
between what the plan specifies and what is implemented, then fix them.

The planning document schema is defined in
[references/plan-schema.md](references/plan-schema.md).
Read it before starting. The section table and pointer resolution rules are authoritative.

## Step 1 — Locate and Parse Plan Docs

1. Find the target plan files. If the user didn't specify, look for `SKELETON` and `ITER_NN`
   files (`.md`) in the project root or a `docs/` directory. Filenames may carry a version tag
   as a prefix or suffix — e.g. `SKELETON_v2.md`, `v2_ITER_03.md`. See "File Naming and Version
   Variants" in [references/plan-schema.md](references/plan-schema.md)
   for the matching rules.
2. Group the discovered files by version tag into plan families (untagged files are the default
   family). If more than one family exists, confirm with the user which version to review; the
   iteration with `mvp: true` is that version's terminator. Read each target artifact's
   `depends_on` and resolve inherited (`sections_unchanged`) sections through that chain for
   context. Audit only each artifact's own `sections_changed`; treat inherited sections as
   context, not audit scope.
3. Read the frontmatter to determine scope:
   - ITER: audit only `sections_changed` (resolve pointers for `sections_unchanged` to use
     as context, but do not audit them — they were covered in a prior review cycle).
   - SKELETON: audit all sections listed in `sections`.
4. If multiple ITER files exist within the target family and the user didn't specify, confirm which one to review.

## Step 2 — Audit Section by Section

Work through in-scope sections in numerical order. For each section:

### Check
Compare the section spec against the actual codebase. Specifically verify:

| Section | What to check |
|---------|--------------|
| §02 Architecture | All specified components exist. Data model entities and key fields are present. All listed routes exist with correct method and path. No undocumented routes or entities. Diagram is Mermaid (not ASCII art) and reflects the current/changed architecture. |
| §04 Backend | All specified modules and files exist. Each route/service is implemented (not just stubbed unless spec says so). Env var names match. `how to run` works. |
| §05 Frontend | All specified pages/routes exist. Component tree matches. Placeholder data strategy followed. `how to run` works. |
| §06 LLM/Prompts | Model and provider match. System prompt implemented. Input/output shape matches. |

### Categorize Findings

For each finding, assign a category:

- **Gap** — something the spec requires that is completely missing
- **Deviation** — something that exists but differs from the spec (wrong method, wrong field name, wrong route path, wrong model, etc.)
- **Error** — something that is broken independent of the spec (import error, missing env var causing crash, etc.)

### Fix

Fix each finding immediately after categorizing it — do not batch auditing before fixing.

If a fix requires a decision (e.g. a route deviation where both the spec and the implementation
could be correct), state the ambiguity and ask before changing anything.

## Step 3 — Report

After all sections, produce a summary table:

```
## Plan Compliance Report

| Section | Findings | Status |
|---------|----------|--------|
| §02 Architecture | 2 gaps fixed (missing /users route, missing User.email field) | Fixed |
| §03 Tech Stack | Clean | OK |
| §04 Backend | 1 deviation fixed (POST /items returned 200, spec requires 201) | Fixed |
| §05 Frontend | 1 gap fixed (missing /profile page) | Fixed |
```

List items NOT fixed and why. Do not mark anything as fixed unless the fix was applied.
