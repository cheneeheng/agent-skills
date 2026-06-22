---
name: release-flow
description: "Load when shipping a complete project release in one pass — bump the version, update the changelog/README/CLAUDE.md, open a PR, merge it, then tag and publish the release. Trigger on \"run the release flow\", \"do the full release\", \"ship this release end to end\", \"release this project\", \"bump version, update docs, open a PR, merge, tag and release\", or \"cut a full release through a PR\". This skill only sequences the steps and gates between them; it delegates each step to the skill that owns it (branch, update-changelog, update-readme, commit, open-pr, merge, release). Not for tagging alone (use ceh-git-workflow:release) or an urgent production fix (use ceh-git-workflow:hotfix)."
---

# Release Flow

End-to-end project release in one pass: **version bump → changelog → README → CLAUDE.md → commit
→ PR → merge → tag → GitHub release**. This skill owns only the **ordering and the gate between
each step**; every step is delegated to the skill that already owns it, so nothing here is
duplicated.

What it adds over running the steps ad hoc: the version bump lands through a **reviewed PR**, and
the tag + release happen **only after merge, on `main`, pointing at the merge commit** — never on
the feature branch.

## Pipeline

Run top to bottom. Each step gates the next — do not proceed past a red gate.

| # | Step | Delegate to (trigger phrase / repo skill) | Gate before next step |
|---|------|-------------------------------------------|-----------------------|
| 1 | Decide the semver bump — MAJOR/MINOR/PATCH; when in doubt, PATCH | "cut a release" → `ceh-git-workflow:release` (bump table) | Version chosen, never below current |
| 2 | Branch `chore/release-vX.Y.Z` from latest `main` | "create a branch" → `ceh-git-workflow:branch` | On a clean branch off up-to-date `main` |
| 3 | Bump the version in **every** manifest the project ships (`pyproject.toml`, `package.json`, `plugin.json`, `marketplace.json`, `Cargo.toml`, …) | — mechanical edit | All manifests read the same vX.Y.Z |
| 4 | Write the vX.Y.Z changelog entry | "update the changelog" → `ceh-documentation:update-changelog` | Section written and semver-validated |
| 5 | Refresh the README if the change is user-facing | "update the readme" → `ceh-documentation:update-readme` | Updated, or "no update needed" recorded |
| 6 | Update CLAUDE.md if project facts/structure changed | surgical edit (or `revise-claude-md` if that plugin is installed) | CLAUDE.md matches reality, or skip logged |
| 7 | Commit the bump + docs | "commit" → `ceh-git-workflow:commit` | Subject `chore: release vX.Y.Z`, tree clean |
| 8 | Open the PR | "open a PR" → `ceh-git-workflow:open-pr` | PR open, self-review + definition-of-done passed |
| 9 | Merge and delete the branch — prefer `--auto` so GitHub queues the merge and lands it when the gate goes green; don't poll CI by hand | "merge the PR" → `ceh-git-workflow:merge` (auto-merge probe) | CI green, approvals met, merged to `main` |
| 10 | Tag and publish the release on `main` | "cut a release" → `ceh-git-workflow:release` | Tag pushed, release created |

## Step 10 detail — tag and release *after* merge

The release skill commits the bump to `main` directly; here the bump already landed via the PR, so
**skip its commit step** and run only the tag + release, on `main`, once the merge is in:

```bash
git checkout main && git pull origin main      # the merge commit is now HEAD
git tag -a vX.Y.Z -m "vX.Y.Z — <summary>"      # annotated; points at the merge commit
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <changelog-section-file>
```

Reuse the vX.Y.Z section you wrote in step 4 as the release notes (`--notes-file`).

## Hard rules

- **One version, everywhere.** Every manifest the project ships reads the same vX.Y.Z before the
  commit in step 7.
- **Tag the merge commit on `main`**, never the feature branch — `git pull origin main` after the
  merge first, then tag.
- **Never tag or release on a red gate.** CI must be green and required approvals met (step 9)
  before step 10. Surface a red gate and wait; do not merge or tag around it.
- **Versions only increase.** When the bump level is unclear, PATCH.
- If a step's owning skill is not installed, its trigger phrase still names the standard — apply it
  inline rather than skipping the step.
