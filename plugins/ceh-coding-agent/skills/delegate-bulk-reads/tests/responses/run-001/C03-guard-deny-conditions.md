## Answer

**bulk-read-guard.py**

- Threshold constant `FALLBACK_MIN_LINES` — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:16
  - Value: 350
  - Set from `BULK_READER_MIN_LINES` environment variable, with fallback when parsing fails — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:27-35
- Environment variable `BULK_READER_MIN_LINES` — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:29
  - When unset or empty, enforcement is off (guard passes through all reads) — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:30-31, 79-80
  - When set to a non-integer value, uses FALLBACK_MIN_LINES instead — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:34-35
- Environment variable `BULK_READER_ALLOW` — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:40
  - Colon-separated patterns appended to allowlist — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:40-42
- Denial conditions: Read tool (line 87) on a whole file (no offset/limit — line 96) that is not allowlisted (line 99) and has >= threshold readable lines (line 103-104) — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:77-119
- Path exemption: matched against hardcoded ALWAYS_ALLOW patterns (*.lock, package-lock.json, pnpm-lock.yaml, *.svg, *.min.js, *.min.css, image formats, *.pdf, *.zip, *.tar, *.gz) or `BULK_READER_ALLOW` patterns by full path or basename using fnmatch — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:19-24, 38-51

**bulk-read-bash-guard.py**

- Threshold constant `FALLBACK_MIN_LINES` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:31
  - Value: 350
  - Set from `BULK_READER_MIN_LINES` environment variable, with fallback when parsing fails — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:50-58
- Environment variable `BULK_READER_MIN_LINES` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:52
  - When unset or empty, enforcement is off — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:53-54, 191-192
  - When set to a non-integer value, uses FALLBACK_MIN_LINES instead — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:57-58
- Environment variable `BULK_READER_ALLOW` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:63
  - Colon-separated patterns appended to allowlist — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:63-65
- Denial conditions: Bash tool (line 199) with a dump command (cat/less/more/bat/batcat) or window command (head/tail) not piped, redirected from stdin, or redirected to stdout (line 139-140), where the file(s) exceed threshold lines (cumulative for dump commands, per-file after window for head/tail) — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:189-224
  - Head/tail with explicit small window passes through if emitted lines < threshold — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:165-170
  - Segment split by `&&`, `||`, `;` and each checked separately — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:34, 206
  - Unexpanded globs (e.g., `dir/*.py`) treated as single non-matching path and skipped — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:158-159
- Path exemption: matched against hardcoded ALWAYS_ALLOW patterns (same as bulk-read-guard.py) or `BULK_READER_ALLOW` patterns, full path or basename — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:42-47, 61-70

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/scripts/bulk-read-guard.py — 124 lines read
- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 354 lines across 2 files. All content read in full.
