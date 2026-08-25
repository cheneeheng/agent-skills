# Agent Skills Repo

Plugin repo for the `ceh-*` Claude Code plugins — engineering standards delivered as skills.
Each plugin is a standalone, self-contained **use case**.

## Organizing Principle

Plugins split on one axis: **use case**. This replaced a mixed axis (tech-domain +
lifecycle-phase) that baked in a fullstack-web assumption and forced the same standard into several
plugins, where the copies drifted. Rationale: `.agents_workspace/PLUGIN_REORG_PLAN.md`.

Two consequences drive how skills are written and where they live:

- **Skills trigger on moments, not topics.** A skill fires on a verb ("I'm opening a PR"), not a
  noun ("PostgreSQL"). Topic-named skills either never auto-trigger or restate what the model
  already knows, so each skill is cut to the repo-opinionated delta.
- **Plugin names declare their scope.** `ceh-python-service` vs `ceh-python-library` — the name
  states the use case, which kills the silent "fullstack-web-only" assumption and makes gaps
  obvious.

Plugins fall into four tiers:

| Tier | Loaded | Plugins |
|------|--------|---------|
| **Scenario bundle** | one per situation | `ceh-scenario-{service,library,webapp}-{greenfield,iterate}`, `ceh-scenario-editorial` |
| **Cross-cutting** | most sessions | `ceh-coding-agent`, `ceh-git-workflow`, `ceh-testing`, plus `ceh-fabled` and `ceh-advisor` *(experimental — never bundled)* |
| **Use-case workflow** | per activity | `ceh-plan-build-review`, `ceh-blog`, `ceh-business-plan`, `ceh-evaluation`, `ceh-usability-audit`, `ceh-documentation`, `ceh-seo`, `ceh-ops`, `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-scaffolding`, `ceh-orchestration` *(experimental)*, `ceh-release-flow` |
| **Stack / build** | per project type | `ceh-python-service`, `ceh-python-library`, `ceh-web-frontend`, `ceh-architecture` |

The scenario tier is the install entry point, not a fourth axis: a bundle is a manifest with
`dependencies` and nothing else — no skills, agents, or hooks. `-greenfield` depends on its own
`-iterate` twin plus the planning delta, so the phase transition is a no-op. **Name the phase
halves `-greenfield` / `-iterate`, never `-maintenance`** — "maintenance" reads as bugfix-only and
already caused `ceh-plan-build-review` to be filed on the wrong side. Design record:
`.agents_workspace/PLUGIN_DEPENDENCY_PLAN.md`.

Categorization rules of thumb:

- **Framework variants do not split into separate plugins** when their skills trigger on disjoint
  file types (`sveltekit` on `.svelte`, `react-vite` on `.tsx`, both in `ceh-web-frontend`).
  Splitting duplicates the shared standards and reintroduces drift. Split later only if a
  framework's skills bloat the plugin.
- **A foundational standard needed by more than one use-case plugin is duplicated into each**, not
  extracted into a shared base plugin — see the Shared-Standards Duplication Policy below.
- **Scenario bundles live in `plugins/`** like everything else, with no `plugins-scenario/` folder.
  The `ceh-scenario-` prefix carries the distinction and `validate.py` enforces the structural
  invariant (manifest + README only).
- **App-specific patterns are not standards.** Anything bound to one application's schema or design
  is removed rather than kept as a niche plugin.
- **The cross-cutting tier is orthogonal by construction**, not an exception to the axis. It holds a
  discipline that applies whatever you are building, so it loads *alongside* a use-case plugin,
  never instead of one: a Python service has commits and it has test design, and
  `ceh-python-service` owns neither.
- **Technique splits from tooling when the technique is genuinely stack-agnostic.** The test:
  **would the content be byte-identical across stacks?** Choosing test inputs, auditing a green
  suite, and proving a refactor changed nothing are identical in Python and TypeScript, so they live
  in `ceh-testing`. The runner, fixtures, mocking library, and coverage thresholds are not, so they
  stay in the three stack testing skills. If a technique skill ever grows stack-specific branches,
  that is the signal it was tooling all along.

## Structure

