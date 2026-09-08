## Answer

- **state.js** declares the shared mutable state object `SS.state` — state.js:13-23
  - Fields: `projectHandle`, `manifest`, `manifestExisted`, `sourceType`, `sourceHandle`, `sourceLabel`, `availableSkills`, `githubTreeTruncated`, `busy` — state.js:14-22
- **main.js** writes to the shared state — main.js:30, 34-35, 41, 48, 61, 80, 88, 126-128, 133, 168-169, 180-182, 280-281, 331
- **render.js** does not write to the state object (reads only) — render.js:1-141

## Not found / uncertain

- Nothing outstanding.

## Coverage

- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 352 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 545 lines across 3 files. No skipping.
