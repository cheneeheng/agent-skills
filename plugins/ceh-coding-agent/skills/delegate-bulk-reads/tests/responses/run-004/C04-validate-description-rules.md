## Answer
- `check_scalar_style(path)` — tools/validate-plugins/validate.py:144-170 — enforces the `description` and other-key frontmatter rules described below; called from `check_frontmatter_doc` at tools/validate-plugins/validate.py:175.
- `description` must be the folded block scalar `>-` — tools/validate-plugins/validate.py:165-168: if `key == "description"` and `value != ">-"`, it calls `fail`, producing the message:
  `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — tools/validate-plugins/validate.py:167-168.
- Every other frontmatter key must not be an unquoted plain scalar containing `": "` — tools/validate-plugins/validate.py:169-170: for any key other than `description`, if the value is non-empty, does not start with `'`, `"`, `>`, or `|`, and contains `": "`, it calls `fail`, producing the message:
  `"'{key}' is an unquoted scalar containing ': ' - quote it"` — tools/validate-plugins/validate.py:170.
- Additional `description`/`compatibility` constraints enforced separately in `check_frontmatter_doc(path, expected_name)` — tools/validate-plugins/validate.py:173-191:
  - Missing `description` → `"frontmatter missing 'description'"` — tools/validate-plugins/validate.py:185-186.
  - `description` longer than `MAX_DESCRIPTION_LEN` (1024, tools/validate-plugins/validate.py:37) → `f"description is {len(desc)} chars, exceeds {MAX_DESCRIPTION_LEN} limit"` — tools/validate-plugins/validate.py:187-188.
  - `compatibility` longer than `MAX_COMPATIBILITY_LEN` (500, tools/validate-plugins/validate.py:38) → `f"compatibility is {len(compat)} chars, exceeds {MAX_COMPATIBILITY_LEN} limit"` — tools/validate-plugins/validate.py:189-191.
- `check_scalar_style` and the length/presence checks are both invoked per skill/agent doc from `check_frontmatter_doc`, which is called by `check_skills()` (tools/validate-plugins/validate.py:194-203) and `check_agents()` (tools/validate-plugins/validate.py:206-209).

## Not found / uncertain
- Nothing outstanding.

## Coverage
- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file. Nothing skipped.
