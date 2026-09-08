## Answer

**bulk-read-guard.py** — denies when:
- `BULK_READER_MIN_LINES` env var is set (line 78-80) — line 29: threshold resolved from env var, line 16: fallback value is `350`
- The tool is "Read" (line 87-88)
- A `file_path` is provided (line 91-93)
- The read has no `offset` or `limit` (line 96-97 — targeted reads always pass)
- The file is not in the allowlist (line 99-100)
- The file's line count is >= threshold (line 102-104)

Path exemption: fnmatch patterns in `ALWAYS_ALLOW` (line 19-24) — e.g., `*.lock`, `*.min.js`, `*.svg`, `*.pdf` — plus colon-separated patterns from `BULK_READER_ALLOW` env var (line 40-42, applied in line 48-50 via `is_allowed()`).

**bulk-read-bash-guard.py** — denies when:
- `BULK_READER_MIN_LINES` env var is set (line 190-192) — line 52: threshold resolved from env var, line 31: fallback value is `350`
- The tool is "Bash" (line 199-200)
- A `command` is provided (line 202-204)
- Any segment (split by `&&`, `||`, `;`) contains (line 206-224):
  - A dump command (`cat`, `less`, `more`, `bat`, `batcat`) or window command (`head`, `tail`) (line 149-151, line 32)
  - No pipe `|` (line 139)
  - No input redirect `<` (line 139)
  - No stdout redirect `>` or `1>` (line 139, line 38 — stderr redirects like `2>` do not exempt)
  - A file argument that is not allowed and not already narrowed (line 160-161)
  - For dump commands: total lines from all file arguments >= threshold (line 173)
  - For window commands: emitted lines (after applying `-n` or `-c` offset) >= threshold (line 167-169)

Path exemption: identical to bulk-read-guard.py — `ALWAYS_ALLOW` patterns (line 42-47) plus `BULK_READER_ALLOW` env var (line 63-65, applied in line 67-69 via `is_allowed()`).

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/scripts/bulk-read-guard.py — 124 lines read
- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 354 lines across 2 files. All content read.
