---
name: "event-sourcing"
description: >
  Load this skill when working with the event log or state snapshots: appending events, reading
  or replaying the event log, updating snapshots, designing new event types, or modifying the
  transaction that writes events and snapshots atomically. Auto-load whenever event_log or
  state_snapshot tables are touched, or a new event type is introduced.
---

# Event Sourcing

The append-only event log pattern, atomic event-plus-snapshot writes, event schema design,
and the closed enum of allowed event types. The event log is a permanent record — UPDATE and
DELETE on event rows are forbidden always.

Read [../architecture-design/references/event-sourcing.md](../architecture-design/references/event-sourcing.md)
and apply the invariants and patterns defined there.
