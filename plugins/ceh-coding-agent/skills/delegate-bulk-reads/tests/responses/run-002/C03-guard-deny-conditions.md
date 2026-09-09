## Answer

- **bulk-read-guard.py** denies under these conditions — path:102-104
  - File has line count >= BULK_READER_MIN_LINES threshold AND is not in allowlist AND is a whole-file read (no offset or limit parameters) — path:96-104
  - BULK_READER_MIN_LINES threshold: constant FALLBACK_MIN_LINES = 350, read from environment variable `BULK_READER_MIN_LINES` with fallback — path:16, 27-35
  - Environment variable `BULK_READER_ALLOW`: colon-separated fnmatch patterns added to allowlist — path:40-42
  - Path exempted by: `is_allowed()` matches against ALWAYS_ALLOW patterns (hardcoded: *.lock, package-lock.json, pnpm-lock.yaml, *.svg, *.min.js, *.min.css, *.png, *.jpg, *.jpeg, *.gif, *.webp, *.ico, *.pdf, *.zip, *.tar, *.gz) plus patterns from BULK_READER_ALLOW, using fnmatch on both full path and basename — path:19-51

- **bulk-read-bash-guard.py** denies under these conditions — path:207-224
  - Bash command containing cat/less/more/bat/batcat or head/tail would emit >= BULK_READER_MIN_LINES lines of an unallowed file AND is not piped (|), stdin-redirected (<), or stdout-redirected (> or 1>) — path:139, 165-174
  - For dump commands (cat/less/more/bat/batcat): sum line counts across all specified files; for window commands (head/tail): check actual output lines from `emitted_lines()` which resolves -n, -c offsets and counts — path:99-135, 165-174
  - BULK_READER_MIN_LINES threshold: constant FALLBACK_MIN_LINES = 350, read from environment variable `BULK_READER_MIN_LINES` with fallback — path:31, 50-58
  - Environment variable `BULK_READER_ALLOW`: colon-separated fnmatch patterns added to allowlist — path:63-65
  - Path exempted by: `is_allowed()` matches against ALWAYS_ALLOW patterns (identical set as bulk-read-guard.py) plus patterns from BULK_READER_ALLOW, using fnmatch on both full path and basename — path:42-70

## Not found / uncertain

- Nothing outstanding.

## Coverage

- C:\Users\Chen\WorkLocal\00_Project\agent-skills\plugins\ceh-coding-agent\scripts\bulk-read-guard.py — 124 lines read
- C:\Users\Chen\WorkLocal\00_Project\agent-skills\plugins\ceh-coding-agent\scripts\bulk-read-bash-guard.py — 230 lines read
- Total: 354 lines across 2 files. No files skipped.
