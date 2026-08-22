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
| **Cross-cutting** | most sessions | `ceh-coding-agent`, `ceh-git-workflow`, `ceh-fabled`, `ceh-advisor`, `ceh-testing` |
| **Use-case workflow** | per activity | `ceh-plan-build-review`, `ceh-blog`, `ceh-business-plan`, `ceh-evaluation`, `ceh-usability-audit`, `ceh-documentation`, `ceh-seo`, `ceh-ops`, `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-scaffolding`, `ceh-orchestration`, `ceh-release-flow` |
| **Stack / build** | per project type | `ceh-python-service`, `ceh-python-library`, `ceh-web-frontend`, `ceh-architecture` |

Categorization rules of thumb:

- **Framework variants do not split into separate plugins** when their skills trigger on disjoint
  file types (e.g. `sveltekit` on `.svelte`, `react-vite` on `.tsx` both live in `ceh-web-frontend`).
  Splitting would duplicate the shared standards (a11y, TS style, testing) and reintroduce drift.
  Apply the "split only when too big" rule later if a framework's skills bloat the plugin.
- **A foundational standard needed by more than one use-case plugin is duplicated into each**, not
  extracted into a shared base plugin — see the Shared-Standards Duplication Policy below.
- **App-specific patterns are not standards.** Anything bound to one application's schema or design
  is removed rather than kept as a niche plugin.
- **The use-case axis governs the use-case-workflow and stack/build tiers; the cross-cutting tier is
  orthogonal by construction.** A cross-cutting plugin holds a discipline that applies whatever you
  are building — agent behavior, git, reasoning, second opinions, testing technique — so it is
  loaded *alongside* a use-case plugin, never instead of one. That is not an exception to the axis;
  it is what the tier is for. `ceh-testing` sits there for exactly the reason `ceh-git-workflow`
  does: a Python service has commits and it has test design, and `ceh-python-service` owns neither.
- **Technique splits from tooling when the technique is genuinely stack-agnostic.** This is the test
  for putting a skill in a cross-cutting plugin rather than a stack one: **would the content be
  byte-identical across stacks?** Choosing test inputs, auditing whether a green suite catches
  defects, and proving a refactor changed nothing are identical in Python and TypeScript — so they
  live in `ceh-testing`. The runner, fixtures, mocking library, and coverage thresholds are not — so
  they stay in the three stack testing skills. Duplicating the technique into `ceh-python-service`,
  `ceh-python-library`, and `ceh-web-frontend` would have created three copies with nothing
  stack-specific to justify the divergence, which is the drift the duplication policy is willing to
  pay for only when the copies actually differ. Revisit the placement if a technique skill ever
  grows stack-specific branches — that is the signal it was tooling all along.

## Structure

```
.agents_workspace/            # Skill session artifacts — not a plugin. DECISION_LOG.md and PLUGIN_REORG_PLAN.md are tracked; skill-evals/<skill>/run-NNN/SKILL_EVAL.md holds ceh-evaluation output
.claude-plugin/               # Marketplace manifest (marketplace.json)
docs/                         # Maintainer docs — CROSS_REFERENCES.md, TESTING_WORKFLOW.md, CHANGELOG-v1-v2.md (pre-v3 releases)
plugins/                      # All plugins live here — flat, one directory per plugin, no tier subfolders
└── ceh-<plugin-name>/
    ├── .claude-plugin/           # Plugin manifest (plugin.json) — version lives here
    ├── agents/                   # Optional — subagents for complex autonomous tasks
    ├── hooks/                    # Optional — hooks.json wiring hook scripts via ${CLAUDE_PLUGIN_ROOT} (e.g. ceh-advisor)
    ├── scripts/                  # Optional — hook scripts and shell helpers (e.g. ceh-advisor guards, ceh-ops CI scaffolding, test/coverage runners)
    └── skills/
        └── <skill-name>/
            ├── SKILL.md               # Required — all content inline; frontmatter + full body
            └── references/            # Sparingly — shared schemas/templates (plan-schema.md) or a standards set too large to inline (fabled)
tools/                         # Standalone meta-tooling, not itself a plugin/skill/agent
└── <tool-name>/               # validate-plugins (the CI gate), skills-sync — own README.md, no plugin.json
```

