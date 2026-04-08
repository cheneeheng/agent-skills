---
name: "architecture-design"
description: >
  Load this skill when making structural decisions, designing new APIs, defining domain models,
  working on event-sourced state, designing or modifying database schemas, or wiring up an LLM
  integration. Covers: ADR format and lifecycle for recording durable decisions, repository layer
  boundaries and separation of concerns, domain modeling with immutable identifiers and bounded
  status enums, event sourcing with append-only event log and atomic snapshot caching, REST API
  URL conventions and HTTP status code usage, consistent error response shapes, API versioning
  strategy, PostgreSQL schema patterns with JSONB and parameterized queries, and LLM integration
  safety rules (stateless LLM as proposal engine, backend validates before any commit). Use this
  skill whenever you are making design decisions, building new endpoints, touching the database
  layer, or integrating an LLM into the application.
---

# Architecture Design

Standards for structural decisions, API design, database schemas, and LLM integrations. Covers
ADR format and lifecycle, repository layer boundaries, domain modeling with prefixed IDs and
bounded status enums, event sourcing with append-only log and atomic snapshots, REST API
conventions, PostgreSQL schema patterns, and LLM safety rules.

## References

Load the relevant file for the topic at hand.

| File | Topic |
|------|-------|
| [references/adrs.md](references/adrs.md) | ADR format, lifecycle, when to write one |
| [references/repository-structure.md](references/repository-structure.md) | Project layout and hard layer boundary rules |
| [references/domain-modeling.md](references/domain-modeling.md) | Prefixed IDs, bounded status enums, immutability rules |
| [references/event-sourcing.md](references/event-sourcing.md) | Append-only event log, atomic snapshot writes, event schema |
| [references/rest-api.md](references/rest-api.md) | URL conventions, HTTP status codes, error response shape, versioning |
| [references/postgresql.md](references/postgresql.md) | Schema design, parameterized queries, tenant isolation, migrations |
| [references/llm-integration.md](references/llm-integration.md) | LLM proposes / backend validates pattern, output schema, safety rules |
