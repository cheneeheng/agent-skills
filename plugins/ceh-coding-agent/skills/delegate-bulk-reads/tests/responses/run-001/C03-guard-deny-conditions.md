## Answer

**bulk-read-guard.py**

- Denial condition — path:77-119: Denies a whole-file Read of the Read tool when threshold is set AND path is not allowlisted AND file has countable lines >= threshold AND read has no offset/limit parameter.
  - Threshold constant: `FALLBACK_MIN_LINES` — 350 — path:16
  - Controlled by: `BULK_READER_MIN_LINES` environment variable — path:29. If set but invalid, falls back to 350. If not set or empty, enforcement is off (threshold is None) — path:29-35.
  - Exemption: Path matches any pattern in `ALWAYS_ALLOW` built-in set OR in `BULK_READER_ALLOW` env var (colon-separated) — path:19-24, 40-42. Matching uses full path or basename — path:48-50.
  - Passes through: Targeted reads with offset or limit parameter — path:96-97.

**bulk-read-bash-guard.py**

- Denial condition — path:189-224: Denies a Bash tool invocation when threshold is set AND a command segment (split by && || ;) contains a dump command (cat/less/more/bat/batcat) or window command (head/tail) AND that segment is not piped (no |) AND is not stdin-redirected (no <) AND is not stdout-redirected (no > or 1>) AND a file argument is not allowlisted AND has countable lines AND would emit >= threshold lines in context.
  - For dump commands (cat etc.): total lines of all file arguments summed — path:172.
  - For window commands (head/tail): lines actually printed by that command, accounting for -n/-c flags with offset/count resolution — path:167-169.
  - Threshold constant: `FALLBACK_MIN_LINES` — 350 — path:31. Controlled by same `BULK_READER_MIN_LINES` env var with same fallback logic — path:52-58.
  - Exemption: Same as bulk-read-guard.py — path:42-47, 63-65. Full path or basename matching — path:67-69.
  - Passes through: Piped commands (| in segment), stdin redirects (< in segment), stdout redirects (> or 1> in segment) — path:139-140.
  - Window calculation (head/tail): Resolves `-n +N` / `-n -N` as offsets (not counts), `-c` as bytes (not lines), default 10 lines with no explicit window — path:86-135.

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/scripts/bulk-read-guard.py — 124 lines read
- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 354 lines across 2 files. All lines read in full.