```
.agents_workspace/            # Session artifacts — not a plugin. DECISION_LOG.md and the two PLUGIN_*_PLAN.md files are tracked; skill-evals/<skill>/run-NNN/SKILL_EVAL.md holds ceh-evaluation output
.claude-plugin/               # Marketplace manifest (marketplace.json)
docs/                         # Maintainer docs — CROSS_REFERENCES.md, TESTING_WORKFLOW.md, CHANGELOG-v1-v2.md
plugins/                      # All plugins live here — flat, one directory per plugin, no tier subfolders
├── ceh-scenario-<name>/      # Scenario bundle — .claude-plugin/plugin.json + README.md ONLY
└── ceh-<plugin-name>/
    ├── .claude-plugin/           # plugin.json — version and dependencies live here
    ├── agents/                   # Optional — subagents for complex autonomous tasks
    ├── hooks/                    # Optional — hooks.json wiring scripts via ${CLAUDE_PLUGIN_ROOT}
    ├── scripts/                  # Optional — hook scripts and shell helpers
    └── skills/
        └── <skill-name>/
            ├── SKILL.md               # Required — frontmatter + full body, all content inline
            └── references/            # Sparingly — see Skills below
tools/                         # Standalone meta-tooling, not itself a plugin/skill/agent
└── <tool-name>/               # validate-plugins (the CI gate), skills-sync — own README.md, no plugin.json
```

## Plugins

| Plugin directory | Domain |
|-----------------|--------|
| `ceh-coding-agent` | The coding agent's own behavior: contract + five-step workflow, write-less-code minimalism, retroactive refactoring (`shrink-diff`, `refactor-repo`), usage-limit guard + handoff, and whole-repo orientation (`explain-until-understood`, `explain-codebase`, `repo-tree-mapper`) |
| `ceh-plan-build-review` | Plan-driven loop: plan a fullstack app (iteratively or to MVP), implement from the plan, review against it, patch a shipped version |
| `ceh-architecture` | Stack-agnostic design: living architecture docs (3-second Overview + Mermaid + Key Decisions), domain modeling |
| `ceh-python-service` | FastAPI, asyncpg, PostgreSQL, Alembic, uv, testing, observability, security |
| `ceh-python-library` | Packaging, public API, semver, uv, testing (no web deps) |
| `ceh-web-frontend` | SvelteKit + React (Vite), Bun, TS style, Vitest, Playwright, accessibility, UI design |
| `ceh-scaffolding` | Per-project-type setup: directory layout + config + .gitignore |
| `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review, dependency management |
| `ceh-ops` | Deploy pipeline, incidents, rollback; CI agents |
| `ceh-seo` | SEO/GEO for anything internet-exposed: web pages (meta, structured data, sitemap, llms.txt) and public-facing text (README first screen, package descriptions, repo topics) |
| `ceh-summarize-chat` | Session summary for LLM handoff |
| `ceh-lessons-learned` | Session retrospectives |
| `ceh-blog` | Interview-driven blog post writing |
| `ceh-documentation` | User guides, operator runbooks, install/config and troubleshooting docs; changelog & README maintenance |
| `ceh-orchestration` | Thin-orchestrator mode: plan/delegate-only main session + executor/verifier subagents |
| `ceh-release-flow` | End-to-end release orchestration — sequences bump, changelog, README, CLAUDE.md, PR, merge, tag, release by invoking the skill that owns each step |
| `ceh-business-plan` | Interview-driven business plan: draft from an app plan or idea, loop until a product-market-fit gate passes |
| `ceh-evaluation` | Evaluate a skill/plugin you wrote: derive criteria, measure structure/triggering/content/behavioral lift with evidence, loop until a readiness gate passes |
| `ceh-fabled` | Frontier-grade reasoning discipline: deliberate thinking, alternative generation, adversarial self-review, verification, calibrated conviction; plus plan review, failure-loop escape, and `fabled-voice` (form only, always-on via SessionStart hook) |
| `ceh-advisor` | Stronger-model second-opinion subagent (agent + hooks, no skills) for decision points, failure loops, irreversible actions, pre-completion gates; ships a destructive-command guard and a failure-watch hook |
| `ceh-usability-audit` | Whether a non-expert can use the thing: cold persona walkthroughs of first-run and of an entered interface, the three-part error-message rule, a plain-language pass, and the `novice-walker` agent. Owns *comprehension* only — WCAG stays in `ceh-web-frontend:accessibility` |
| `ceh-testing` | Stack-agnostic testing *technique*: reproduce-first fixes and bisection, test-case design, suite audits (assertions, mutation, flakiness, coverage), behavior-preservation for refactors, and a pre-completion risk gate |

## Skills

Each skill is a self-contained SKILL.md with frontmatter and inline content. Default to inlining;
`references/` is for two cases only:

- **A schema or template used by several skills** — `plan-schema.md` has four consumer copies:
  `implement-from-plan`, `review-against-plan`, `patch-built-version`, and — the only cross-plugin
  one — `ceh-business-plan:develop-business-plan`. All four are word-for-word identical.
- **A standards set too large to inline** — `ceh-fabled:fabled` splits six standards files out;
  `ceh-web-frontend:ui-design` keeps design-system examples there.

Never for general reference material a model already knows.

## Frontmatter Conventions

**`description` is always a folded block scalar (`>-`), never quoted and never plain.** Enforced by
`validate.py`.

```yaml
---
name: my-skill
description: >-
  Load this skill when doing X: the colon here is literal, as are "quotes",
  'apostrophes', backslashes and # hashes. Wrap at ~98 chars, 2-space indent.
