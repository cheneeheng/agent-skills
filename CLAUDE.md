# Agent Skills Repo

Plugin repo for the `ceh-*` Claude Code plugins — engineering standards delivered as skills.
Each plugin is a standalone, self-contained **use case** (see Organizing Principle below).

## Organizing Principle

Plugins are split on a single axis: **use case** — load exactly the plugins that match what you are
building. This replaced an earlier mixed axis (tech-domain + lifecycle-phase) that baked in a
fullstack-web assumption and forced the same standard into multiple plugins where copies drifted.
The full rationale and migration record live in `docs/PLUGIN_REORG_PLAN.md`.

Two consequences drive how skills are written and where they live:

- **Skills trigger on moments, not topics.** A skill fires on a verb/moment ("I'm opening a PR",
  "I'm writing a migration"), not a noun/topic ("PostgreSQL"). Topic-named skills either never
  auto-trigger or restate what the model already knows, so each skill is cut to the
  repo-opinionated delta and framed as a moment.
- **Plugin names declare their scope.** `ceh-python-service` vs `ceh-python-library`,
  `ceh-web-frontend`, etc. — the name states the use case, which removes the silent
  "fullstack-web-only" assumption and makes gaps obvious.

Plugins fall into three tiers:

| Tier | Loaded | Plugins |
|------|--------|---------|
| **Cross-cutting** | most sessions | `ceh-agent-coding-contract`, `ceh-git-workflow` |
| **Use-case workflow** | per activity | `ceh-plan-build-review`, `ceh-blog`, `ceh-documentation`, `ceh-ops`, `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-scaffolding` |
| **Stack / build** | per project type | `ceh-python-service`, `ceh-python-library`, `ceh-web-frontend`, `ceh-architecture` |

`ceh-dev-tools` is a standalone tooling plugin (agents only). Categorization rules of thumb:

- **Framework variants do not split into separate plugins** when their skills trigger on disjoint
  file types (e.g. `sveltekit` on `.svelte`, `react-vite` on `.tsx` both live in `ceh-web-frontend`).
  Splitting would duplicate the shared standards (a11y, TS style, testing) and reintroduce drift.
  Apply the "split only when too big" rule later if a framework's skills bloat the plugin.
- **A foundational standard needed by more than one use-case plugin is duplicated into each**, not
  extracted into a shared base plugin — see the Shared-Standards Duplication Policy below.
- **App-specific patterns are not standards.** Anything bound to one application's schema or design
  is removed rather than kept as a niche plugin.

## Structure

```
.claude-plugin/               # Marketplace manifest (marketplace.json)
ceh-<plugin-name>/
├── .claude-plugin/           # Plugin manifest (plugin.json) — version lives here
├── agents/                   # Optional — subagents for complex autonomous tasks
├── scripts/                  # Optional — shell helpers (e.g. coverage, branch delete)
└── skills/
    └── <skill-name>/
        ├── SKILL.md               # Required — all content inline; frontmatter + full body
        └── references/            # Sparingly — schemas and templates only (e.g. plan-schema.md)
docs/                          # Plugin reorg plan, decision log, etc. — not a plugin
tools/                         # Standalone meta-tooling, not itself a plugin/skill/agent
└── <tool-name>/               # e.g. skills-sync — own README.md, no plugin.json
```

## Plugins

| Plugin directory | Domain |
|-----------------|--------|
| `ceh-agent-coding-contract` | Behavioral contract for coding agents |
| `ceh-plan-build-review` | Plan-driven development loop: plan a fullstack app (iteratively or to MVP), implement from the plan, review against it |
| `ceh-architecture` | Stack-agnostic design: ADRs, domain modeling |
| `ceh-python-service` | FastAPI, asyncpg, PostgreSQL, Alembic, uv, testing, observability, security |
| `ceh-python-library` | Packaging, public API, semver, uv, testing (no web deps) |
| `ceh-web-frontend` | SvelteKit + React (Vite), Bun, TS style, Vitest, Playwright, accessibility |
| `ceh-scaffolding` | Per-project-type setup: directory layout + config + .gitignore |
| `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review |
| `ceh-ops` | Deploy pipeline, incidents, rollback; CI agents |
| `ceh-summarize-chat` | Session summary for LLM handoff |
| `ceh-lessons-learned` | Session retrospectives |
| `ceh-dev-tools` | Repository exploration and codebase orientation agents (agents only — no skills) |
| `ceh-blog` | Interview-driven blog post writing |
| `ceh-documentation` | User guides, operator runbooks, install/config and troubleshooting docs; changelog & README agents |

## Skills

Each skill is a self-contained SKILL.md file with frontmatter and inline content. The
`references/` subdirectory is reserved for schemas and templates shared across multiple skills
(e.g. `plan-schema.md` in `implement-from-plan`) — not for general reference material.

## Adding an Agent

1. Identify the correct plugin for the agent's domain.
2. Create `ceh-<plugin>/agents/<name>.md` with frontmatter `name`, `description`, and `tools` fields.
3. Update `README.md` agents tables:
   - Add a row under the correct plugin group in the "Agents" section.
   - If the plugin has no agents group yet, add a new `### <Plugin> (`ceh-<plugin>`)` subsection.