## Plugins

| Plugin directory | Domain |
|-----------------|--------|
| `ceh-coding-agent` | Behavioral contract for coding agents; write-less-code minimalism reflex; retroactive refactoring (`shrink-diff` on a branch's diff, `refactor-repo` campaign-wide); usage-limit guard hook + stop-and-summarize handoff (`usage-limit-handoff`); explaining code to a person in-session until it lands (`explain-until-understood`); whole-repo orientation — `explain-codebase` writes a component-level explanation into a git-ignored `.agents_workspace/CODEBASE_EXPLAINED.md`, and the `repo-tree-mapper` agent writes an annotated structure map |
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
| `ceh-blog` | Interview-driven blog post writing |
| `ceh-documentation` | User guides, operator runbooks, install/config and troubleshooting docs; changelog & README maintenance |
| `ceh-orchestration` | Thin-orchestrator mode: plan/delegate-only main session + executor/verifier subagents (and the built-in Explore agent) for cost-optimized multi-step work |
| `ceh-release-flow` | End-to-end release orchestration: sequences version bump, changelog, README, CLAUDE.md, PR, merge, tag, and release by delegating to the skill that owns each step |
| `ceh-business-plan` | Interview-driven business plan: draft from an app plan or product idea, then loop interview/revise until a product-market-fit readiness gate passes |
| `ceh-evaluation` | Evaluate a skill/plugin you wrote: derive its own criteria, measure structure/triggering/content/behavioral lift with evidence, loop fix/re-run until a readiness gate passes; skill-creator and plugin-dev are optional cross-checks only |
| `ceh-fabled` | Frontier-grade reasoning discipline for any non-trivial task: deliberate thinking, alternative generation, adversarial self-review, verification, calibrated conviction; plus plan review against that standard, failure-loop escape after repeated failed fixes, and `fabled-voice` for delivering in fable's response style (form only, always-on via SessionStart hook) |
| `ceh-advisor` | Stronger-model second-opinion subagent (agent + hooks, no skills): consulted at decision points, failure loops, irreversible actions, and pre-completion gates; ships a destructive-command guard and a consecutive-failure watch hook |
| `ceh-usability-audit` | Whether a non-expert can actually use the thing: cold persona-constrained walkthroughs of first-run (`first-run-walkthrough`) and of an interface already entered (`audit-interface`), the three-part error-message rule (`audit-error-messages`), a plain-language pass over in-product copy (`plain-language-pass`), and the `novice-walker` agent they all dispatch. Owns the *comprehension* layer only — the WCAG floor stays in `ceh-web-frontend:accessibility`, build-time visual design in `ceh-web-frontend:ui-design` |
| `ceh-testing` | Stack-agnostic testing *technique* (not tooling): reproduce-first bug fixes and bisection, test-case design (partitions, boundaries, decision tables, pairwise, properties, metamorphic relations, fuzzing), suite audits (assertions, mutation, flakiness, branch coverage), behavior-preservation for refactors, and a pre-completion risk gate (concurrency, contract drift, perf, authz, migrations) |

## Skills

Each skill is a self-contained SKILL.md file with frontmatter and inline content. Default to
inlining everything; `references/` is for two cases only:

- **A schema or template used by several skills** — `plan-schema.md` is shared by
  `implement-from-plan`, `patch-built-version`, and `review-against-plan`.
- **A standards set too large to inline** without making SKILL.md unreadable — `ceh-fabled:fabled`
  splits six standards files out, `ceh-web-frontend:ui-design` keeps design-system examples there.

Never for general reference material a model already knows.

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

The repo-local skill `.claude/skills/add-plugin-component/` is the single checklist for adding or
changing a skill, agent, hook, or script — plugin choice, frontmatter fields worth reaching for
(and their traps), the plugin-agent gotchas, both README tables, `docs/CROSS_REFERENCES.md`, the
two-manifest version bump, and the validator. It auto-loads when a `SKILL.md` or `agents/*.md` is
being created; load it explicitly if it has not.

Whatever else gets skipped, these four land in the **same commit** or CI fails:

1. A row in the root `README.md` table (Skills or Agents).
2. A row in `plugins/ceh-<plugin>/README.md`.
3. A version bump in **both** `plugins/ceh-<plugin>/.claude-plugin/plugin.json` and
   `.claude-plugin/marketplace.json` — PATCH for content, MINOR for a new skill or agent.
4. `python tools/validate-plugins/validate.py` green.

## Commands

```bash
# List all skills in a plugin
ls plugins/ceh-<plugin>/skills/

# Find a skill by name across all plugins
find plugins -path '*skills/<name>/SKILL.md'

# Verify every plugin is listed in marketplace.json
grep '"name"' plugins/ceh-*/.claude-plugin/plugin.json .claude-plugin/marketplace.json

# Validate the whole repo (manifests, skills, agents, references, scripts) — CI runs this too
python tools/validate-plugins/validate.py
```

## Versioning

This repo has two independent versioning layers:

**Per-plugin versions** (load-bearing for auto-update):
- Live in `plugins/ceh-<plugin>/.claude-plugin/plugin.json` and mirrored in `.claude-plugin/marketplace.json`.
- Follow semver: **PATCH** for content/description updates, **MINOR** for new skills or agents.
- Bump only at commit time — not during iterative edits within a session.
- Both `plugin.json` and `marketplace.json` must be bumped in the same commit.

**Repo git tag** (mono-repo release snapshot):
- A single tag (e.g. `v2.3.0`) marks a consistent state of all plugins together.
- Increments sequentially from the previous repo tag — MINOR bump when any plugin adds skills or agents, PATCH bump for content-only changes. Independent of individual plugin versions.
- Purpose: deployment snapshot and changelog anchor. It does not drive auto-update.
- Cut a new tag after bumping plugin versions: `git tag vX.Y.Z && git push origin vX.Y.Z`.
- Add a `CHANGELOG.md` entry under the new version: prose on what changed and why, a
  `### Plugin versions` table listing every plugin bumped, then `### Added` / `### Changed` / `### Fixed`.

Current plugin versions: check `plugins/ceh-<plugin>/.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json`.

## Key Files

| File | Purpose |
|------|---------|
| `plugins/ceh-<plugin>/.claude-plugin/plugin.json` | Plugin version and metadata |
| `.claude-plugin/marketplace.json` | Marketplace listing (all plugins) |
| `README.md` | User-facing docs — skill and agent tables live here |
| `docs/CROSS_REFERENCES.md` | Tracks content duplicated across skills; lists canonical source and all copies per block |
| `CHANGELOG.md` | Release notes per repo tag; each entry carries a `### Plugin versions` table |
| `docs/CHANGELOG-v1-v2.md` | Release notes for v1.0.0–v2.8.0, before the v3.0.0 plugin reorganisation |
| `docs/TESTING_WORKFLOW.md` | Cross-plugin guide: how `ceh-testing`, the three stack testing skills, and the tester agents route between each other |
| `.agents_workspace/DECISION_LOG.md` | Agent decision log — **tracked in git here**, append-only, next sequential entry ID |

## Cross-Reference Rule

Before editing any skill, check `docs/CROSS_REFERENCES.md`. If the section you are changing appears
in that file, propagate the edit to every other listed file in the same session. Edit the
canonical file first, then mirror the change to all copies. If you add new duplication, add an
entry to `docs/CROSS_REFERENCES.md`.

## Shared-Standards Duplication Policy

Plugins are organized around **use cases**, and each use-case plugin must be self-contained so a
user loads exactly one plugin per use case. When a foundational standard is needed by more than
one use-case plugin, **duplicate the delta into each plugin** rather than extracting a shared base
plugin.

Canonical case: the Python foundation (uv/pyproject/ruff/mypy environment + pytest testing) is
duplicated into both `ceh-python-service` and `ceh-python-library`. The library copy drops
web-only dependencies (`fastapi`, `uvicorn`, `asyncpg`) and the uvicorn dev-server command.

Cost of this choice is drift between copies; the required mitigation is to register every
duplicated block in `docs/CROSS_REFERENCES.md` and propagate edits in the same session (see the
Cross-Reference Rule above).
