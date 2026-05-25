---
name: "adr"
description: Load this skill when making a significant architectural decision: choosing a framework, runtime, or persistence strategy; picking between fundamentally different implementation approaches; planning a major dependency upgrade; or explaining the same design rationale in multiple PR reviews. Auto-load when a decision would confuse a future developer without context, or reversing it requires a migration.
---

# Architecture Decision Records (ADRs)

Record every significant architectural decision — one that would confuse a future developer without context, or that reversing would require a migration or refactor.

**When to write an ADR:**
- Choosing a framework, runtime, or infrastructure tool
- Defining a data persistence strategy (schema shape, migration approach)
- Choosing between fundamentally different implementation patterns
- Any major version upgrade of a core dependency
- Any decision you find yourself explaining repeatedly in PR reviews

## Format

```markdown
## ADR-<NNN>: <Short, Descriptive Title>

**Status:** Proposed | Accepted | Superseded by ADR-<NNN>
**Date:** YYYY-MM-DD

### Context
Problem or situation requiring a decision. Include constraints, goals, and options considered.

### Decision
What was decided. Be explicit and unambiguous.

### Consequences
Implications, trade-offs, limitations, follow-up considerations.

### Alternatives Considered (Optional)
What was not chosen and why.
```

## Lifecycle

- `Proposed` — written, pending team review
- `Accepted` — agreed upon and in force
- `Superseded by ADR-NNN` — replaced; link to the superseding ADR

Never delete ADRs — mark superseded and link forward. To change a decision, write a new ADR. Never silently diverge from an accepted ADR.
