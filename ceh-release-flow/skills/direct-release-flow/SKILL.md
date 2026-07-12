---
name: direct-release-flow
disable-model-invocation: true
description: "Ship a complete project release in one pass directly on main, with no PR and no merge — bump the version, update the changelog/README/CLAUDE.md, commit straight to main, then tag and publish the release. This skill only sequences the steps and gates between them; it delegates each step to the skill that owns it (update-changelog, update-readme, commit, release). For the PR-gated variant use ceh-release-flow:release-flow; for tagging alone use ceh-git-workflow:release; for an urgent production fix use ceh-git-workflow:hotfix."
---

# Direct Release Flow

End-to-end project release in one pass, **directly on `main` with no PR and no merge**: **version
bump → changelog → README → CLAUDE.md → commit on `main` → tag → GitHub release**. This skill owns
only the **ordering and the gate between each step**; every step is delegated to the skill that
already owns it, so nothing here is duplicated.

This is the PR-less variant of `ceh-release-flow:release-flow`. Use it for solo repos, low-risk
releases, or projects where direct commits to `main` are the norm. When the bump should land
through a reviewed PR instead, use `ceh-release-flow:release-flow`.

## Pipeline

Run top to bottom. Each step gates the next — do not proceed past a red gate.

| # | Step | Delegate to (trigger phrase / repo skill) | Gate before next step |
|---|------|-------------------------------------------|-----------------------|
| 1 | Decide the semver bump — MAJOR/MINOR/PATCH; when in doubt, PATCH | "cut a release" → `ceh-git-workflow:release` (bump table) | Version chosen, never below current |
| 2 | Confirm you are on an up-to-date `main` | `git checkout main && git pull origin main` | Clean tree on latest `main` |
| 3 | Bump the version in **every** manifest the project ships (`pyproject.toml`, `package.json`, `plugin.json`, `marketplace.json`, `Cargo.toml`, …) | — mechanical edit | All manifests read the same vX.Y.Z |
| 4 | Write the vX.Y.Z changelog entry | "update the changelog" → `ceh-documentation:update-changelog` | Section written and semver-validated |
| 5 | Refresh the README if the change is user-facing | "update the readme" → `ceh-documentation:update-readme` | Updated, or "no update needed" recorded |
| 6 | Update CLAUDE.md if project facts/structure changed | surgical edit (or `revise-claude-md` if that plugin is installed) | CLAUDE.md matches reality, or skip logged |
| 7 | Commit the bump + docs straight to `main` | "commit" → `ceh-git-workflow:commit` | Subject `chore: release vX.Y.Z`, tree clean, pushed to `main` |
| 8 | Tag and publish the release on `main` | "cut a release" → `ceh-git-workflow:release` | Tag pushed, release created |

## Delegating steps 7–8 to subagents

Steps 7–8 are mechanical once the docs are written. When the `ceh-git-workflow` agents are
installed, dispatch them to the subagent that owns each — `commit-author` (7, tell it the commit
goes straight to `main` and must be pushed) and `release-cutter` (8, pass "tag-only" plus the
changelog notes file) — to keep the main session lean. Dispatch each on the model and effort
declared in its frontmatter: **Claude Sonnet at medium reasoning effort** for both. These steps
write to `main` — do not downgrade to a smaller model or lower effort. The gates stay **here**: check each step's
gate on the agent's report before dispatching the next. Steps 1–6 stay in the main session — they
need the session's context to write correct docs. Without the agents, delegate to the skills by
trigger phrase as in the table.

## Step 8 detail — tag and release after the commit lands

The bump is already committed to `main` in step 7, so **skip the release skill's commit step** and
run only the tag + release, on `main`:

```bash
git push origin main                           # step 7's commit is now on the remote HEAD
git tag -a vX.Y.Z -m "vX.Y.Z — <summary>"      # annotated; points at the release commit
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <changelog-section-file>
```

Reuse the vX.Y.Z section you wrote in step 4 as the release notes (`--notes-file`).

## Hard rules

- **One version, everywhere.** Every manifest the project ships reads the same vX.Y.Z before the
  commit in step 7.
- **Commit and tag on `main`.** This flow has no branch and no PR — confirm you are on an
  up-to-date `main` (step 2) before committing, and tag the release commit you just pushed.
- **Push before you tag.** The release commit must be on the remote `main` (step 7) before the tag
  in step 8, so the tag points at a pushed commit.
- **Versions only increase.** When the bump level is unclear, PATCH.
- If a step's owning skill is not installed, its trigger phrase still names the standard — apply it
  inline rather than skipping the step.
