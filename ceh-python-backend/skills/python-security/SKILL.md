---
name: "python-security"
description: Load this skill when handling secrets, configuring CORS, applying rate limiting, validating external input, or reviewing Python service code for security issues: adding environment variable loading, configuring allowed origins, protecting mutation endpoints, or setting up input validation with Pydantic. Auto-load whenever secrets management, CORS config, rate limiting, or authentication/authorization code is written or reviewed. Not for frontend secret handling.
---

# Python Security Baseline

## Secrets Management

- Never hard-code secrets, API keys, or passwords in source code
- Load secrets via `pydantic-settings` (`BaseSettings`) from environment variables / `.env`
- Never commit `.env`; always maintain `.env.example` with placeholder values
- Generate cryptographic secrets: `python -c "import secrets; print(secrets.token_hex(32))"`
- Run `uv run pip-audit` before every release
- Session tokens: `secrets.token_urlsafe(32)`, never logged, never in URLs

## CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # from config — never wildcard in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "X-Correlation-ID"],
)
```

Never use `allow_origins=["*"]` in production.

## Rate Limiting

Apply to all mutating endpoints and expensive read endpoints. Return `429 Too Many Requests` with a `Retry-After` header when exceeded. Apply per session on mutation endpoints (e.g. 10 req/min).

## Input Validation

- All request bodies validated through Pydantic models — reject with `422` on failure
- All SQL queries use parameterized placeholders — never string interpolation
- Use `ConfigDict(extra='forbid')` on models receiving externally-sourced input (API requests, LLM output)
- All LLM output must pass schema validation before any state mutation
