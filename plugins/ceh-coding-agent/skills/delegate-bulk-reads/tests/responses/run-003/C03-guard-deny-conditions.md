## Answer

### bulk-read-guard.py

**Denial conditions** — denies whole-file Reads when all are true: `BULK_READER_MIN_LINES` is set (enforcement on) — line 78-80; tool is Read — line 87-88; file_path exists — line 91-93; no offset or limit (not targeted) — line 96-97; path not allowlisted — line 99-100; file line count >= threshold — line 102-107.

- **Threshold constant** — `FALLBACK_MIN_LINES = 350` — line 16
- **Threshold source and fallback** — reads `BULK_READER_MIN_LINES` environment variable; if unset/empty, enforcement is off (allows all) — line 29-31; if set but invalid, uses 350 — line 33-35
- **Environment variables changing behavior** — `BULK_READER_MIN_LINES` (line 29) enables/sets threshold; `BULK_READER_ALLOW` (line 40) adds colon-separated fnmatch patterns to allowlist
- **Path exemptions** — `is_allowed()` function — line 46-51 — matches full path or basename against hardcoded ALWAYS_ALLOW patterns (line 19-24: lock files, images, archives, minified assets) plus patterns from `BULK_READER_ALLOW` environment variable (line 40-42)

### bulk-read-bash-guard.py

**Denial conditions** — denies Bash commands when all are true: `BULK_READER_MIN_LINES` is set (enforcement on) — line 190-192; tool is Bash — line 199-200; command contains a segment with a dump or window command (cat/less/more/bat/batcat/head/tail) — line 150; segment is not piped (no `|`), redirected from stdin (no `<`), or sent to stdout (no unescaped `>` or `1>`) — line 139; file(s) not allowlisted — line 160-161; and either: for head/tail, emitted lines >= threshold (line 168), or for cat/etc, total lines across all arguments >= threshold (line 173).

- **Threshold constant** — `FALLBACK_MIN_LINES = 350` — line 31
- **Threshold source and fallback** — reads `BULK_READER_MIN_LINES` environment variable; if unset/empty, enforcement is off (allows all) — line 52-54; if set but invalid, uses 350 — line 56-58
- **Environment variables changing behavior** — `BULK_READER_MIN_LINES` (line 52) enables/sets threshold; `BULK_READER_ALLOW` (line 63) adds colon-separated fnmatch patterns to allowlist
- **Path exemptions** — `is_allowed()` function — line 61-70 — matches full path or basename against hardcoded ALWAYS_ALLOW patterns (line 42-47: mirrors bulk-read-guard.py) plus patterns from `BULK_READER_ALLOW` environment variable (line 63-65); also passes through piped commands (segment contains `|` — line 139), stdin redirections (segment contains `<` — line 139), and stdout redirections matching unescaped `>` or `1>` regex (line 38, checked line 139)

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/scripts/bulk-read-guard.py — 124 lines read
- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 354 lines across 2 files. All content read.
