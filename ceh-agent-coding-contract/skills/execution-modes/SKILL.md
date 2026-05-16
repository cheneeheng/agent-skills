---
name: "execution-modes"
description: >
  Sets Interactive or Autonomous execution mode for the current session. Interactive Mode (default):
  stop and ask on ambiguity. Autonomous Mode: decide, document, and continue. Load when user says
  "act autonomously", "proceed autonomously", "autonomous mode", "don't stop to ask", "just do it",
  "interactive mode", or uses /execution-modes.
argument-hint: "[autonomous|interactive]"
arguments: mode
---

# Execution Modes

## Activation

Requested mode: `$mode`

- If `$mode` is `autonomous` → activate **Autonomous Mode**
- If `$mode` is `interactive` → activate **Interactive Mode**
- If `$mode` is empty and this skill was triggered by a phrase, infer from context:
  - "act autonomously" / "proceed autonomously" / "autonomous mode" / "don't stop to ask" / "just do it" → **Autonomous Mode**
  - "interactive mode" → **Interactive Mode**
- If mode still cannot be determined, use `AskUserQuestion`: "Which mode? `autonomous` (decide and document) or `interactive` (stop and ask)?"

Confirm the activated mode in one line before proceeding.

---

## Interactive Mode (Default)

Applied when no mode is specified.

- Ambiguity → **STOP → ask for clarification using the `AskUserQuestion` tool**
- No assumptions without confirmation
- No autonomous decisions

## Autonomous Mode (Explicit Opt-In)

In Autonomous Mode:
- Ambiguity → **DECIDE → DOCUMENT → continue**
- Decisions must be conservative and reasonable
- Every decision must be logged in `docs/claude_logs/DECISION_LOG.md`

A single "just do it" on a clearly scoped task activates autonomous mode for that task only.

## Authority Hierarchy (When Context Files Conflict)

1. This behavioral contract
2. Domain-specific standards (environment, testing, coding style)
3. Workflow and process files

If conflict cannot be resolved by this hierarchy, stop and ask.
