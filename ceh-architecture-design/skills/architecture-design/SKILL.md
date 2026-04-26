---
name: "architecture-design"
description: >
  Load this skill when making structural decisions, designing APIs, defining domain models,
  working on event-sourced state, designing database schemas, or integrating an LLM. Covers:
  ADR format and lifecycle, repository layer boundaries, domain modeling with prefixed IDs and
  bounded status enums, append-only event sourcing with atomic snapshots, REST API conventions
  and versioning, PostgreSQL schema patterns, and LLM safety rules (LLM proposes, backend
  validates).
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
