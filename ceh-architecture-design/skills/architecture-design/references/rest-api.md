# REST API Design

## URL Conventions

- Lowercase, hyphen-separated path segments: `/user-profiles`, not `/userProfiles`
- Plural nouns for collections: `/sessions`, not `/session`
- Nested resources for ownership: `/sessions/{id}/messages`
- No verbs in URLs — HTTP methods express the action

```
POST   /resources              Create
GET    /resources              List
GET    /resources/{id}         Get one
PATCH  /resources/{id}         Partial update
DELETE /resources/{id}         Delete
POST   /resources/{id}/archive Non-CRUD action as sub-resource
```

## HTTP Status Codes

| Code | When to use |
|------|------------|
| `200 OK` | Successful GET, PATCH, or DELETE returning data |
| `201 Created` | Successful POST that creates a resource |
| `204 No Content` | Successful operation with no response body |
| `400 Bad Request` | Malformed request syntax or type mismatch |
| `401 Unauthorized` | Authentication required but missing or invalid |
| `403 Forbidden` | Authenticated but not authorized |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Resource already exists, or illegal state transition |
| `422 Unprocessable Entity` | Syntactically valid but semantically invalid (Pydantic validation) |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server-side failure |
| `503 Service Unavailable` | Dependency unavailable (DB down, upstream timeout) |

Do not return `200` for errors. Do not return `500` for user input errors.

## Error Response Shape

All errors return a consistent envelope:

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "Resource with ID res_abc123 does not exist.",
    "correlation_id": "req_xyz789"
  }
}
```

| Field | Description |
|-------|-------------|
| `code` | Machine-readable, snake_case, stable across versions |
| `message` | Human-readable, safe to display |
| `correlation_id` | Propagated from the request for log tracing |

## API Versioning

Avoid versioning as long as possible — prefer backward-compatible additions (new optional fields, new endpoints). Only version when a breaking change cannot be avoided.

When required: use URL prefix (`/v2/resources`), maintain `/v1/` for a documented deprecation period, and record the deprecation timeline as an ADR.

## Headers

| Header | Direction | Purpose |
|--------|-----------|---------|
| `X-Correlation-ID` | Request + Response | Request tracing |
| `Content-Type: application/json` | Both | Required on all JSON endpoints |
