## Answer

- Line 34 (splits bash command into segments on `&&`, `||`, `;`) — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:34
  ```
  SEGMENT_SPLIT = re.compile(r"&&|\|\||;")
  ```

- Line 38 (detects stdout redirection `>` or `1>`) — plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py:38
  ```
  STDOUT_REDIRECT = re.compile(r"(?<![0-9])>|(?<![0-9])1>")
  ```

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/scripts/bulk-read-bash-guard.py — 230 lines read
- Total: 230 lines across 1 file.
