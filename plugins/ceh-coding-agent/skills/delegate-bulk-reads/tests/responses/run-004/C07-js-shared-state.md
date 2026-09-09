## Answer
- `SS.state` object declared — tools/skills-sync/js/state.js:13-23
  - Fields: `projectHandle` (FileSystemDirectoryHandle) — tools/skills-sync/js/state.js:14
  - `manifest` (parsed manifest object or null) — tools/skills-sync/js/state.js:15
  - `manifestExisted` (bool) — tools/skills-sync/js/state.js:16
  - `sourceType` ("github" | "local", default "github") — tools/skills-sync/js/state.js:17
  - `sourceHandle` (FileSystemDirectoryHandle for local source) — tools/skills-sync/js/state.js:18
  - `sourceLabel` (string label for local source) — tools/skills-sync/js/state.js:19
  - `availableSkills` (Map<name, handle|githubEntries> or null) — tools/skills-sync/js/state.js:20
  - `githubTreeTruncated` (bool) — tools/skills-sync/js/state.js:21
  - `busy` (bool) — tools/skills-sync/js/state.js:22
- tools/skills-sync/js/main.js — writes to `state`: `state.projectHandle` (tools/skills-sync/js/main.js:30), `state.manifest` (tools/skills-sync/js/main.js:34, 249-251, 280, 322-331), `state.manifestExisted` (tools/skills-sync/js/main.js:35, 281), `state.sourceType` (tools/skills-sync/js/main.js:41, 48, 80), `state.availableSkills` (tools/skills-sync/js/main.js:61, 88, 126-129, 133, 180-183), `state.sourceHandle` (tools/skills-sync/js/main.js:168), `state.sourceLabel` (tools/skills-sync/js/main.js:169), `state.githubTreeTruncated` (read only at tools/skills-sync/js/main.js:117 — no write site found in this file; likely set inside `SS.detectGithubSkills`, not among the given files).
- tools/skills-sync/js/render.js — no match. `state` (aliased at tools/skills-sync/js/render.js:5) is only read (`state.manifest`, `state.availableSkills`, `state.projectHandle` at lines 8, 14, 17, 19, 21, 23, 34, 40, 46, 63, 70, 82, 94, 98-100, 132-133); no assignment to any `state.*` field appears in this file.
- `setBusy` (referenced tools/skills-sync/js/main.js:7, 28, 70, 114, 136, 151, 192, 222, 289, 309, 340, 349) presumably toggles `state.busy` but its definition is not in any of the three given files.

## Not found / uncertain
- `state.busy` — no assignment site visible in these three files; it is only read (tools/skills-sync/js/main.js:26, 99, 145, 201, 298) and toggled via the `setBusy` helper (tools/skills-sync/js/main.js:7), whose implementation lives outside state.js/main.js/render.js and was not provided.
- `state.githubTreeTruncated` — read at tools/skills-sync/js/main.js:117 but no write to it appears in these files; likely set inside `SS.detectGithubSkills`, whose source was not provided.

## Coverage
- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 352 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 545 lines across 3 files. Nothing skipped.