---
```

`>-` is the only style with **no escaping burden**: every character is literal, and `-` strips the
trailing newline. Each alternative has a rule that has already broken files here — a plain scalar
cannot contain `: `, single-quoted needs `''` doubling, double-quoted needs `\` and `"` escaping.

Two mechanical rules keep folding lossless: **uniform 2-space indent** on every continuation line (a
more-indented line becomes a literal newline instead) and **no blank lines** inside the block.
Folding joins lines with one space, so never rely on a double space.

Every **other** frontmatter key containing `: ` must be quoted — single quotes by default
(`argument-hint: '[plan-file]'`). Short values that need no quoting stay bare (`effort: max`).

## Plugin Dependencies

**Declare `dependencies` in `plugin.json` only, never in the `marketplace.json` entry.** The
platform accepts either, with no documented precedence when both are set — one source of truth, and
`marketplace.json` mirrors only version and description. Bare strings, no version ranges (the repo
has no per-plugin `{name}--v{version}` tags).

Dependencies install and enable automatically and transitively. There is **no optional dependency**,
and `defaultEnabled: false` does not protect one.

Two rules decide whether a cross-plugin reference earns a dependency:

- **It must fire on every run of the skill.** A conditional handoff — `ceh-usability-audit`
  delegating WCAG to `ceh-web-frontend:accessibility` only when the subject has a UI — stays prose.
  Declaring it installs a whole plugin for a branch most runs never reach.
- **Negative routing never counts.** `Not for tagging, use ceh-git-workflow:release` names an
  *alternative*; a dependency there installs what the user steered away from.

**A cross-cutting plugin may depend only on other cross-cutting plugins.** This keeps the graph
layered; `validate.py` checks acyclicity directly rather than relying on the rule to imply it.

Where a dependency exists, the referencing skill body calls the target **explicitly** —
`Invoke the Skill tool with skill="ceh-testing:design-test-cases"` — instead of naming a trigger
phrase and hoping the description matches. `validate.py` rejects such a call if the target does not
resolve, is not in a declared dependency, or sets `disable-model-invocation: true` (6 of 77 skills
do, and the resulting failed call is silent).

Do not convert every backtick-quoted skill name into an invocation: most references are advisory,
and a sweep would pull a 6-plugin closure into a single install.

## Adding a Component

The repo-local skill `.claude/skills/add-plugin-component/` is the single checklist for adding or
changing a skill, agent, hook, or script — plugin choice, frontmatter traps, plugin-agent gotchas,
both README tables, `docs/CROSS_REFERENCES.md`, the two-manifest version bump, and the validator. It
auto-loads when a `SKILL.md` or `agents/*.md` is created; load it explicitly if it has not.

Whatever else gets skipped, these five land in the **same commit** or CI fails:

