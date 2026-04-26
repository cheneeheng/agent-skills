# ceh-architecture-design

Architectural standards for APIs, domain modeling, event sourcing, LLM integration, and
PostgreSQL. Covers structural decisions, layer boundaries, REST conventions, schema design,
and LLM safety rules.

## Bundle Skills

| Skill | Invoke | Description |
|-------|--------|-------------|
| `architecture-design` | `/architecture-design` | Full architectural standards — load when making structural decisions, designing APIs, or touching the database |

## Micro-Skills (Auto-Load)

| Skill | Triggers When |
|-------|---------------|
| `adr` | Making a significant architectural decision that should be recorded |
| `domain-modeling` | Designing entities, identifier formats, status enums, or state transitions |
| `event-sourcing` | Working with event logs, state snapshots, or event types |
| `llm-integration` | Writing LLM API calls, defining output schemas, or validating LLM responses |
| `postgresql` | Writing SQL, designing schemas, asyncpg queries, or filtering by tenant |
| `repository-structure` | Creating new directories, adding modules, or deciding where code belongs |
| `rest-api` | Designing REST endpoints, choosing HTTP status codes, or shaping error responses |

## Reference Files

All reference files live under `skills/architecture-design/references/`:

| File | Topic |
|------|-------|
| `adrs.md` | ADR format, lifecycle, when to write one |
| `repository-structure.md` | Project layout and hard layer boundary rules |
| `domain-modeling.md` | Prefixed IDs, bounded status enums, immutability rules |
| `event-sourcing.md` | Append-only event log, atomic snapshot writes, event schema |
| `rest-api.md` | URL conventions, HTTP status codes, error response shape, versioning |
| `postgresql.md` | Schema design, parameterized queries, tenant isolation, migrations |
| `llm-integration.md` | LLM proposes / backend validates pattern, output schema, safety rules |

Cross-bundle stub: `skills/python-backend/references/database.md` — asyncpg queries,
transactions, connection pool (mirrors `ceh-python-backend`).
