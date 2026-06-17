---
name: "merge"
description: "Load when merging a pull request and cleaning up after, any phrasing — merge/land/integrate a PR or branch, 'merge it', 'merge and delete the branch', 'clean up the branch'. Also the merge half of compound requests like 'create a PR, merge it, delete the branch'. Covers the pre-merge gate (CI green, approvals, rebased, clean history), merge-commit strategy (no squash/rebase-merge), and post-merge cleanup (delete remote + local branch, return to main, pull)."
---

# Merging a Pull Request

Owns the merge and cleanup moment. To author the PR first, say "open a PR".

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
  otherwise edit the message in the GitHub merge dialog before confirming.

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

## Post-Merge Cleanup

```bash
gh pr merge <number> --merge --delete-branch   # merge commit + delete remote & local tracking branch
git checkout main && git pull origin main      # return to main and sync
git branch -d <branch-name>                    # only if a local copy lingers (e.g. merged via UI)
git fetch --prune                              # drop stale remote-tracking refs
```

`git branch -d` (lowercase) refuses an unmerged branch — do not force with `-D` unless you intend
to discard unmerged commits.

For "create a PR, merge it, delete the branch": open the PR, wait for the gate to pass, then run
the cleanup above. Never merge before CI finishes — surface it and wait rather than merging red.
