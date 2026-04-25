---
name: "rollback"
description: >
  Load this skill when deciding whether to roll back a deployment, executing an
  application rollback, or planning recovery from a failed migration. Auto-load
  whenever a deployment fails its health check, error rates spike post-deploy,
  P95 latency triples within 10 minutes of a release, or any data integrity issue
  is detected after deploying.
---

# Rollback

Rollback triggers (health check failure, error rate > 5× baseline, P95 latency >
3× baseline, or data integrity issue — all within 10 minutes of deploy), the
5-step application rollback procedure (redeploy previous image → verify /health →
confirm metrics → open incident → document), and database rollback considerations:
additive migrations are left in place; destructive migrations cannot be rolled back
and require a forward-fix.

Read [../release-ops/references/rollback.md](../release-ops/references/rollback.md)
and apply the rollback criteria and procedure defined there.
