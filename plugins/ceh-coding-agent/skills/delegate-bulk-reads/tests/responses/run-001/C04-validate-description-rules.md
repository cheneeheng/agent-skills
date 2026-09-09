## Answer

- `check_scalar_style()` function — validates.py:144-171
  - For `description` field: enforces that it must use the folded block scalar `>-` — validates.py:165-168
  - Exact failure message: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — validates.py:167-168
  - For every other frontmatter key: enforces that unquoted plain scalars must not contain `: ` — validates.py:169-170
  - Exact failure message: `f"'{key}' is an unquoted scalar containing ': ' - quote it"` — validates.py:170

## Not found / uncertain
- Nothing outstanding.

## Coverage
- tools/validate-plugins/validate.py — 412 lines read
- Total: 412 lines across 1 file. All content read.
