---
name: "repository-structure"
description: >
  Load this skill when creating new directories, adding a new service or module, deciding where
  a file belongs, or restructuring the project layout. Auto-load whenever a new package, layer,
  or top-level directory is introduced.
---

# Repository Structure and Layer Boundaries

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
├── frontend/
│   ├── src/
│   │   ├── routes/        # SvelteKit pages and load functions
│   │   └── lib/
│   │       ├── components/ # UI components — receive props, emit events
│   │       ├── stores/     # Reactive state — updated by API responses only
│   │       ├── api/        # Centralized API client — all fetch calls go here
│   │       └── types/      # Shared TypeScript types
│   └── tests/
└── migrations/            # Database migrations (Alembic)
```

## Hard Layer Rules

- Route handlers contain no business logic — they call services
- Services contain no SQL — they call the database layer
- Database layer contains no business logic — it executes SQL
- Components do not write to stores directly — they call callbacks or dispatch events
- All `fetch` calls go through the centralized API client — components never call `fetch`
- One mutation path per aggregate — if multiple services could write the same table, define a single state manager
