# Plan Document Schema

Planning documents come in two artifact types: **SKELETON** and **ITER_NN**.

## Frontmatter

**SKELETON.md:**
```yaml
---
artifact: SKELETON
status: ready
created: YYYY-MM-DD
app: <one-line app name>
stack: <comma-separated key technologies>
sections: [01, 02, 03, 04, 05]   # sections present
---
```

**ITER_NN.md:**
```yaml
---
artifact: ITER_01          # NN increments per iteration
status: ready
created: YYYY-MM-DD
scope: <what this iteration adds or changes>
sections_changed: [02, 05] # sections with content in this file
sections_unchanged: [01, 03, 04]  # sections using pointers (look in SKELETON or prior ITER)
---
```

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

To find the authoritative spec for a given section:
1. Find the most recent ITER_NN.md whose `sections_changed` includes that section number.
2. If none, fall back to SKELETON.md.
