# Agent Skills Repo

Plugin repo for the `ceh-*` Claude Code plugins — engineering standards delivered as skills.
Each plugin is a standalone, self-contained **use case** (see Organizing Principle below).

## Organizing Principle

Plugins are split on a single axis: **use case** — load exactly the plugins that match what you are
building. This replaced an earlier mixed axis (tech-domain + lifecycle-phase) that baked in a
fullstack-web assumption and forced the same standard into multiple plugins where copies drifted.
The full rationale and migration record live in `.agents_workspace/PLUGIN_REORG_PLAN.md`.

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
| **Cross-cutting** | most sessions | `ceh-agent-coding-contract`, `ceh-git-workflow`, `ceh-fabled`, `ceh-advisor`, `ceh-testing` |
| **Use-case workflow** | per activity | `ceh-plan-build-review`, `ceh-blog`, `ceh-business-plan`, `ceh-evaluation`, `ceh-documentation`, `ceh-seo`, `ceh-ops`, `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-scaffolding`, `ceh-orchestration`, `ceh-release-flow` |
| **Stack / build** | per project type | `ceh-python-service`, `ceh-python-library`, `ceh-web-frontend`, `ceh-architecture` |

`ceh-dev-tools` is a standalone tooling plugin. Categorization rules of thumb:

- **Framework variants do not split into separate plugins** when their skills trigger on disjoint
  file types (e.g. `sveltekit` on `.svelte`, `react-vite` on `.tsx` both live in `ceh-web-frontend`).
  Splitting would duplicate the shared standards (a11y, TS style, testing) and reintroduce drift.
  Apply the "split only when too big" rule later if a framework's skills bloat the plugin.
- **A foundational standard needed by more than one use-case plugin is duplicated into each**, not
  extracted into a shared base plugin — see the Shared-Standards Duplication Policy below.
- **App-specific patterns are not standards.** Anything bound to one application's schema or design
  is removed rather than kept as a niche plugin.
- **Technique may split from tooling when the technique is genuinely stack-agnostic.** `ceh-testing`
  is the one deviation from the use-case-only axis: choosing test inputs, auditing whether a green
  suite catches defects, and proving a refactor changed nothing are identical in Python and
  TypeScript, while the runner, fixtures, and mocking library are not. Duplicating the technique
  into `ceh-python-service`, `ceh-python-library`, and `ceh-web-frontend` would have created three
  copies of the same standard with nothing stack-specific to justify the divergence — the exact
  drift the duplication policy is willing to pay for only when the copies actually differ. The three
  stack testing skills keep the runner/fixtures/mocking; `ceh-testing` is loaded alongside them.
  Reconsider this if a technique skill ever grows stack-specific branches.

## Structure

```
.agents_workspace/            # Skill session artifacts (DECISION_LOG.md, LESSONS_LEARNED.md, ARCHITECTURE.md), plugin reorg plan, architecture docs, etc. — not a plugin
.claude-plugin/               # Marketplace manifest (marketplace.json)
ceh-<plugin-name>/
├── .claude-plugin/           # Plugin manifest (plugin.json) — version lives here
├── agents/                   # Optional — subagents for complex autonomous tasks
├── hooks/                    # Optional — hooks.json wiring hook scripts via ${CLAUDE_PLUGIN_ROOT} (e.g. ceh-advisor)
├── scripts/                  # Optional — shell helpers and hook scripts (e.g. coverage, branch delete)
└── skills/
    └── <skill-name>/
        ├── SKILL.md               # Required — all content inline; frontmatter + full body
        └── references/            # Sparingly — schemas and templates only (e.g. plan-schema.md)
tools/                         # Standalone meta-tooling, not itself a plugin/skill/agent
└── <tool-name>/               # e.g. skills-sync — own README.md, no plugin.json
```

## Plugins

