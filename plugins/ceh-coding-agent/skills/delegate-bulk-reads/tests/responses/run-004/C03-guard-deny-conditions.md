## Answer
- `bulk-read-guard.py` denies when: enforcement is on (`BULK_READER_MIN_LINES` set, non-empty) AND `tool_name == "Read"` AND the path is present AND neither `offset` nor `limit` is set (targeted reads always pass) AND the path is not on the allowlist AND the file's line count is `>= threshold` — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:78-107
  - Threshold constant `FALLBACK_MIN_LINES = 350` — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:16, used only when `BULK_READER_MIN_LINES` is set but not parseable as an int (`ValueError`) — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:27-35
  - Env var `BULK_READER_MIN_LINES`: absent/blank → guard fully disabled (`min_lines()` returns `None`, `main` exits immediately); present and int-parseable → that int is the threshold; present but not parseable → falls back to 350 — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:27-35, 78-80
  - Env var `BULK_READER_ALLOW`: colon-separated extra fnmatch patterns appended to `ALWAYS_ALLOW` — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:38-43
  - Path exemption: `is_allowed(path)` matches either the full path or its basename via `fnmatch` against `ALWAYS_ALLOW` (`*.lock`, `package-lock.json`, `pnpm-lock.yaml`, `*.svg`, `*.min.js`, `*.min.css`, image types, `*.pdf`, `*.zip`, `*.tar`, `*.gz`) plus any `BULK_READER_ALLOW` patterns — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:19-24, 38-51
  - Fails open: non-`Read` tool calls, missing/unparseable JSON stdin, missing `file_path`, binary/unreadable files (`count_lines` returns `None`), and line count under threshold all `sys.exit(0)` without denying — plugins/ceh-coding-agent/scripts/bulk-read-guard.py:78-104

- `bulk-read-bash-guard.py` denies when: enforcement is on (`BULK_READER_MIN_LINES` set) AND `tool_name == "Bash"` AND a command segment (split on `&&`, `||`, `;`) contains a dump command (`cat`, `less`, `more`, `bat`, `batcat`) or window command (`head`, `tail`) that is not piped/redirected/`<`-fed AND the target file(s) are not allowlisted AND the counted/emitted lines reach the threshold — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:189-224, offending_file logic at 138-175
  - Threshold constant `FALLBACK_MIN_LINES = 350` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:31, same fallback-on-`ValueError` behaviour as the Read guard — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:50-58
  - Env var `BULK_READER_MIN_LINES`: identical semantics to the Read guard (unset/blank disables; parseable int is threshold; unparseable falls back to 350) — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:50-58, 190-192
  - Env var `BULK_READER_ALLOW`: same colon-separated extra patterns, appended per-call inside `is_allowed` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:61-70
  - Path exemption: same `ALWAYS_ALLOW` tuple (kept in sync per comment) plus `BULK_READER_ALLOW`, matched via `fnmatch` on full path or basename, applied per-file after glob expansion — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:40-47, 61-70, 159-161
  - Denial thresholds differ by command type: for `cat`/`less`/`more`/`bat`/`batcat`, line counts of all non-allowlisted files in the segment are **summed** and denial fires once the running total `>= threshold` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:171-174; for `head`/`tail`, each file is checked individually via `emitted_lines()` (resolving `-n`, `-c`, `+N`/`-N` offset forms against the real file) and denial fires if the actually-emitted lines `>= threshold` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:165-169, 99-135
  - Exempt/passed-through by construction: piped segments (`|`), input-redirected (`<`), and stdout-redirected segments (bare `>` or `1>`, but not `2>`) are never inspected — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:36-38, 139-140; unexpanded globs with no match fall back to treating the literal token as a path — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:159
  - Fails open: non-`Bash` tool, empty command, unparseable shlex tokens, unrecognized command name, binary/unreadable/missing files (`count_lines` → `None`), and head/tail with no explicit window (`window_arg` → `(None, None)`, default-10-line case) all skip denial — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:106-107, 138-151, 163-164, 199-204

## Not found / uncertain
- Nothing outstanding.

## Coverage
- plugins/ceh-coding-agent/scripts/bulk-read-guard.py — 124 lines read
- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 354 lines across 2 files. Nothing skipped.
