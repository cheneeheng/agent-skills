# Sunsetting agent-skills

**Status:** Sunset / archived — no longer maintained.
**Date:** 2026-10-02
**Final state:** Archived, as-is, at `v6.12.0`. The repo stays public and the `ceh-plugins`
marketplace stays installable, frozen at its current plugin versions. There will be no further
development, bug fixes, or compatibility updates. **Use at your own risk** — the plugins may break
with future versions of Claude Code.

**Successor:** [`cheneeheng/ceh-claude-code-library`](https://github.com/cheneeheng/ceh-claude-code-library).
All further work on the `ceh-*` plugins happens there.

This document records the decision to sunset agent-skills, the reason behind it, and where to go
instead.

## What agent-skills was

agent-skills is a Claude Code plugin marketplace (`ceh-plugins`) of engineering standards delivered
as skills, agents, and hooks. Its plugins are organized around **use cases** rather than
technologies: scenario bundles as install entry points, cross-cutting plugins for the coding
agent's own behavior and git workflow, use-case workflow plugins, and stack plugins for Python
services, Python libraries, and web frontends.

## Why sunset it

The project was not abandoned, it moved. The repo had grown past what it needed to be:

- **Too many plugins.** The marketplace had more plugins than anyone could keep in their head, which
  is why scenario bundles had to exist as an install entry point at all.
- **Too many dependencies.** Plugins depended on plugins, so installing one pulled in a closure of
  others.
- **Too many layers.** Four tiers, with bundles depending on bundles, sat between a user and the
  skill they wanted.
- **Too many experimental and unused plugins.** Several were never bundled or never reached for, and
  still had to be versioned, validated, and documented.

Migrating to [`ceh-claude-code-library`](https://github.com/cheneeheng/ceh-claude-code-library),
started on 2026-09-30, was the chance to clean all of that up instead of trimming it in place. It
was also an experiment in its own right: to see how much of a repo migration Claude could do on its
own.

Maintaining two copies of the same plugins would only let them drift, so this repo is frozen at its
last release and the successor carries the work forward.

## What changed in the successor

As of the sunset date, the successor is still marked work in progress. The differences visible
today:

- **A new marketplace name.** `ceh-plugins` becomes `ceh-claude-code-library`, so an install from
  this repo does not update itself to the new one. See the migration steps below.
- **Fewer scenario bundles.** The `-greenfield` / `-iterate` pairs collapse into one bundle per
  situation: `ceh-scenario-service`, `ceh-scenario-library`, `ceh-scenario-webapp`,
  `ceh-scenario-ideation`, `ceh-scenario-editorial`.
- **A `ceh-core` plugin.** The usage-limit handoff and the delegated bulk reads move out of
  `ceh-coding-agent` into `ceh-core`, and `update-readme` moves into `ceh-git-workflow`.
- **Date-named releases.** Repo releases are named `vYYYY.MM.DD`. Each plugin keeps its own
  semantic version.
- **Not every plugin is listed there.** `ceh-architecture`, `ceh-scaffolding`, `ceh-ops`,
  `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-orchestration`, `ceh-evaluation`, `ceh-fabled`,
  and `ceh-advisor` do not appear in the successor's plugin table as of the sunset date. They stay
  installable from this repo, frozen.

The successor's own README is the source of truth for its current contents.

## What to use instead

Switch the marketplace, then reinstall the bundle that matches your situation:

```
/plugin marketplace remove ceh-plugins
/plugin marketplace add cheneeheng/ceh-claude-code-library
/plugin install ceh-scenario-service@ceh-claude-code-library --scope user
```

Plugin names changed between the two repos, so pick the bundle from the successor's README rather
than reusing the name you had installed here.

## Thanks

This repo grew into a full marketplace across six major versions. It stops here in a clean,
released state, and the work continues next door.
