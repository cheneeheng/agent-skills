---
name: "domain-modeling"
description: >
  Load this skill when designing or modifying domain entities: defining new entity IDs, choosing
  identifier formats, creating or extending status fields, designing state transition rules, or
  modelling ownership and relationships between entities. Auto-load whenever a new entity type is
  introduced, a status enum is added or changed, or an ID field is defined.
---

# Domain Modeling

Conventions for entity identifiers, status enums, and immutability rules. Covers prefixed
URL-safe IDs, bounded status enums using StrEnum (Python) and const assertions (TypeScript),
and the immutability rules for IDs, timestamps, and status transitions.

Read [../architecture-design/references/domain-modeling.md](../architecture-design/references/domain-modeling.md)
and apply the conventions defined there.
