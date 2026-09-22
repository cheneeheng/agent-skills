---
name: add-plugin-component
description: >-
  The checklist for adding or changing a skill, agent, hook, script, or a whole new ceh-* plugin in
  this plugin repo — which plugin it belongs in, the frontmatter it needs, and every registration
  chore that must land in the same commit (README tables, docs/CROSS_REFERENCES.md, plugin.json +
  marketplace.json version bumps, validate.py). Overrides plugin-dev advice that conflicts with this
  repo. Load whenever a new SKILL.md or agents/*.md is being created, an existing one is being
  renamed or moved between plugins, a new plugin directory is being added under plugins/, or the
  user says "add a skill", "add an agent", "new plugin component", "create a plugin", "new ceh
  plugin", or asks why validate.py is failing.
argument-hint: '[skill-or-agent-name]'
---

# Adding a Component to This Repo

The content is the easy half. The half that gets forgotten is registration: this repo keeps the
same fact in four places on purpose, and CI fails when they drift.

## 1. Pick the plugin

Plugins split on **use case**, not tech domain or lifecycle phase. Load exactly one plugin per
use case, so each must be self-contained.

- A skill triggers on a **moment** (a verb: "I'm opening a PR", "I'm writing a migration"), never
  a **topic** (a noun: "PostgreSQL"). Topic-named skills either never auto-trigger or restate what
  the model already knows. If you cannot name the moment, the skill is not ready.
- Framework variants do **not** get their own plugin when their skills trigger on disjoint file
  types — `sveltekit` and `react-vite` share `ceh-web-frontend`.
- A foundational standard needed by two use-case plugins is **duplicated into both**, never
  extracted into a shared base plugin. Register the duplication (step 4).
- App-specific patterns are not standards. Anything bound to one application's schema or design
  gets removed, not filed as a niche plugin.

If no existing plugin owns the use case, create one first — see [New plugin](#new-plugin) — then
continue at step 2.

## 2. Write the component

**Skill** — `plugins/ceh-<plugin>/skills/<name>/SKILL.md`, `name` matching the directory. All content
inline; `references/` is only for schemas and templates shared across skills.

**Agent** — `plugins/ceh-<plugin>/agents/<name>.md`. Required frontmatter is only `name` and `description`
(`model` defaults to `inherit`); auto-delegation is driven entirely by `description` (include "use
proactively" to encourage it).

**`description` is always a folded block scalar (`>-`)** — never quoted, never plain. `validate.py`
rejects anything else.

```yaml
description: >-
  Load this skill when doing X: the colon is literal here, as are "quotes" and 'apostrophes'.
  Wrap at ~98 chars with a uniform 2-space indent and no blank lines.
```

It is the only style with no escaping burden. A plain scalar cannot contain `: `, single-quoted
needs `''` doubling, double-quoted needs `\` and `"` escaping — all three have silently produced
invalid YAML in this repo. Keep the indent uniform (a more-indented line becomes a literal newline
instead of folding) and avoid blank lines. Any *other* key containing `: ` gets single quotes.

Frontmatter worth reaching for before writing prose that does the same job:

| Field | Use it for | Watch out |
|---|---|---|
| `paths` | Skills whose trigger really is a file type | **Narrows** auto-loading. A skill with real non-file triggers ("a `uv` command is run") loses them |
| `effort` | Reasoning-heavy skills | Default is already `high` — only `xhigh`/`max`/`low` change anything |
| `disallowed-tools` | Skills that must not write | Check the body first; most "review" skills here do apply fixes |
| `context: fork` | Heavy, **non-interactive** skills that act on the conversation | A fork inherits the transcript and full tool pool; a plain subagent loses `AskUserQuestion` |
| `argument-hint` | Any `disable-model-invocation: true` skill | Cosmetic but free |
| `${CLAUDE_SKILL_DIR}` | Referencing a bundled script | Substituted in the body *and* in `allowed-tools` Bash rules; `${CLAUDE_PLUGIN_ROOT}` is **not** substituted in skill bodies |
| `memory` | Agents that should learn across sessions | Auto-enables Read/Write/Edit on that agent |
| `compatibility` | Skills that need software the machine may lack (`git`, `gh`, `uv`, `bun`, a server, network) | `>-` scalar, max 500 chars. Name runtime + minimum version and what fails without it. Omit for read-files-emit-Markdown skills |

**Cross-plugin calls** — when a skill must call a skill in another plugin on *every* run, add the
target plugin to `dependencies` in `plugin.json` (never in `marketplace.json`; bare strings, no
ranges) and call it explicitly: `Invoke the Skill tool with skill="ceh-<plugin>:<skill>"`.
Conditional handoffs and negative routing ("Not for X, use ...") stay prose with no dependency. A
cross-cutting plugin may depend only on other cross-cutting plugins. `validate.py` rejects a call
whose target does not resolve, is not a declared dependency, or sets
`disable-model-invocation: true`.

**Plugin-agent gotchas** — Claude Code ignores `permissionMode`, `hooks`, and `mcpServers` on
plugin agents (security restriction). Do not add them; they read as working config and are not.
Grant edit permissions via session `permissions.allow` in `settings.json` instead. Subagents run in
the **background by default**, and background subagents keep only a reduced built-in tool set — if
an agent needs a tool outside `Read/Grep/Glob/Bash/PowerShell/Edit/Write/NotebookEdit/WebFetch/
WebSearch/TodoWrite/Skill/ToolSearch/EnterWorktree/ExitWorktree/Monitor/TaskStop/SendMessage/
Artifact`, it will be stripped silently. `AskUserQuestion` is stripped from *every* subagent,
foreground or background — an agent can never stop to ask.

`skills:` entries must be fully qualified as `plugin:skill` or the preload fails silently. The
preload is also the only route a hook-loaded standard has into an agent: `SessionStart` hooks never
fire for subagents.

**`isolation: worktree` is deliberately unused in this repo.** Subagent worktrees branch from the
repository's **default branch**, not the parent session's `HEAD`, unless `worktree.baseRef: "head"`
is set in `settings.json` — and their changes stay in the worktree rather than landing in your
checkout. Under this repo's feature-branch rule that hands an agent a copy of `main` without your
work, so no agent sets it.

## 3. Update both README tables

- Root `README.md` — add a row under the correct plugin group in **Skills** or **Agents**. If the
  plugin has no agents group yet, add a `### <Plugin> (\`ceh-<plugin>\`)` subsection.
- `plugins/ceh-<plugin>/README.md` — add a row to that plugin's own table.

## 4. Register any duplication

Before editing an existing skill, check `docs/CROSS_REFERENCES.md`. If the section appears there,
propagate the edit to **every** listed file in the same session — canonical file first, then the
copies. If you introduce new duplication, add an entry naming the canonical source, every copy,
what is shared, and what deliberately diverges.

## 5. Bump the version in both manifests

Same commit, both files, or CI fails:

- `plugins/ceh-<plugin>/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

**PATCH** for content/description updates, **MINOR** for a new skill or agent or for adding or
removing a `dependencies` entry, **MAJOR** for renaming or removing the plugin. Bump at commit
time, not during iterative edits. The repo git tag is a separate, independent layer — cut it after
the plugin bumps land.

## 6. Validate

```bash
python tools/validate-plugins/validate.py
```

Same gate CI runs via `.github/workflows/validate.yml`. It checks manifest/marketplace sync,
semver, skill/agent frontmatter (`name` + `description`, description ≤ 1024 chars, skill `name`
matching its directory), that `references/...` and `${CLAUDE_PLUGIN_ROOT}/scripts/...` and
`${CLAUDE_SKILL_DIR}/...` mentions resolve to real files, that `plugin:component` references
resolve, and that bundled `*.sh` / `*.py` scripts parse.

The validator only requires `name` and `description` in frontmatter, so a typo in any other field
passes validation and fails silently at runtime. Check new fields against the Claude Code docs
rather than trusting a green run.

## New plugin

Only when step 1 finds no plugin that owns the use case. Decide the tier first (scenario bundle,
cross-cutting, use-case workflow, stack/build — see `CLAUDE.md`), then:

1. `plugins/ceh-<name>/.claude-plugin/plugin.json` — copy the shape of an existing one (`name`
   matching the directory, `version: "1.0.0"`, `description`, `author`, `repository`, `license`,
   `keywords`) plus `dependencies` if any. The directory sits flat under `plugins/`, no tier folder.
2. `plugins/ceh-<name>/README.md` with the plugin's own skill/agent table.
3. `.claude-plugin/marketplace.json` — a new entry whose `source`, `version`, and `description`
   mirror `plugin.json`. `validate.py` fails on a plugin missing from the marketplace or a version
   mismatch.
4. Root `README.md` — a row in the **Plugins** table, the plugin in the **Categorization** tier
   table, its Skills/Agents rows, and a line in both install lists (`/plugin install` and the
   manual `path` list).
5. `CLAUDE.md` — a row in the **Plugins** table and the plugin in the tier table.
6. A `ceh-scenario-*` bundle, only if the plugin belongs in that situation's install set. A bundle
   holds `plugin.json` (with `dependencies`) and `README.md` and nothing else — `validate.py`
   enforces it. Update `.agents_workspace/PLUGIN_DEPENDENCY_PLAN.md` §4 locally for any new edge.

The repo tag bumps MINOR and `CHANGELOG.md` lists the plugin at `1.0.0` under `### Added`.

## When plugin-dev skills are also loaded

`plugin-dev:create-plugin`, `skill-development`, `agent-development`, and `hook-development` trigger
on the same phrases and give generic advice. Where it conflicts with this repo, this skill wins:

| plugin-dev says | This repo does |
|---|---|
| Lean SKILL.md, detail in `references/` and `examples/` | Content inline. `references/` only for shared schemas or oversized standards |
| "This skill should be used when…" descriptions, any scalar style | `>-` folded scalar, "Load this skill when…" |
| Hook scripts in `examples/` | `scripts/`, referenced as `${CLAUDE_PLUGIN_ROOT}/scripts/...` |
| New plugin at `0.1.0`, marketplace entry optional | `1.0.0`, marketplace entry in the same commit |
| `plugin-validator` agent, `validate-agent.sh`, `validate-hook-schema.sh` | `python tools/validate-plugins/validate.py` is the gate |
| Agent `<example>` blocks and `color` | Prose `description`, no `<example>` blocks; `color` optional |
| Wait for user confirmation at each phase, ask where to create, `git init` | Autonomous mode, flat `plugins/`, existing repo |

plugin-dev stays useful for Claude Code mechanics this skill does not cover — hook event payloads,
MCP server config, settings files.
