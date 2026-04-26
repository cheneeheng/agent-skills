---
name: "definition-of-done"
description: >
  Load this skill when preparing to open a pull request or marking a task as complete: verifying
  that a bug fix, feature, or refactor meets the quality bar before review. Auto-load whenever
  a PR is about to be opened, a task is being closed, or a checklist of completion criteria
  is needed.
---

# Definition of Done

Completion checklists for bug fixes (failing test added, root cause documented), features (unit
+ integration tests, no any/@ts-ignore), and refactors (no behavioral change, no tests deleted).
Covers coverage targets: 80% Python application package, 95% core business logic, 70% TypeScript src/lib/.
mypy --strict and tsc --noEmit must pass with zero errors.

Read [../release-ops/references/definition-of-done.md](../release-ops/references/definition-of-done.md)
and verify all applicable items before opening the PR.