4. Bump version in both:
   - `ceh-<plugin>/.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`

> **Plugin-agent frontmatter gotcha:** Claude Code ignores `permissionMode`, `hooks`, and
> `mcpServers` on plugin subagents (security restriction — see the
> [subagents docs](https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope)).
> Every agent in this repo is a plugin agent, so `permissionMode: acceptEdits` is a no-op —
> do not rely on it. To grant edit/write permissions, use session `permissions.allow` in
> `settings.json`. Required fields are only `name` and `description`; `model` defaults to
> `inherit`. Auto-delegation is driven by the `description` field — include "use proactively"
> to encourage it.

## Adding a Skill

1. Identify the correct plugin for the skill's domain.
2. Create `ceh-<plugin>/skills/<name>/SKILL.md` with frontmatter `name` and `description` fields.
3. Write all content inline in the SKILL.md body — no separate reference files unless it is a
   schema or template shared across multiple skills (e.g. a plan document schema).
4. Update `README.md` skills tables:
   - Add a row under the correct plugin group in the "Skills" section of the root README.
   - Add a row to the plugin's own README.md skills table.
5. Bump version in both:
   - `ceh-<plugin>/.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`

## Commands

```bash
# List all skills in a plugin
ls ceh-<plugin>/skills/

# Find a skill by name across all plugins
find . -path '*skills/<name>/SKILL.md'

# Verify every plugin is listed in marketplace.json
grep '"name"' ceh-*/.claude-plugin/plugin.json .claude-plugin/marketplace.json
```

## Versioning

This repo has two independent versioning layers:

**Per-plugin versions** (load-bearing for auto-update):
- Live in `ceh-<plugin>/.claude-plugin/plugin.json` and mirrored in `.claude-plugin/marketplace.json`.
- Follow semver: **PATCH** for content/description updates, **MINOR** for new skills or agents.
- Bump only at commit time — not during iterative edits within a session.
- Both `plugin.json` and `marketplace.json` must be bumped in the same commit.

**Repo git tag** (mono-repo release snapshot):
- A single tag (e.g. `v2.3.0`) marks a consistent state of all plugins together.
- Increments sequentially from the previous repo tag — MINOR bump when any plugin adds skills or agents, PATCH bump for content-only changes. Independent of individual plugin versions.
- Purpose: deployment snapshot and changelog anchor. It does not drive auto-update.
- Cut a new tag after bumping plugin versions: `git tag vX.Y.Z && git push origin vX.Y.Z`.

Current plugin versions: check `ceh-<plugin>/.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json`.

## Key Files

| File | Purpose |
|------|---------|
| `ceh-<plugin>/.claude-plugin/plugin.json` | Plugin version and metadata |
| `.claude-plugin/marketplace.json` | Marketplace listing (all plugins) |
| `README.md` | User-facing docs — skill and agent tables live here |
| `CROSS_REFERENCES.md` | Tracks content duplicated across skills; lists canonical source and all copies per block |

## Cross-Reference Rule

Before editing any skill, check `CROSS_REFERENCES.md`. If the section you are changing appears
in that file, propagate the edit to every other listed file in the same session. Edit the
canonical file first, then mirror the change to all copies. If you add new duplication, add an
entry to `CROSS_REFERENCES.md`.

## Shared-Standards Duplication Policy

Plugins are organized around **use cases**, and each use-case plugin must be self-contained so a
user loads exactly one plugin per use case. When a foundational standard is needed by more than
one use-case plugin, **duplicate the delta into each plugin** rather than extracting a shared base
plugin.

Canonical case: the Python foundation (uv/pyproject/ruff/mypy environment + pytest testing) is
duplicated into both `ceh-python-service` and `ceh-python-library`. The library copy drops
web-only dependencies (`fastapi`, `uvicorn`, `asyncpg`) and the uvicorn dev-server command.

Cost of this choice is drift between copies; the required mitigation is to register every
duplicated block in `CROSS_REFERENCES.md` and propagate edits in the same session (see the
Cross-Reference Rule above).
