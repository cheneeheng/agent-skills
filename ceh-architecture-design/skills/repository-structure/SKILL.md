---
name: "repository-structure"
description: Load this skill when organizing backend code or deciding where a module belongs: adding a service, route module, or database-access module, or setting the layer boundaries between API, services, and the database layer. Auto-load whenever a new backend package, layer, or top-level directory is introduced. (Frontend structure lives in the sveltekit skill.)
---

# Backend Repository Structure and Layer Boundaries

Organize by concern, not by file type. Each layer has one job.

```
project/
├── backend/
│   ├── app/
│   │   ├── api/           # Thin route handlers — validate input, call service, return output
│   │   ├── core/          # Config, dependencies, exceptions, middleware
│   │   ├── models/        # Pydantic request/response + domain models
│   │   ├── services/      # Business logic — no HTTP, no SQL
│   │   └── db/            # Database queries — SQL only, no business logic
│   └── tests/
└── migrations/            # Database migrations (Alembic)
```

## Hard Layer Rules

- Route handlers contain no business logic — they call services
- Services contain no SQL — they call the database layer
- Database layer contains no business logic — it executes SQL
- One mutation path per aggregate — if multiple services could write the same table, define a single state manager
