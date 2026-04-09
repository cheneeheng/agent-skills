---
name: "fastapi"
description: >
  Load this skill when writing FastAPI route handlers, services, or middleware: adding a new
  endpoint, wiring up dependency injection, configuring lifespan startup/shutdown, registering
  exception handlers, or defining the custom exception hierarchy. Auto-load whenever a route
  handler is written, a FastAPI dependency is defined, or a domain exception is added.
---

# FastAPI Conventions

Thin route handler pattern, dependency injection setup, lifespan for startup/shutdown,
middleware registration order, global exception handler mapping, and the custom exception
hierarchy with service/handler boundary rules. Route handlers must contain no business logic —
they validate input, call a service, and return output.

Read both reference files and apply the conventions defined there:

- [../python-backend/references/fastapi.md](../python-backend/references/fastapi.md) — handler patterns, DI, lifespan, middleware order, exception handlers
- [../python-backend/references/exceptions.md](../python-backend/references/exceptions.md) — custom exception hierarchy, service vs handler boundary rules
