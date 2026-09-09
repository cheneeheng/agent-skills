## Answer
- `check_scalar_style` (`tools/validate-plugins/validate.py:144-170`) enforces the `description` frontmatter field and every other key's scalar style:
  - `description` must equal exactly `>-` (the folded block scalar) — if not, it fails with the exact message built from `path:167-168`: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"`.
  - Every other frontmatter key must not be an unquoted plain scalar containing `': '` — checked at `path:169` (`elif value and not value.startswith(("'", '"', ">", "|")) and ": " in value:`), failing with the exact message at `path:170`: `"'{key}' is an unquoted scalar containing ': ' - quote it"`.
- `check_frontmatter_doc` (`tools/validate-plugins/validate.py:173-191`) separately enforces content-level rules on `description` (not style): missing `description` fails with `"frontmatter missing 'description'"` (`path:186`), and length over `MAX_DESCRIPTION_LEN` (1024, `path:37`) fails with `f"description is {len(desc)} chars, exceeds {MAX_DESCRIPTION_LEN} limit"` (`path:187-188`).

## Not found / uncertain
- Nothing outstanding — the question's scope (description scalar-style enforcement, other-key scalar-style enforcement, function names, exact messages) is fully answered from this single file.

## Coverage
- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file. Nothing skipped.
