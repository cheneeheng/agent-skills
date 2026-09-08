## Answer

- `check_scalar_style()` function — tools/validate-plugins/validate.py:144-170
  - For `description` field: must use the folded block scalar `>-`; exact failure message: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — tools/validate-plugins/validate.py:167-168
  - For every other frontmatter key: must not be an unquoted plain scalar containing `: ` (strict YAML parsing rejects that as a nested mapping); exact failure message: `f"'{key}' is an unquoted scalar containing ': ' - quote it"` — tools/validate-plugins/validate.py:170

## Not found / uncertain

- Nothing outstanding.

## Coverage

- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file. No files skipped.
