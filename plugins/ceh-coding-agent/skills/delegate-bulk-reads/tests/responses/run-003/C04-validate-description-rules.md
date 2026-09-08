## Answer

- `check_scalar_style` — validate.py:144
  - For `description`: must use the folded block scalar `>-`; failure message is `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — validate.py:167-168
  - For every other frontmatter key: must not be an unquoted scalar containing `: `; failure message is `f"'{key}' is an unquoted scalar containing ': ' - quote it"` — validate.py:170

## Not found / uncertain

- Nothing outstanding.

## Coverage

- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file. No lines skipped.
