# Execution Modes

## Interactive Mode (Default)

Applied when no mode is specified.

- Ambiguity → **STOP → ask for clarification**
- No assumptions without confirmation
- No autonomous decisions

## Autonomous Mode (Explicit Opt-In)

Activated only by an explicit instruction such as:
- "proceed autonomously"
- "autonomous mode"
- "don't stop to ask, just do it"

A single "just do it" on a clearly scoped task activates autonomous mode for that task only.

In Autonomous Mode:
- Ambiguity → **DECIDE → DOCUMENT → continue**
- Decisions must be conservative and reasonable
- Every decision must be logged in `docs/claude_logs/DECISION_LOG.md`

## Authority Hierarchy (When Context Files Conflict)

1. This behavioral contract
2. Domain-specific standards (environment, testing, coding style)
3. Workflow and process files

If conflict cannot be resolved by this hierarchy, stop and ask.
