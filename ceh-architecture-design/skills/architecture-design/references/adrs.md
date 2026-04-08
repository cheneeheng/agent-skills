# Architecture Decision Records (ADRs)

Record every significant architectural decision. A decision is significant if it would be confusing to a future developer without the context behind it, or if reversing it would require a migration or broad refactor.

## When to Write an ADR

- Choosing a framework, runtime, or infrastructure tool
- Defining a data persistence strategy (schema shape, migration approach)
- Choosing between fundamentally different implementation patterns
- Any major version upgrade of a core dependency
- Any decision you find yourself explaining repeatedly in PR reviews

## ADR Format

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

## ADR Lifecycle

- `Proposed` — written, pending team review
- `Accepted` — agreed upon and in force
- `Superseded by ADR-NNN` — replaced; link to the superseding ADR

Never delete ADRs. Mark as superseded and link forward. History is valuable.

To change a decision: write a new ADR that references and supersedes the old one. Never silently diverge from an accepted ADR.