| Plugin directory | Domain |
|-----------------|--------|
| `ceh-agent-coding-contract` | Behavioral contract for coding agents; write-less-code minimalism reflex; retroactive refactoring (`shrink-diff` on a branch's diff, `refactor-repo` campaign-wide); usage-limit guard hook + stop-and-summarize handoff (`usage-limit-handoff`) |
| `ceh-plan-build-review` | Plan-driven development loop: plan a fullstack app (iteratively or to MVP), implement from the plan, review against it, patch a shipped version with small non-feature changes |
| `ceh-architecture` | Stack-agnostic design: living architecture docs (Mermaid diagrams + Key Decisions), domain modeling |
| `ceh-python-service` | FastAPI, asyncpg, PostgreSQL, Alembic, uv, testing, observability, security |
| `ceh-python-library` | Packaging, public API, semver, uv, testing (no web deps) |
| `ceh-web-frontend` | SvelteKit + React (Vite), Bun, TS style, Vitest, Playwright, accessibility |
| `ceh-scaffolding` | Per-project-type setup: directory layout + config + .gitignore |
| `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review |
| `ceh-ops` | Deploy pipeline, incidents, rollback; CI agents |
| `ceh-seo` | SEO/GEO discoverability for anything internet-exposed: public web pages (meta, structured data, sitemap, llms.txt, rendering) and public-facing text (README first screen, package descriptions, repo topics) |
| `ceh-summarize-chat` | Session summary for LLM handoff |
| `ceh-lessons-learned` | Session retrospectives |
| `ceh-dev-tools` | Repository exploration and codebase orientation: `explain-codebase` writes a component-level explanation of a whole repo into a git-ignored `.agents_workspace/CODEBASE_EXPLAINED.md`; the `repo-tree-mapper` agent writes an annotated structure map |
| `ceh-blog` | Interview-driven blog post writing |
| `ceh-documentation` | User guides, operator runbooks, install/config and troubleshooting docs; changelog & README maintenance |
| `ceh-orchestration` | Thin-orchestrator mode: plan/delegate-only main session + executor/verifier subagents (and the built-in Explore agent) for cost-optimized multi-step work |
| `ceh-release-flow` | End-to-end release orchestration: sequences version bump, changelog, README, CLAUDE.md, PR, merge, tag, and release by delegating to the skill that owns each step |
| `ceh-business-plan` | Interview-driven business plan: draft from an app plan or product idea, then loop interview/revise until a product-market-fit readiness gate passes |
| `ceh-evaluation` | Evaluate a skill/plugin you wrote: derive its own criteria, measure structure/triggering/content/behavioral lift with evidence, loop fix/re-run until a readiness gate passes; skill-creator and plugin-dev are optional cross-checks only |
| `ceh-fabled` | Frontier-grade reasoning discipline for any non-trivial task: deliberate thinking, alternative generation, adversarial self-review, verification, calibrated conviction; plus plan review against that standard, failure-loop escape after repeated failed fixes, and `fabled-voice` for delivering in fable's response style (form only, always-on via SessionStart hook) |
| `ceh-advisor` | Stronger-model second-opinion subagent (agent + hooks, no skills): consulted at decision points, failure loops, irreversible actions, and pre-completion gates; ships a destructive-command guard and a consecutive-failure watch hook |
| `ceh-testing` | Stack-agnostic testing *technique* (not tooling): reproduce-first bug fixes, test-case design (partitions, boundaries, decision tables, pairwise, properties), suite audits (assertions, mutation, flakiness), behavior-preservation for refactors, and a pre-completion risk gate (concurrency, contract drift, perf, authz) |

## Skills

Each skill is a self-contained SKILL.md file with frontmatter and inline content. The
`references/` subdirectory is reserved for schemas and templates shared across multiple skills
(e.g. `plan-schema.md` in `implement-from-plan`) — not for general reference material.

## Frontmatter Conventions

**`description` is always a folded block scalar (`>-`), never quoted and never plain.** Enforced
by `validate.py`.

```yaml
---
name: my-skill
description: >-
  Load this skill when doing X: the colon here is literal, as are "quotes",
  'apostrophes', backslashes and # hashes. Wrap at ~98 chars, 2-space indent.
---
```

`>-` is the only style with **no escaping burden** — every character is literal inside the block,
and `-` strips the trailing newline so the value has no stray `\n`. The alternatives each have a
rule that has already broken files here: a plain scalar cannot contain `: ` (strict YAML reads it
as a nested mapping), single-quoted needs `''` doubling, double-quoted needs `\` and `"` escaping.
Descriptions in this repo run 500–1000 characters, so the block form is also the readable one.

Two mechanical rules keep folding lossless: **uniform 2-space indent** on every continuation line
(a more-indented line suppresses folding and becomes a literal newline), and **no blank lines**
inside the block. Folding joins lines with a single space, so never rely on a double space.

Every **other** frontmatter key that contains `: ` must be quoted — single quotes are the default
(`argument-hint: '[plan-file]'`). Short values that need no quoting stay bare (`effort: max`).

## Adding a Component

The repo-local skill `.claude/skills/add-plugin-component/` carries the full checklist for both
of the sections below — plugin choice, frontmatter fields worth reaching for (and their traps),
both README tables, `CROSS_REFERENCES.md`, the two-manifest version bump, and the validator. It
auto-loads when a `SKILL.md` or `agents/*.md` is being created. The condensed versions follow.

## Adding an Agent

1. Identify the correct plugin for the agent's domain.
2. Create `ceh-<plugin>/agents/<name>.md` with frontmatter `name`, `description`, and `tools` fields.
3. Update `README.md` agents tables:
   - Add a row under the correct plugin group in the "Agents" section.
   - If the plugin has no agents group yet, add a new `### <Plugin> (`ceh-<plugin>`)` subsection.
4. Bump version in both:
   - `ceh-<plugin>/.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`
5. Validate before committing: `python tools/validate-plugins/validate.py`
   (checks manifest/marketplace sync, semver, and skill/agent frontmatter — the same
   gate CI runs via `.github/workflows/validate.yml`).

> **Plugin-agent frontmatter gotcha:** Claude Code ignores `permissionMode`, `hooks`, and
> `mcpServers` on plugin subagents (security restriction — see the
> [subagents docs](https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope)).
> Every agent in this repo is a plugin agent, so these fields are never set here — do not
> add them back. To avoid edit prompts, put the session in `acceptEdits` before dispatching
> (a parent `acceptEdits`/`bypassPermissions` takes precedence and is inherited) or use
> `permissions.allow` in `settings.json`. Required fields are only `name` and `description`;
> `model` defaults to `inherit`. Auto-delegation is driven by the `description` field —
> include "use proactively" to encourage it.
>
> **Background tool filter:** subagents run in the background by default, and a background
> subagent keeps only these built-in tools — `Read`, `Grep`, `Glob`, `Bash`, `PowerShell`,
> `Edit`, `Write`, `NotebookEdit`, `WebFetch`, `WebSearch`, `TodoWrite`, `Skill`,
> `ToolSearch`, `EnterWorktree`, `ExitWorktree`, `Monitor`, `TaskStop`, `SendMessage`,
> `Artifact`. Everything else is stripped whether inherited or named in `tools:`, and the
> removal is silent. Check any new agent's `tools:` against that list. `AskUserQuestion` is
> removed from *every* subagent, foreground or background — an agent can never stop to ask.
>
> **`isolation: worktree` is deliberately unused.** Subagent worktrees branch from the
> repository's **default branch**, not the parent session's `HEAD`, unless
> `worktree.baseRef: "head"` is set in `settings.json` — and their changes stay in the
> worktree rather than landing in your checkout. With this repo's feature-branch rule that
> would hand an agent a copy of `main` without your work, so no agent sets it.
>
> **Preloading skills into an agent:** the `skills:` frontmatter list loads a skill into the
> agent's context at dispatch — the agent does **not** need the `Skill` tool for this, and
> `SessionStart` hooks never fire for subagents, so `skills:` is the only way a hook-loaded
> standard reaches one. Always write entries fully qualified as `plugin:skill`; a bare skill
> name may resolve to nothing and the preload fails silently.

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
6. Validate before committing: `python tools/validate-plugins/validate.py`
   (checks manifest/marketplace sync, semver, and skill/agent frontmatter — the same
   gate CI runs via `.github/workflows/validate.yml`).

## Commands

```bash
# List all skills in a plugin
ls ceh-<plugin>/skills/

# Find a skill by name across all plugins
find . -path '*skills/<name>/SKILL.md'

# Verify every plugin is listed in marketplace.json
grep '"name"' ceh-*/.claude-plugin/plugin.json .claude-plugin/marketplace.json

# Validate the whole repo (manifests, skills, agents, references, scripts) — CI runs this too
python tools/validate-plugins/validate.py
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
