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

**Invoke:** `/ceh-release-flow:release-flow`

**Auto-triggers on:** "run the release flow", "do the full release", "ship this release end to
end", "release this project", "bump version, update docs, open a PR, merge, tag and release".

Each delegated step is named by trigger phrase as well as by skill, so the flow degrades
gracefully when a referenced plugin is not installed — the phrase still names the standard to
apply inline.

## Installation

```
/plugin install ceh-release-flow@ceh-plugins --scope user
```

Or manually in `~/.claude/settings.json`:

```json
{ "plugins": [{ "path": "~/agent-skills/ceh-release-flow" }] }
```
