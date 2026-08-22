# ceh-release-flow

Orchestrate a complete project release in one pass. One skill sequences the steps that ship a
release — version bump, changelog, README, CLAUDE.md, PR, merge, tag, GitHub release — and gates
each step on the previous one.

It composes the skills that already own each step rather than reimplementing them, so there is no
duplicated standard to drift. Its only original content is the **sequencing** and the one rule none
of the individual skills own: the version bump lands through a **reviewed PR**, and the tag +
release happen **only after merge, on `main`, pointing at the merge commit**.

## Skill

### `release-flow`

Runs the release pipeline top to bottom, delegating each step:

| Step | Delegated to |
|------|--------------|
| Decide the semver bump | `ceh-git-workflow:release` |
| Branch from `main` | `ceh-git-workflow:branch` |
| Bump every manifest | mechanical edit |
| Changelog entry | `ceh-documentation:update-changelog` |
| README refresh | `ceh-documentation:update-readme` |
| CLAUDE.md update | surgical edit (or `revise-claude-md` if installed) |
| Commit the bump + docs | `ceh-git-workflow:commit` |
| Open the PR | `ceh-git-workflow:open-pr` |
| Merge + delete branch | `ceh-git-workflow:merge` |
| Tag + publish release | `ceh-git-workflow:release` |

**Invoke:** `@"ceh-release-flow:release-flow (agent)"`

**Auto-triggers on:** "run the release flow", "do the full release", "ship this release end to
end", "release this project", "bump version, update docs, open a PR, merge, tag and release".

### `direct-release-flow`

The PR-less variant — same pipeline directly on `main`, with no branch, PR, or merge:

| Step | Delegated to |
|------|--------------|
| Decide the semver bump | `ceh-git-workflow:release` |
| Confirm up-to-date `main` | `git pull origin main` |
| Bump every manifest | mechanical edit |
| Changelog entry | `ceh-documentation:update-changelog` |
| README refresh | `ceh-documentation:update-readme` |
| CLAUDE.md update | surgical edit (or `revise-claude-md` if installed) |
| Commit the bump + docs to `main` | `ceh-git-workflow:commit` |
| Tag + publish release | `ceh-git-workflow:release` |

**Invoke:** `@"ceh-release-flow:direct-release-flow (agent)"`

**Auto-triggers on:** "run the release flow without a PR", "do the full release directly on main",
"release this project without opening a PR", "cut a release without a PR".

## Dependencies

`ceh-git-workflow` and `ceh-documentation` are declared `dependencies` in this plugin's manifest,
so installing `ceh-release-flow` installs both. Each step below is invoked directly by name — the
flow does not rely on a trigger phrase matching.

| Skill | Plugin | Used by |
|-------|--------|---------|
| `release` | `ceh-git-workflow` | both (semver bump, tag + release) |
| `branch` | `ceh-git-workflow` | `release-flow` only |
| `commit` | `ceh-git-workflow` | both |
| `open-pr` | `ceh-git-workflow` | `release-flow` only |
| `merge` | `ceh-git-workflow` | `release-flow` only |
| `update-changelog` | `ceh-documentation` | both |
| `update-readme` | `ceh-documentation` | both |
| `revise-claude-md` | `claude-md-management` | both (optional — CLAUDE.md refresh) |

`revise-claude-md` is the one exception: it lives in another marketplace, which plugin
dependencies cannot reach, so step 6 still falls back to a surgical inline edit.

Disabling `ceh-git-workflow` or `ceh-documentation` while `ceh-release-flow` is enabled is refused
by the plugin system, which is the point: the step tables call those skills unconditionally.

## Installation

```
/plugin install ceh-release-flow@ceh-plugins --scope user
```

Or manually in `~/.claude/settings.json`:

```json
{ "plugins": [{ "path": "~/agent-skills/plugins/ceh-release-flow" }] }
```
