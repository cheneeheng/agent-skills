---
name: "security"
description: >
  Load this skill when handling secrets, configuring CORS, applying rate limiting, validating
  external input, or reviewing code for security issues: adding environment variable loading,
  configuring allowed origins, protecting mutation endpoints, or setting up input validation
  with Pydantic. Auto-load whenever secrets management, CORS config, rate limiting, or
  authentication/authorization code is written or reviewed.
---

# Security

Secrets loaded via pydantic-settings (never hard-coded), .env never committed, CORS with
explicit allowed origins (never wildcard in production), rate limiting on mutation endpoints,
input validation at API boundaries, ConfigDict(extra='forbid') on LLM output models, and
pre-release vulnerability scanning with pip-audit and bun audit.

Read both reference files and apply the baseline defined there:

- [../release-ops/references/security.md](../release-ops/references/security.md) — secrets management, CORS config with code, rate limiting, input validation, pip-audit
- [../python-backend/references/security.md](../python-backend/references/security.md) — session token rules, LLM output validation before state mutation, per-session rate limit
