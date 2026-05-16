---
name: "python-security"
description: >
  Load this skill for Python backend security baseline: secrets management, input validation,
  parameterized SQL, CORS, rate limiting, and session token generation. Auto-load whenever
  security-sensitive code is written — auth, secrets, CORS config, or user input handling.
---

# Python Security Baseline

- Secrets loaded via `pydantic-settings` (`BaseSettings`) from `.env` — never hard-coded
- `.env` must never be committed — `.gitignore` enforced
- Validate all inputs at the API boundary using Pydantic models
- Never pass raw user input to database queries — parameterized queries always
- All LLM output must pass schema validation before any state mutation
- Use `ConfigDict(extra='forbid')` on all LLM output models
- Apply rate limiting per session on mutation endpoints (e.g. 10 req/min)
- Configure CORS explicitly — no wildcard origins in production
- Session tokens: `secrets.token_urlsafe(32)`, never logged, never in URLs
- Run `uvx pip-audit` before every release
