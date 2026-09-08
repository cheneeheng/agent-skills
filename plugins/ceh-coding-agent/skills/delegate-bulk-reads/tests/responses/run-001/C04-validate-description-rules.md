## Answer

- `check_scalar_style` function enforces both rules — tools/validate-plugins/validate.py:144-170

- **For `description` field:** Must use the folded block scalar `>-`. The function checks if the value after the colon is exactly `>-`, and fails with message: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — tools/validate-plugins/validate.py:165-168

- **For every other frontmatter key:** Must not be an unquoted plain scalar containing `: ` (a colon followed by a space). The function checks if the value starts with a quote or block scalar indicator and contains `: `, and fails with message: `"'{key}' is an unquoted scalar containing ': ' - quote it"` — tools/validate-plugins/validate.py:169-170

## Not found / uncertain

- Nothing outstanding.

## Coverage

- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file.
