## Answer

- **bulk-read-guard.py** denies under these conditions:
  - Condition: File read is whole-file (no offset/limit) and file line count >= threshold — lines 102-104
  - Threshold constant: `FALLBACK_MIN_LINES` — line 16, value 350
  - Threshold source: `BULK_READER_MIN_LINES` environment variable (fallback 350 if not set or invalid) — lines 29-35
  - Exemption mechanism: paths matching `ALWAYS_ALLOW` patterns or patterns in `BULK_READER_ALLOW` env var — lines 38-51; matching is via `fnmatch` on full path or basename — lines 48-50
  - Environment variables: `BULK_READER_MIN_LINES` (line 29) controls enforcement on/off and sets threshold; `BULK_READER_ALLOW` (line 40) adds colon-separated exemption patterns — line 42
  - Guard is opt-in: returns 0 (allow) if `BULK_READER_MIN_LINES` not set — lines 79-80

- **bulk-read-bash-guard.py** denies under these conditions:
  - Conditions: Bash command contains `cat`, `less`, `more`, `bat`, or `batcat` (dump commands, line 32) or `head`/`tail` (window commands, line 33) and:
    - For dump commands: file line count >= threshold when not piped/redirected — line 173
    - For window commands: emitted lines >= threshold (calculated by `emitted_lines()` function resolving `-n +N`, `-n -N`, `-c` flags) — line 168
  - Threshold constant: `FALLBACK_MIN_LINES` — line 31, value 350
  - Threshold source: `BULK_READER_MIN_LINES` environment variable (fallback 350 if not set or invalid) — lines 52-58
  - Exemption mechanism: same as bulk-read-guard.py — lines 61-70; `ALWAYS_ALLOW` patterns (lines 42-47) mirrored from bulk-read-guard.py for consistency (see line 40-41 comment); `BULK_READER_ALLOW` env var colon-separated patterns — lines 63-65
  - Environment variables: `BULK_READER_MIN_LINES` (line 52) controls enforcement on/off and threshold; `BULK_READER_ALLOW` (line 63) adds exemptions
  - Pass-through conditions (never denied): piped commands (line 139), stdout redirected commands (lines 139, 38), stderr-only redirects (line 12 note)
  - Guard is opt-in: returns 0 (allow) if `BULK_READER_MIN_LINES` not set — lines 191-192

## Not found / uncertain

- Nothing outstanding.

## Coverage

- `/Users/Chen/WorkLocal/00_Project/agent-skills/plugins/ceh-coding-agent/scripts/bulk-read-guard.py` — 124 lines read
- `/Users/Chen/WorkLocal/00_Project/agent-skills/plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py` — 230 lines read
- Total: 354 lines across 2 files. No files skipped.
