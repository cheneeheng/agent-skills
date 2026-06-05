#!/usr/bin/env node
// SessionStart hook — injects the Python service invariants as always-on context.
// These under-trigger as auto-load skills because they fire on implicit mid-turn decisions
// (naming a variable, adding a log line, writing a query) with no signal in the user's prompt.
// The detailed patterns and code stay in the skills (load on demand for depth); this block is
// the compact enforcement layer. Self-sufficient: works when this plugin is enabled alone.
// Cross-platform (Node), wired via hooks/hooks.json.

const invariants = `PYTHON SERVICE INVARIANTS (ceh-python-service) — apply to all Python work in this project.
These are non-negotiable defaults. For full patterns and code behind any rule, load the matching
skill via the Skill tool as \`ceh-python-service:<name>\`, where \`<name>\` is the tag shown in
brackets below (e.g. \`ceh-python-service:python-security\`).

Style & types [python-environment]:
- Type hints on every function signature and class attribute. Use 3.12 built-in generics (\`list[str]\`, not \`List[str]\`).
- No \`Any\` without a comment explaining why. No \`# type: ignore\` without a comment. Never downgrade mypy \`strict = true\` to silence errors.
- ruff only for lint/format — not flake8, pylint, isort, or Black. \`snake_case\` functions/vars, \`PascalCase\` classes, \`UPPER_SNAKE_CASE\` constants.
- Pydantic v2 \`BaseModel\` for all request/response types and domain entities. Use \`await asyncio.sleep()\`, never \`time.sleep()\`. All I/O is awaited.

Security [python-security]:
- Secrets via \`pydantic-settings\` (\`BaseSettings\`) from \`.env\` — never hard-coded; \`.env\` is never committed.
- Validate all input at the API boundary with Pydantic. Parameterized SQL always — never interpolate user input into queries.
- \`ConfigDict(extra='forbid')\` on all external-input / LLM output models; validate LLM output before any state mutation.
- CORS explicit — no wildcard origins in production. Rate-limit mutation endpoints. Session tokens: \`secrets.token_urlsafe(32)\`, never logged, never in URLs.
- Run pip-audit before every release.

Logging [python-observability]:
- structlog with an event name + key=value pairs. Never log secrets, tokens, credentials, full session/LLM content, query params containing user data, or PII.
- Every request carries a \`correlation_id\`: generated at the boundary if absent, propagated through service calls, included in every log entry, returned as \`X-Correlation-ID\`.
- Do not log at INFO on every request — use DEBUG for high-frequency events.`;

const payload = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: invariants
  }
};

process.stdout.write(JSON.stringify(payload));
