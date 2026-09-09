## Answer
- `SS.state` shared mutable state object is declared in `tools/skills-sync/js/state.js:13-23`.
- Fields held by `SS.state`:
  - `projectHandle` (FileSystemDirectoryHandle, readwrite) — tools/skills-sync/js/state.js:14
  - `manifest` (parsed manifest object or null) — tools/skills-sync/js/state.js:15
  - `manifestExisted` (bool) — tools/skills-sync/js/state.js:16
  - `sourceType` ("github" | "local", default "github") — tools/skills-sync/js/state.js:17
  - `sourceHandle` (FileSystemDirectoryHandle for local source) — tools/skills-sync/js/state.js:18
  - `sourceLabel` (string label for local source) — tools/skills-sync/js/state.js:19
  - `availableSkills` (Map<name, handle|githubEntries> or null) — tools/skills-sync/js/state.js:20
  - `githubTreeTruncated` (bool) — tools/skills-sync/js/state.js:21
  - `busy` (bool) — tools/skills-sync/js/state.js:22
- `tools/skills-sync/js/main.js` writes to `SS.state` (via local alias `const state = SS.state;` at main.js:5):
  - `state.projectHandle` — main.js:30
  - `state.manifest` — main.js:34, main.js:280, main.js:331
  - `state.manifestExisted` — main.js:35, main.js:281
  - `state.sourceType` — main.js:41, main.js:48, main.js:80
  - `state.availableSkills` — main.js:61, main.js:88, main.js:126, main.js:133, main.js:180
  - `state.sourceHandle` — main.js:168
  - `state.sourceLabel` — main.js:169
- `tools/skills-sync/js/render.js` — no match for writes to `state`. It only aliases `const state = SS.state;` (render.js:5) and reads fields (`state.manifest`, `state.availableSkills`, `state.projectHandle`) at render.js:8-46, render.js:94, render.js:98-100; every reference is a read/comparison, none is an assignment to a `state.*` property.

## Not found / uncertain
- `state.busy` — no assignment to this field appears in any of the three given files; it is only read (e.g. main.js:26, main.js:99). It is set via `SS.setBusy` (aliased at main.js:7), whose definition lives outside the three given files.
- `state.githubTreeTruncated` — only read (main.js:117); no assignment appears in the given files, so the writer module could not be determined from these files alone.

## Coverage
- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 352 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 545 lines across 3 files. Nothing skipped.
