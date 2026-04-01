# Incident Management

## Severity Levels

| Level | Definition | Response Time |
|-------|-----------|--------------|
| P1 | Production is down or data is corrupted | Immediate — all hands |
| P2 | Major feature broken, no workaround for users | < 1 hour |
| P3 | Feature degraded, workaround exists | < 1 business day |

## Incident Response Steps

1. **Detect** — identify from monitoring alerts or user report
2. **Triage** — classify severity, identify scope
3. **Mitigate** — roll back if available; disable the feature if possible
4. **Fix** — hotfix process (see hotfix.md)
5. **Post-mortem** — written within 48 hours for P1/P2

## Post-Mortem Format (Required for P1 and P2)

```markdown
## Incident Post-Mortem: <Short Title>

**Date:** YYYY-MM-DD
**Severity:** P1 | P2
**Duration:** <how long production was impacted>

### What Happened
Brief timeline of events.

### Root Cause
The single underlying cause (not symptoms).

### Impact
What was broken. How many users/requests affected.

### Detection
How was the incident discovered? How long between impact and detection?

### Resolution
What fixed it?

### Prevention
What changes prevent recurrence?
- [ ] Action item (owner, due date)
```
