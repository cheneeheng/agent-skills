# Security — Python Backend Specifics

## Session Tokens

Randomly generated: `secrets.token_urlsafe(32)`. Never log session tokens and
never include them in URLs — URLs appear in server access logs and browser history.

## LLM Output Validation

All LLM output must pass schema validation **before any state mutation**. Use
`ConfigDict(extra='forbid')` on all LLM output models to reject unexpected fields.

## Rate Limiting

Apply per-session rate limit on mutation endpoints: 10 requests/minute per session.
