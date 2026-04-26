---
name: "observability"
description: >
  Load this skill when adding or modifying logging, metrics, health checks, or correlation ID
  propagation: writing structured log calls, choosing log levels, adding Prometheus metrics,
  defining the health check endpoint, or wiring up correlation ID middleware. Auto-load whenever
  a log call is written, a metric is added, or the /health endpoint is touched.
---

# Observability

Structured logging with structlog (log levels, what never to log), correlation ID generation
and propagation through the full request lifecycle, required Prometheus metrics and their labels,
and the health check endpoint contract (200 healthy / 503 degraded, must verify DB connectivity).

Read both reference files and apply the conventions defined there:

- [../release-ops/references/observability.md](../release-ops/references/observability.md) — structlog levels, correlation ID middleware, required Prometheus metrics, health check contract
- [../python-backend/references/observability.md](../python-backend/references/observability.md) — Python-specific log examples, PII never-log rules
