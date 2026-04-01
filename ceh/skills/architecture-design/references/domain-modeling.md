# Domain Modeling

## Immutable Identifiers

Every entity has an application-generated, prefixed, URL-safe identifier. Never use database auto-increment as the public ID — it leaks row counts and is meaningless in logs.

```python
import secrets

def generate_id(prefix: str) -> str:
    """Generates a prefixed, URL-safe unique identifier."""
    return f"{prefix}_{secrets.token_urlsafe(12)}"

# Usage
session_id = generate_id("sess")   # sess_abc123...
resource_id = generate_id("res")   # res_xyz456...
```

## Status Enums — Bounded, Not Free-Form Strings

Status values must come from an explicit, closed set. Never trust free-form strings from external callers for status fields.

```python
# Python — use StrEnum for serialization compatibility
from enum import StrEnum

class ResourceStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

```ts
// TypeScript — const assertion, never TypeScript enum
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
