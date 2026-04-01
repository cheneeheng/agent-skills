# Stop Conditions and Partial Failures

## Stop Conditions (All Modes)

Stop and request clarification when:
- Context files conflict and the authority hierarchy cannot resolve it
- Repository state contradicts the instructions
- A change risks data loss, security issues, or irreversible impact
- A partial failure leaves the system in an inconsistent state

Always report what was completed before stopping. Do not silently roll back.

## Partial Failures

If a task partially completes before a blocker:
- Do not roll back completed work silently
- Report what was finished and what was not
- Describe the blocker explicitly
- Await instruction before continuing

## Multi-Agent Scenarios

When operating as a sub-agent invoked by another agent:
- Treat the calling agent's instructions as user-level authorization
- Do not escalate scope beyond what the calling agent requested
- Autonomous Mode decisions still require documentation
