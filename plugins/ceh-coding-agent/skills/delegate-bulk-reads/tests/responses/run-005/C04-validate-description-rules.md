## Answer
- `check_scalar_style` (function) — tools/validate-plugins/validate.py:144-170 — enforces the frontmatter scalar conventions:
  - `description` must be exactly the folded block scalar `>-`. If `value != ">-"`, it fails with: `"'description' must use the folded block scalar '>-' (found {value[:12]!r}...) - see CLAUDE.md"` — tools/validate-plugins/validate.py:165-168.
  - Every other key: if its value is non-empty, does not start with `'`, `"`, `>`, or `|`, and contains `": "`, it fails with: `"'{key}' is an unquoted scalar containing ': ' - quote it"` — tools/validate-plugins/validate.py:169-170.
- `check_frontmatter_doc` (function) — tools/validate-plugins/validate.py:173-191 — additionally enforces `description` presence/length (not scalar style): missing description fails with `"frontmatter missing 'description'"` (line 186), and over `MAX_DESCRIPTION_LEN` (1024, line 37) fails with `f"description is {len(desc)} chars, exceeds {MAX_DESCRIPTION_LEN} limit"` (line 188). It also checks `compatibility` length (`f"compatibility is {len(compat)} chars, exceeds {MAX_COMPATIBILITY_LEN} limit"`, line 191), and `name` presence/match (lines 180-183) — not part of the "every other key" scalar rule but part of the same function.
- Both checks are wired together per doc in `check_frontmatter_doc` — tools/validate-plugins/validate.py:175 (`check_scalar_style(path)` call) then frontmatter parsing/length checks (lines 176-191); `check_frontmatter_doc` itself is called for every SKILL.md via `check_skills` (line 203) and every agent `.md` via `check_agents` (line 209).

## Not found / uncertain
- Nothing outstanding — the question is fully answered from the single file provided.

## Coverage
- tools/validate-plugins/validate.py — 413 lines read
- Total: 413 lines across 1 file.
