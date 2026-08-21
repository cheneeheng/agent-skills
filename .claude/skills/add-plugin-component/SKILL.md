---
name: add-plugin-component
description: >-
  The checklist for adding or changing a skill, agent, hook, or script in this plugin repo — which
  plugin it belongs in, the frontmatter it needs, and every registration chore that must land in the
  same commit (README tables, CROSS_REFERENCES.md, plugin.json + marketplace.json version bumps,
  validate.py). Load whenever a new SKILL.md or agents/*.md is being created, an existing one is
  being renamed or moved between plugins, or the user says "add a skill", "add an agent", "new
  plugin component", or asks why validate.py is failing.
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

Before editing an existing skill, check `CROSS_REFERENCES.md`. If the section appears there,
propagate the edit to **every** listed file in the same session — canonical file first, then the
copies. If you introduce new duplication, add an entry naming the canonical source, every copy,
what is shared, and what deliberately diverges.

## 5. Bump the version in both manifests

Same commit, both files, or CI fails:

- `plugins/ceh-<plugin>/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

**PATCH** for content/description updates, **MINOR** for a new skill or agent. Bump at commit
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
