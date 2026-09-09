## Answer

- **state.js** declares the shared mutable state object `SS.state` — state.js:13-23
  - **projectHandle** (FileSystemDirectoryHandle or null) — state.js:14
  - **manifest** (parsed manifest object or null) — state.js:15
  - **manifestExisted** (boolean) — state.js:16
  - **sourceType** (string: "github" | "local") — state.js:17
  - **sourceHandle** (FileSystemDirectoryHandle or null) — state.js:18
  - **sourceLabel** (string) — state.js:19
  - **availableSkills** (Map or null) — state.js:20
  - **githubTreeTruncated** (boolean) — state.js:21
  - **busy** (boolean) — state.js:22

- **main.js** writes to state fields:
  - projectHandle — main.js:30
  - manifest — main.js:34, 280, 331
  - manifestExisted — main.js:35, 281
  - sourceType — main.js:41, 48, 80
  - sourceHandle — main.js:168
  - sourceLabel — main.js:169
  - availableSkills — main.js:61, 88, 126, 128, 133, 180, 182

- **render.js** — no writes to state, only reads

## Not found / uncertain

- Nothing outstanding.

## Coverage

- C:\Users\Chen\WorkLocal\00_Project\agent-skills\tools\skills-sync\js\state.js — 51 lines read
- C:\Users\Chen\WorkLocal\00_Project\agent-skills\tools\skills-sync\js\main.js — 352 lines read
- C:\Users\Chen\WorkLocal\00_Project\agent-skills\tools\skills-sync\js\render.js — 142 lines read
- Total: 545 lines across 3 files. None skipped.
