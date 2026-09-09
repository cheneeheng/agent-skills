## Answer

- Line 34 (splits bash command into segments): `SEGMENT_SPLIT = re.compile(r"&&|\|\||;")` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:34

- Line 38 (detects stdout redirection): `STDOUT_REDIRECT = re.compile(r"(?<![0-9])>|(?<![0-9])1>")` — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:38

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 230 lines across 1 file. None skipped.