1. A row in the root `README.md` table (Skills or Agents).
2. A row in `plugins/ceh-<plugin>/README.md`.
3. A version bump in **both** `plugins/ceh-<plugin>/.claude-plugin/plugin.json` and
   `.claude-plugin/marketplace.json` — level per the Versioning section below.
4. `.agents_workspace/PLUGIN_DEPENDENCY_PLAN.md` §4, if the change adds or removes a dependency
   edge or a `ceh-scenario-*` bundle.
5. `python tools/validate-plugins/validate.py` green.

## Commands

```bash
# List all skills in a plugin
ls plugins/ceh-<plugin>/skills/

# Find a skill by name across all plugins
find plugins -path '*skills/<name>/SKILL.md'

# Show every declared dependency edge
grep -H '"dependencies"' plugins/*/.claude-plugin/plugin.json

# Verify every plugin is listed in marketplace.json
grep '"name"' plugins/ceh-*/.claude-plugin/plugin.json .claude-plugin/marketplace.json

# Validate the whole repo — CI runs this too
python tools/validate-plugins/validate.py
```

## Versioning

Two independent layers.

**Per-plugin versions** (load-bearing for auto-update) live in
`plugins/ceh-<plugin>/.claude-plugin/plugin.json`, mirrored in `.claude-plugin/marketplace.json`,
and both must be bumped in the same commit. Bump at commit time, not during iterative edits.

- **PATCH** — content or description updates.
- **MINOR** — a new skill or agent, or adding/removing a `dependencies` entry (that changes what a
  user gets on install, which is more than content).
- **MAJOR** — the plugin is renamed or removed.

**The repo git tag** (e.g. `v2.3.0`) marks a consistent state of all plugins together and is a
deployment snapshot and changelog anchor only — it does not drive auto-update. It increments
sequentially from the previous repo tag, independent of individual plugin versions: MINOR when any
plugin adds a skill or agent, PATCH for content-only. Cut it after bumping plugin versions
(`git tag vX.Y.Z && git push origin vX.Y.Z`), and add a `CHANGELOG.md` entry: prose on what changed
and why, a `### Plugin versions` table listing every plugin bumped, then `### Added` / `### Changed`
/ `### Fixed`.

## Key Files

| File | Purpose |
|------|---------|
| `plugins/ceh-<plugin>/.claude-plugin/plugin.json` | Plugin version, metadata, dependencies |
| `.claude-plugin/marketplace.json` | Marketplace listing (all plugins) |
| `README.md` | User-facing docs — scenario, skill, and agent tables live here |
| `docs/CROSS_REFERENCES.md` | Content duplicated across skills: canonical source and every copy |
| `CHANGELOG.md` | Release notes per repo tag, each with a `### Plugin versions` table |
| `docs/CHANGELOG-v1-v2.md` | Release notes for v1.0.0–v2.8.0, before the v3.0.0 reorganisation |
| `docs/TESTING_WORKFLOW.md` | How `ceh-testing`, the three stack testing skills, and the tester agents route between each other |
| `.agents_workspace/DECISION_LOG.md` | Agent decision log — **tracked in git here**, append-only, next sequential entry ID |
| `.agents_workspace/PLUGIN_DEPENDENCY_PLAN.md` | Dependency graph and scenario bundles: decisions, reference audit, checklist |

## Cross-Reference Rule

Before editing any skill, check `docs/CROSS_REFERENCES.md`. If the section you are changing appears
there, edit the canonical file first, then mirror the change to every listed copy in the same
session. New duplication gets a new entry.

## Shared-Standards Duplication Policy

Each use-case plugin must be self-contained so a user loads exactly one plugin per use case. When a
foundational standard is needed by more than one, **duplicate the delta into each** rather than
extracting a shared base plugin.

Canonical case: the Python foundation (uv/pyproject/ruff/mypy + pytest) is duplicated into
`ceh-python-service` and `ceh-python-library`, with the library copy dropping the web-only deps
(`fastapi`, `uvicorn`, `asyncpg`) and the uvicorn dev-server command.

The cost is drift; the required mitigation is to register every duplicated block in
`docs/CROSS_REFERENCES.md` and propagate edits in the same session (see above).
