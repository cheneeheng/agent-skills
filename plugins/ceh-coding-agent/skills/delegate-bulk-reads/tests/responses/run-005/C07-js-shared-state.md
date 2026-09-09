## Answer
- `SS.state` declared as the shared mutable state object — tools/skills-sync/js/state.js:13-23
  - Fields: `projectHandle` (FileSystemDirectoryHandle) — tools/skills-sync/js/state.js:14
  - `manifest` (parsed manifest object or null) — tools/skills-sync/js/state.js:15
  - `manifestExisted` (bool) — tools/skills-sync/js/state.js:16
  - `sourceType` ("github" | "local", defaults "github") — tools/skills-sync/js/state.js:17
  - `sourceHandle` (FileSystemDirectoryHandle for local source) — tools/skills-sync/js/state.js:18
  - `sourceLabel` (string) — tools/skills-sync/js/state.js:19
  - `availableSkills` (Map<name, handle|githubEntries> or null) — tools/skills-sync/js/state.js:20
  - `githubTreeTruncated` (bool) — tools/skills-sync/js/state.js:21
  - `busy` (bool) — tools/skills-sync/js/state.js:22
- `main.js` writes to `state` — tools/skills-sync/js/main.js:30 (`projectHandle`), :34 & :280 & :331 (`manifest`), :35 & :281 (`manifestExisted`), :41/:48 (`sourceType` from manifest source), :80 (`sourceType` from radio), :61/:88/:126/:133/:180 (`availableSkills`), :168 (`sourceHandle`), :169 (`sourceLabel`)
  - `state.busy` is only read (e.g. tools/skills-sync/js/main.js:26,99,145,201,298), never assigned directly in this file — the write comes from `SS.setBusy`, a function imported (`const setBusy = SS.setBusy;` — tools/skills-sync/js/main.js:7) but not defined in any of the three given files.
- `render.js` does not write to `state` — it only reads `state.manifest` and `state.availableSkills` (e.g. tools/skills-sync/js/render.js:8,14,17,19,21,34,40,46,47,98,99,100,133); no assignment to any `state.*` field appears in this file.

## Not found / uncertain
- Definition of `SS.setBusy`, which is the actual writer of `state.busy` — referenced at tools/skills-sync/js/main.js:7 but not defined in any of the three files given; the file that defines it (likely `dom.js` or similar) was not provided.
- Definition of `SS.detectGithubSkills`, which presumably sets `state.githubTreeTruncated` (read at tools/skills-sync/js/main.js:117) — not defined in the given files, so I cannot confirm where that field is written.

## Coverage
- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 352 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 545 lines across 3 files. Nothing skipped.
