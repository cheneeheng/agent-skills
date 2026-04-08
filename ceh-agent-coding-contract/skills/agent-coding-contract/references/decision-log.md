# Decision Log Format

When operating in Autonomous Mode, append each decision to `docs/claude_logs/DECISION_LOG.md`. Create the file and any missing parent directories if they do not exist.

```markdown
### Entry <ID>

**Type:** Decision | Execution
**Mode:** Autonomous
**Timestamp:** <ISO-8601>
**Task:** <brief description>

**Context:** What was ambiguous or why a decision was needed.
**Decision / Action:** What was decided or executed.
**Rationale:** Why this choice was made.
**Impact / Risk:** Potential side effects.
**Outcome:** Observed result (if applicable).
```
