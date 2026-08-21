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

Each delegated step is named by trigger phrase as well as by skill, so the flow degrades
gracefully when a referenced plugin is not installed — the phrase still names the standard to
apply inline.

## Dependencies

Both skills delegate to the following skills from other CEH plugins. Install them for the full
experience:

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

**Fallback when a dependency is not installed:** these are soft dependencies, not hard requirements.
Each step is named by its trigger phrase as well as by its owning skill, so if a referenced plugin
is missing the flow does **not** skip the step — it falls back to applying that step's standard
inline (e.g. it bumps versions, writes the changelog, or tags the release directly) instead of
delegating. The `revise-claude-md` step always falls back to a surgical inline edit.

## Installation

```
/plugin install ceh-release-flow@ceh-plugins --scope user
```

Or manually in `~/.claude/settings.json`:

```json
{ "plugins": [{ "path": "~/agent-skills/plugins/ceh-release-flow" }] }
```
