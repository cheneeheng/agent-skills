---
name: "incidents"
description: >
  Load this skill when responding to a production incident, writing a post-mortem, executing a
  hotfix, or classifying incident severity. Auto-load whenever a production issue is reported,
  a P1/P2/P3 classification is needed, a hotfix branch is being created, or a post-mortem
  document is being written.
---

# Incident Response

P1/P2/P3 severity classification and response time targets, the five-step incident response
process (detect → triage → mitigate → fix → post-mortem), post-mortem format required for P1
and P2, and the hotfix process (minimal scope, all CI must pass, staging still required).

Read both reference files and apply the procedures defined there:

- [../release-ops/references/incidents.md](../release-ops/references/incidents.md) — severity levels, response steps, post-mortem format
- [../release-ops/references/hotfix.md](../release-ops/references/hotfix.md) — hotfix branch, scope, CI requirements, abbreviated deploy steps
