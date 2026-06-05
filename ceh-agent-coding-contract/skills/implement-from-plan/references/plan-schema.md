# Plan Document Schema

Planning documents come in two artifact types: **SKELETON** and **ITER_NN**.

## File Naming and Version Variants

The base filenames are `SKELETON.md` and `ITER_NN.md`. A planning set may carry an optional
**version tag** — e.g. `v2`, `v3` — when more than one version of the app is planned in the same
location. The tag attaches as a prefix or suffix, bound by a `_`, `-`, or `.` separator:

- `SKELETON_v2.md`, `v2_SKELETON.md`, `SKELETON-v2.md`
- `ITER_03_v2.md`, `v2_ITER_03.md`, `ITER_03-v3.md`

Match plan files as the base name `SKELETON` or `ITER_NN` (`NN` = two digits) with an optional
separator-bound tag on either side, plus the `.md` extension. Untagged files (`SKELETON.md`,
`ITER_NN.md`) belong to the **default (untagged) family**.

Files that share a version tag form one **plan family**. The `NN` iteration counter restarts
within each family — `ITER_01_v2.md` is the first iteration of the `v2` family, independent of
`ITER_01.md`.

### Cross-version dependencies

Versions are linked, not isolated. A later version builds on an earlier one through the standard
`depends_on` frontmatter field (see Frontmatter) — a `v2` file lists the `v1` artifacts it builds
on and inherits every section it does not re-specify. Because `depends_on` names artifacts by
**stem** (filename without `.md`, which carries the version tag), one mechanism covers both
same-sequence iteration chaining (`[SKELETON, ITER_01]`) and cross-version inheritance
(`[SKELETON_v1, ITER_03_v1]`). A version's SKELETON is optional — a version may be ITER files
alone that depend on the previous version's SKELETON.

## Frontmatter

**SKELETON.md:**
```yaml
---
artifact: SKELETON
status: ready
created: YYYY-MM-DD
app: <one-line app name>
stack: <comma-separated key technologies>
sections: [01, 02, 03, 04, 05]   # sections present in this file
mvp_target: <one-line description of the MVP this sequence reaches>
---
```

The SKELETON body also carries a `## Out of MVP scope` block — a bulleted list of the features and
concerns consciously deferred from this MVP. Treat it as scope boundary, not as work to implement.

**ITER_NN.md:**
```yaml
---
artifact: ITER_01          # NN increments per iteration; stem = filename without .md
status: ready
created: YYYY-MM-DD
scope: <what this iteration adds or changes>
sections_changed: [02, 05] # sections with substantive content in this file
sections_unchanged: [01, 03, 04]  # sections using pointers (resolve via depends_on)
depends_on: [SKELETON]     # artifacts this iteration builds on; e.g. [SKELETON, ITER_01]
mvp: false                 # true exactly once, on the FINAL iteration (MVP terminator)
---
```

**Key field rules:**
- `depends_on` (ITER) — the prior artifacts this iteration relies on, named by stem. Must
  reference only SKELETON or earlier iterations — never a later one. Resolution traces this field;
  it is also what catches forward references.
- `mvp` (ITER) — `true` exactly once, on the final iteration. It marks where the plan stops;
  nothing is planned past it.
- `mvp_target` (SKELETON) — one line stating the MVP the iteration sequence terminates at.

## Sections

| ID | Title | Skeleton content | Iteration content |
|----|-------|-----------------|-------------------|
| §01 | Concept | What the app does, who it's for, the single most important user flow | What changed; pointer if unchanged |
| §02 | Architecture | Component diagram, data model (entity names + key fields), API surface (method + path + one-liner) | Changed entities/routes only; pointer otherwise |
| §03 | Tech Stack | Language/runtime versions, one framework per layer, database, key libraries | New deps + rationale, version pins if relevant; pointer otherwise |
| §04 | Backend | File/module tree (2–3 levels), one representative stub per route group, `how to run`, env var names | New modules/files, implementation detail for new endpoints; check `implementation-gotchas.md` |
| §05 | Frontend | Page/screen list with routes, top-level component tree, `how to run`, placeholder data strategy | New screens/components, state changes, new API calls; check `implementation-gotchas.md` |
| §06 | LLM/Prompts | *Skip if no LLM integration.* Model + provider, stub system prompt, input/output shape | Revised prompts, context strategy changes, eval approach |

## Pointers

When a section appears in `sections_unchanged`, the ITER file contains a pointer (e.g. "See SKELETON §02"). Do not treat this as content — look up the referenced document and section to get the actual spec.

## Resolution Order

Resolution follows the `depends_on` chain backward — never a forward reference.

To find the authoritative spec for a given section:
1. If a pointer names a specific artifact, honor it directly.
2. Walk the `depends_on` chain backward from the target. The authoritative spec lives in the
   nearest artifact (closest to the target) whose `sections_changed` (ITER) or `sections`
   (SKELETON) lists that section number.
3. For a version variant the chain crosses into the base version's artifacts. It never moves
   forward to a later iteration or version; the trace ends at a SKELETON.
