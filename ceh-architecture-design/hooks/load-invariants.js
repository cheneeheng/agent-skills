#!/usr/bin/env node
// SessionStart hook — injects the architecture invariants as always-on context.
// These are the must-always-hold rules that under-trigger as auto-load skills because
// they fire on implicit mid-turn decisions with no signal in the user's prompt. The
// detailed patterns and code stay in the skills (load on demand for depth); this block
// is the compact enforcement layer. Cross-platform (Node), wired via hooks/hooks.json.

const invariants = `ARCHITECTURE INVARIANTS (ceh-architecture-design) — apply to all work in this project.
These are non-negotiable defaults. For the full patterns and code behind any rule, load the matching
skill via the Skill tool as \`ceh-architecture-design:<name>\`, where \`<name>\` is the tag shown in
brackets below (e.g. \`ceh-architecture-design:postgresql\`).

Identifiers & entities [domain-modeling]:
- Public IDs are application-generated, prefixed, URL-safe: \`{prefix}_{secrets.token_urlsafe(12)}\`. Never expose DB auto-increment as a public ID.
- Status fields come from a closed set (Python StrEnum / TS \`as const\`). Never accept free-form status strings from external callers.
- IDs and \`created_at\` are set once and never changed. Status transitions must be validated — not all are legal.

Layer boundaries [repository-structure]:
- Route handlers contain no business logic — they call services.
- Services contain no SQL — they call the db layer. The db layer contains no business logic.
- One mutation path per aggregate.

PostgreSQL [postgresql]:
- Parameterized queries only (\`$1\`, \`$2\`). Never interpolate values into SQL.
- Tenant isolation: every query on user-owned data filters by \`owner_id\`. One user's data is never reachable by another.
- \`TIMESTAMPTZ\` storing UTC; \`JSONB\` for evolving data, typed columns for anything filtered or sorted.
- Migrations via Alembic, backward-compatible; destructive changes are two-step (stop using, then drop).

Event sourcing [event-sourcing]:
- The event log is append-only — \`UPDATE\`/\`DELETE\` on event rows are forbidden.
- Every event append and its snapshot update happen in a single transaction.
- Event types are a closed, application-controlled enum. Unknown types are rejected.

LLM integration [llm-integration]:
- LLM proposes, backend validates and commits. Validate all proposed events against domain invariants before any state mutation.
- \`extra='forbid'\` on all LLM output models. Reject unknown event types — no authority escalation.
- All-or-nothing: any single invalid event rejects the whole batch. Never log full LLM responses at INFO.`;

const payload = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: invariants
  }
};

process.stdout.write(JSON.stringify(payload));
