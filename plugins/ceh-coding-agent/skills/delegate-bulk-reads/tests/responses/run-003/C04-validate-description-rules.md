## Answer

- `check_scalar_style()` function — validate.py:144
  - Enforces for `description` field: must use folded block scalar `>-` — validate.py:165-168
    - Failure message: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — validate.py:167-168
  - Enforces for every other frontmatter key: must not be an unquoted scalar containing `': '` — validate.py:169-170
    - Failure message: `"'{key}' is an unquoted scalar containing ': ' - quote it"` — validate.py:170

## Not found / uncertain
- Nothing outstanding.

## Coverage
- C:\Users\Chen\WorkLocal\00_Project\agent-skills\tools\validate-plugins\validate.py — 413 lines read
- Total: 413 lines across 1 file. No files skipped.
