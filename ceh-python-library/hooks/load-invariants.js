#!/usr/bin/env node
// SessionStart hook — injects the Python library invariants as always-on context.
// These under-trigger as auto-load skills because they fire on implicit mid-turn decisions
// (naming a symbol, writing a signature, reaching for a dependency) with no signal in the user's
// prompt. The detailed patterns and code stay in the skills (load on demand for depth); this block
// is the compact enforcement layer. Self-sufficient: works when this plugin is enabled alone.
// Cross-platform (Node), wired via hooks/hooks.json.

const invariants = `PYTHON LIBRARY INVARIANTS (ceh-python-library) — apply to all Python work in this project.
These are non-negotiable defaults. For full patterns and code behind any rule, load the matching
skill via the Skill tool as \`ceh-python-library:<name>\`, where \`<name>\` is the tag shown in
brackets below (e.g. \`ceh-python-library:python-library-environment\`).

Style & types [python-library-environment]:
- Type hints on every function signature and class attribute. Use 3.12 built-in generics (\`list[str]\`, not \`List[str]\`).
- No \`Any\` without a comment explaining why. No \`# type: ignore\` without a comment. Never downgrade mypy \`strict = true\` to silence errors.
- ruff only for lint/format — not flake8, pylint, isort, or Black. Line length 88. \`snake_case\` functions/vars, \`PascalCase\` classes, \`UPPER_SNAKE_CASE\` constants.
- Google-style docstrings required on all public symbols.

Dependencies [python-library-environment]:
- Keep the runtime dependency set minimal — a library imposes every dependency onto every consumer. Start from \`dependencies = []\` and add only what is truly required.
- Never add web-service deps (\`fastapi\`, \`uvicorn\`, \`asyncpg\`) to a library. Never edit \`uv.lock\` manually; never commit \`.env\`.`;

const payload = {
  systemMessage: "ceh-python-library: loading Python library invariants for this session.",
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: invariants
  }
};

process.stdout.write(JSON.stringify(payload));
