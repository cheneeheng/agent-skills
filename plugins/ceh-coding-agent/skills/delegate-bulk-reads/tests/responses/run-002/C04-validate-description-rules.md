## Answer

- `check_scalar_style()` function — tools/validate-plugins/validate.py:144
  - Enforces for `description` field: must use folded block scalar `>-` — tools/validate-plugins/validate.py:165-168
    - Exact failure message: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — tools/validate-plugins/validate.py:167-168
  - Enforces for every other frontmatter key: must not be an unquoted scalar containing `: ` — tools/validate-plugins/validate.py:169-170
    - Exact failure message: `f"'{key}' is an unquoted scalar containing ': ' - quote it"` — tools/validate-plugins/validate.py:170

## Not found / uncertain
- Nothing outstanding.

## Coverage
- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file. All content read.
