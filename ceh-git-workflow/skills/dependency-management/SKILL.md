---
name: "dependency-management"
description: >
  Load this skill when adding, removing, or upgrading a dependency: evaluating whether a package
  is appropriate, deciding on pinning strategy, handling a major version upgrade, or running a
  security audit. Auto-load whenever a new package is being added with uv add or bun add, a
  dependency version is being changed, or a vulnerability is found in an existing package.
---

# Dependency Management

Evaluation criteria for adding a new dependency (necessity, maintenance health, license, bundle
size), pinning policy, security audit commands (pip-audit, bun audit), and the process for
major version upgrades (dedicated PR + ADR required). Not every problem needs a new package.

Read [../git-workflow/references/dependencies.md](../git-workflow/references/dependencies.md)
and apply the evaluation criteria and policies defined there.
