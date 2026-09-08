## Answer

- **state.js** declares the shared mutable state object `SS.state` — tools/skills-sync/js/state.js:13-23
  - Fields: `projectHandle`, `manifest`, `manifestExisted`, `sourceType`, `sourceHandle`, `sourceLabel`, `availableSkills`, `githubTreeTruncated`, `busy` — tools/skills-sync/js/state.js:14-23

- **main.js** writes to the state object — tools/skills-sync/js/main.js
  - Writes to: `projectHandle` (line 30), `manifestExisted` (line 35), `sourceType` (lines 41, 48, 80), `availableSkills` (lines 61, 88, 126, 128, 133, 180, 182), `sourceHandle` (line 168), `sourceLabel` (line 169), `manifest` (lines 280, 331)

- **render.js** — no writes. Only reads from state object for rendering purposes (lines 8, 14, 21, 34, 40, 46, 47, 98-100, 133).

## Not found / uncertain

- Nothing outstanding.

## Coverage

- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 351 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 544 lines across 3 files.
