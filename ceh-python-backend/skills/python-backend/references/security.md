# Security Baseline

- Secrets loaded via `pydantic-settings` (`BaseSettings`) from `.env` — never hard-coded
- `.env` files must never be committed — `.gitignore` enforced
- Validate all inputs at the API boundary using Pydantic models
- Never pass raw user input to database queries — use parameterized queries always
- All LLM output must pass schema validation before any state mutation
- Use `ConfigDict(extra='forbid')` on all LLM output models
- Apply rate limiting per session on mutation endpoints (e.g. 10 req/min)
- Configure CORS explicitly — no wildcard origins in production
- Session tokens: randomly generated (`secrets.token_urlsafe(32)`), never logged, never in URLs
- Run `uvx pip-audit` before every release to check for known vulnerabilities
