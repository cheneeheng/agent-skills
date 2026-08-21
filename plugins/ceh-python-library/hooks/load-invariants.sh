#!/usr/bin/env bash
# SessionStart hook - injects the Python library invariants as always-on context.
# These under-trigger as auto-load skills because they fire on implicit mid-turn decisions
# with no signal in the user's prompt. The detailed patterns and code stay in the skills
# (load on demand for depth); this block is the compact enforcement layer. Self-sufficient:
# works when this plugin is enabled alone. Pure-shell (bash), no Node required; wired via
# hooks/hooks.json. The payload below is static JSON.
cat <<'JSON_EOF'
{"systemMessage":"ceh-python-library: loading Python library invariants for this session.","hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"PYTHON LIBRARY INVARIANTS (ceh-python-library) — apply to all Python work in this project.\nThese are non-negotiable defaults. For full patterns and code behind any rule, load the matching\nskill via the Skill tool as `ceh-python-library:<name>`, where `<name>` is the tag shown in\nbrackets below (e.g. `ceh-python-library:python-library-environment`).\n\nStyle & types [python-library-environment]:\n- Type hints on every function signature and class attribute. Use 3.12 built-in generics (`list[str]`, not `List[str]`).\n- No `Any` without a comment explaining why. No `# type: ignore` without a comment. Never downgrade mypy `strict = true` to silence errors.\n- ruff only for lint/format — not flake8, pylint, isort, or Black. Line length 88. `snake_case` functions/vars, `PascalCase` classes, `UPPER_SNAKE_CASE` constants.\n- Google-style docstrings required on all public symbols.\n\nDependencies [python-library-environment]:\n- Keep the runtime dependency set minimal — a library imposes every dependency onto every consumer. Start from `dependencies = []` and add only what is truly required.\n- Never add web-service deps (`fastapi`, `uvicorn`, `asyncpg`) to a library. Never edit `uv.lock` manually; never commit `.env`."}}
JSON_EOF
