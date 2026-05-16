---
name: "domain-modeling"
description: >
  Load this skill when designing or modifying domain entities: defining new entity IDs, choosing
  identifier formats, creating or extending status fields, designing state transition rules, or
  modelling ownership and relationships between entities. Auto-load whenever a new entity type is
  introduced, a status enum is added or changed, or an ID field is defined.
---

# Domain Modeling

## Immutable Identifiers

Every entity has an application-generated, prefixed, URL-safe identifier. Never use database auto-increment as the public ID — leaks row counts and is meaningless in logs.

```python
import secrets

def generate_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(12)}"

session_id = generate_id("sess")   # sess_abc123...
resource_id = generate_id("res")   # res_xyz456...
```

## Bounded Status Enums

Status values must come from an explicit, closed set. Never trust free-form strings from external callers for status fields.

```python
from enum import StrEnum

class ResourceStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

```ts
const ResourceStatus = {
  Active: 'active',
  Archived: 'archived',
  Deleted: 'deleted',
} as const;
type ResourceStatus = typeof ResourceStatus[keyof typeof ResourceStatus];
```

## Immutability Rules

- IDs are set once at creation, never changed
- `created_at` timestamps are set once, never updated
- Status transitions must be validated — not all transitions are legal
- Document all legal and illegal transitions explicitly
