## Answer

- **Module:** `tools/skills-sync/js/state.js` declares the shared mutable state object — state.js:13-23

- **Fields it holds:** — state.js:13-23
  - `projectHandle` — null, FileSystemDirectoryHandle (readwrite)
  - `manifest` — null, parsed manifest object or null
  - `manifestExisted` — boolean
  - `sourceType` — string ("github" | "local")
  - `sourceHandle` — null, FileSystemDirectoryHandle for local source
  - `sourceLabel` — string, label for local source (folder name)
  - `availableSkills` — null or Map<name, handle | githubEntries>
  - `githubTreeTruncated` — boolean
  - `busy` — boolean

- **Modules that write to it:**
  - `tools/skills-sync/js/main.js` writes to multiple fields: `projectHandle` (line 30), `manifest` (lines 34, 280, 331), `manifestExisted` (lines 35, 281), `sourceType` (lines 41, 48, 80), `availableSkills` (lines 61, 88, 126, 180, 182, 133), `sourceHandle` (line 168), `sourceLabel` (line 169)
  - `tools/skills-sync/js/render.js` does not write; it only reads from state

## Not found / uncertain

- Nothing outstanding.

## Coverage

- tools/skills-sync/js/state.js — 51 lines read
- tools/skills-sync/js/main.js — 352 lines read
- tools/skills-sync/js/render.js — 142 lines read
- Total: 545 lines across 3 files.
