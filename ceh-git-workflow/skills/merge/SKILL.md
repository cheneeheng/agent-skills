---
name: merge
description: >-
  Load when merging and cleaning up after, any phrasing — merge/land/integrate a PR or a local
  branch, 'merge it', 'merge and delete the branch', 'clean up the branch', 'merge this branch into
  main'. Also the merge half of compound requests like 'create a PR, merge it, delete the branch'.
  Covers both the PR-merge case (gh pr merge, including auto-merge) and the local no-PR branch-merge
  case (git merge --no-ff into main), the pre-merge gate (CI green, approvals, rebased, clean
  history), merge-commit strategy (no squash/rebase-merge), and post-merge cleanup (delete remote +
  local branch, return to main, pull).
---

# Merging

Owns the merge and cleanup moment for two cases:

- **PR merge** — landing a pull request through GitHub (immediately, or queued via auto-merge).
  To author the PR first, say "open a PR". On repos that allow auto-merge, `open-pr` already queues
  the merge at PR-creation time — use this skill when you want to merge *now*, or to queue a PR on a
  repo where it wasn't enabled at creation.
- **Local branch merge** — integrating a local feature branch into `main` with no PR (solo repos,
  low-risk work, or the no-PR variant of the release flow). See "Local Branch Merge" below.

Both cases share the same merge-commit strategy and post-merge cleanup; the pre-merge gate applies
to whichever signals exist (CI/approvals only apply when the branch is on a remote with them).

## Pre-Merge Gate

Do not merge until all hold:

- [ ] All CI checks pass — never merge red, never bypass CI
- [ ] Required approvals met (1 for bug fixes / small features; 2 for new API surfaces, schema, or security)
- [ ] Rebased on latest `main`
- [ ] History clean — fixup/WIP/debug commits squashed or dropped; every commit Conventional Commits format

## Merge Strategy

**Merge commit only** — never squash, never rebase-merge. Commits land on `main` as written
(the per-PR history is kept on purpose as source material for write-ups), so clean the branch
first.

## Merge Commit Message

The merge commit is a real commit — give it a message that reads on its own in `git log main`,
not GitHub's default `Merge pull request #N from user/branch`.

```
Merge pull request #<N>: <type>(<scope>): <PR title>

<one line on what the PR delivers and why it's landing>
```

- Subject: reuse the PR's Conventional Commits title so `main`'s history stays scannable.
- Body: one or two lines of context — the "why", and anything a future bisect would want
  (e.g. "behind feature flag X", "requires migration 0042"). Skip if the PR title says it all.
- With the CLI, `gh pr merge <N> --merge --subject "..." --body "..."` sets it explicitly;
  otherwise edit the message in the GitHub merge dialog before confirming. If the body spans
  more than one line, write it to a temp file and pass `--body-file <file>` (then delete it)
  rather than an inline `--body` — the temp-file path avoids shell quoting and works the same
  in PowerShell and Bash.

## Resolving Conflicts

If the branch won't merge cleanly, rebase it on `main` and resolve there — never resolve inside
the merge commit:

```bash
git checkout <branch-name>
git fetch origin && git rebase origin/main
# resolve conflicts, then for each file:
git add <file> && git rebase --continue
git push --force-with-lease            # your own feature branch only
```

Re-run CI after the rebase; the pre-merge gate applies to the rebased state, not the pre-conflict one.

## PR Merge & Cleanup

Prefer `--auto` when the repo allows it: GitHub queues the merge and lands it the moment the gate
(CI + approvals, enforced server-side via branch protection) goes green, then deletes the branch.
Probe for support and fall back to a direct merge (which requires the gate already green):

```bash
if [ "$(gh api repos/{owner}/{repo} --jq .allow_auto_merge)" = "true" ]; then
  gh pr merge <number> --merge --auto --delete-branch   # queues; lands when the gate goes green
else
  gh pr merge <number> --merge --delete-branch          # gate must already be green
fi
git checkout main && git pull origin main   # return to main and sync
git branch -d <branch-name>                 # only if a local copy lingers (e.g. merged via UI)
git fetch --prune                           # drop stale remote-tracking refs
```

`git branch -d` (lowercase) refuses an unmerged branch — do not force with `-D` unless you intend
to discard unmerged commits. For "create a PR, merge it, delete the branch", chain this after the
PR opens. Never bypass CI — surface a red gate and wait rather than merging red.

## Local Branch Merge

When there is no PR — a local feature branch going straight into `main` (solo repos, low-risk work,
or the no-PR release flow) — merge with an explicit merge commit and clean up the same way. Still a
**merge commit only** (`--no-ff`); never fast-forward away the branch's history. Apply the pre-merge
gate to whatever signals exist: rebased on latest `main`, history clean, and any local checks
(tests, lint, type-check) green — there are no server-side CI/approval gates to lean on here.

```bash
git checkout <branch-name>
git fetch origin && git rebase origin/main   # rebase first so the merge is a clean fast-forward base
git checkout main && git pull origin main
git merge --no-ff <branch-name>              # explicit merge commit; reuse the Conventional Commits subject
git push origin main
git branch -d <branch-name>                  # lowercase: refuses if somehow unmerged
git push origin --delete <branch-name>       # only if the branch was ever pushed
```

Give the merge commit the same kind of message as the PR case — a Conventional Commits subject plus
a line of "why" — so `git log main` reads on its own. Never `--no-ff` past a failing local check;
fix it on the branch first.
