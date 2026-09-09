## Answer

- **state.js** declares the shared mutable state object `SS.state` — state.js:13-23
  - Fields: `projectHandle` (FileSystemDirectoryHandle or null) — state.js:14
  - `manifest` (parsed object or null) — state.js:15
  - `manifestExisted` (boolean) — state.js:16
  - `sourceType` (string: "github" | "local") — state.js:17
  - `sourceHandle` (FileSystemDirectoryHandle or null) — state.js:18
  - `sourceLabel` (string) — state.js:19
  - `availableSkills` (Map or null) — state.js:20
  - `githubTreeTruncated` (boolean) — state.js:21
  - `busy` (boolean) — state.js:22

- **main.js** writes to the state object — main.js:1-351
  - Writes to: `projectHandle` (line 30), `manifest` (lines 34, 280, 331), `manifestExisted` (lines 35, 281), `sourceType` (lines 41, 48, 80), `sourceHandle` (line 168), `sourceLabel` (line 169), `availableSkills` (lines 61, 88, 126, 133, 180, 182)

- **render.js** — no writes to state object. Only reads state properties.

## Not found / uncertain
- Nothing outstanding.

## Coverage
- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 351 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 544 lines across 3 files.
