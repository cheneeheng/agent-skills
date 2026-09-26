# Plugin Dependencies

The current dependency graph between `ceh-*` plugins: every declared edge, the reference that
forces it, what each scenario bundle installs, and the rules for adding or removing an edge.

The rules themselves are summarized in `CLAUDE.md` (Plugin Dependencies). This page holds what
`CLAUDE.md` does not: the graph as it stands, and the evidence behind each edge. The full design
record is `.agents_workspace/archive/PLUGIN_DEPENDENCY_PLAN.md`, git-ignored and local only.

## How dependencies behave

- **Declared in `plugin.json` only.** Never in the `marketplace.json` entry, which mirrors only
  version and description.
- **Bare strings, no version ranges.** Ranges resolve against per-plugin `{name}--v{version}` tags,
  and this repo tags only repo-wide snapshots (`v6.9.2`).
- **Installed and enabled automatically and transitively.** There is no optional dependency, and
  `defaultEnabled: false` does not keep a dependency out. The only way to not install a plugin is to
  leave it out of every `dependencies` list on the path.

## The graph

Arrow = "the left plugin cannot do its job unless the right plugin is installed".

```
LAYER 3 — scenario bundles (plugin.json + README.md only)

  ceh-scenario-{service,library,webapp}-greenfield
        │  own -iterate twin + ceh-scaffolding + ceh-business-plan
        ▼
  ceh-scenario-{service,library,webapp}-iterate
        │  ceh-scenario-core,
        │  ceh-architecture, ceh-documentation, ceh-usability-audit, ceh-plan-build-review
        │  + one stack plugin: ceh-python-service | ceh-python-library | ceh-web-frontend
        ▼
  ceh-scenario-core   ◄──   ceh-scenario-editorial
        │                     + ceh-blog, ceh-documentation, ceh-seo
        │  ceh-coding-agent, ceh-git-workflow, ceh-testing

LAYER 2 — plugins that depend on Layer 1 (five edges)

  ceh-python-service  ──► ceh-testing
  ceh-python-library  ──► ceh-testing
  ceh-web-frontend    ──► ceh-testing
  ceh-ops             ──► ceh-coding-agent
  ceh-orchestration   ──► ceh-coding-agent

LAYER 1 — cross-cutting leaves, declare nothing

  ceh-coding-agent   ceh-git-workflow   ceh-testing
  ceh-fabled         ceh-advisor        (experimental)
```

Every other plugin declares nothing and depends on nothing.

## Edge evidence

Each Layer 2 edge exists because a reference fires on every run. Negative routing and conditional
handoffs never create an edge (see Rules below).

| Edge | Reference that forces it |
|------|--------------------------|
| `ceh-python-service` ──► `ceh-testing` | `skills:` preload of `ceh-testing:design-test-cases` in `python-{unit,integration,system}-tester`, and an explicit invocation in `python-service-testing` |
| `ceh-web-frontend` ──► `ceh-testing` | `skills:` preload of `ceh-testing:design-test-cases` in `ts-{unit,integration,system}-tester`, and an explicit invocation in `frontend-testing` |
| `ceh-python-library` ──► `ceh-testing` | Explicit invocation of `ceh-testing:design-test-cases` in `python-library-testing` |
| `ceh-ops` ──► `ceh-coding-agent` | `skills:` preload of `ceh-coding-agent:agent-coding-contract` in `github-actions` and `gitlab-ci` |
| `ceh-orchestration` ──► `ceh-coding-agent` | `skills:` preload of `ceh-coding-agent:agent-coding-contract` in `executor` |

All remaining explicit invocations (`ceh-git-workflow` flows, `ceh-documentation:write-project-docs`,
`ceh-workflow-builder:build-agentic-workflow`) call skills inside their own plugin.

## What each scenario installs

The full transitive closure. `●` = listed directly, `○` = arrives through another dependency.

| Plugin | core | service-iterate | library-iterate | webapp-iterate | *-greenfield | editorial |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| `ceh-coding-agent` | ● | ○ | ○ | ○ | ○ | ○ |
| `ceh-git-workflow` | ● | ○ | ○ | ○ | ○ | ○ |
| `ceh-testing` | ● | ○ | ○ | ○ | ○ | ○ |
| `ceh-architecture` | | ● | ● | ● | ○ | |
| `ceh-documentation` | | ● | ● | ● | ○ | ● |
| `ceh-usability-audit` | | ● | ● | ● | ○ | |
| `ceh-plan-build-review` | | ● | ● | ● | ○ | |
| `ceh-python-service` | | ● | | | ○ (service) | |
| `ceh-python-library` | | | ● | | ○ (library) | |
| `ceh-web-frontend` | | | | ● | ○ (webapp) | |
| `ceh-scaffolding` | | | | | ● | |
| `ceh-business-plan` | | | | | ● | |
| `ceh-blog` | | | | | | ● |
| `ceh-seo` | | | | | | ● |

`ceh-scenario-core` is also an install entry point on its own, for a stack no other bundle covers.
Every other bundle reaches it, directly or through its `-iterate` twin.

Worst-case closure for a single non-bundle plugin is 2 plugins, because every Layer 1 plugin is a
leaf.

## Never bundled

| Reason | Plugins |
|--------|---------|
| Experimental, installed deliberately | `ceh-fabled`, `ceh-advisor` (installs always-on session hooks), `ceh-orchestration` |
| Session mechanics, install once at user scope | `ceh-summarize-chat`, `ceh-lessons-learned` |
| Opt-in per moment | `ceh-ops` (deploy), `ceh-seo` outside editorial (a public surface is a per-release property) |
| Standalone workflows | `ceh-evaluation`, `ceh-git-datastore`, `ceh-workflow-builder` |

## Rules for an edge

1. **The reference fires on every run of the skill or agent.** A conditional handoff stays prose:
   `ceh-usability-audit` delegating WCAG to `ceh-web-frontend:accessibility` fires only when the
   subject has a UI.
2. **Negative routing never counts.** `Not for tagging, use ceh-git-workflow:release` names an
   alternative, and an edge would install what the user steered away from.
3. **A cross-cutting plugin depends only on cross-cutting plugins.** This keeps the graph layered.
4. **A non-bundle plugin never depends on a scenario bundle.** A bundle is an install entry point,
   and depending on one drags a whole scenario into an unrelated install.
5. **An explicit invocation needs its edge.** `Invoke the Skill tool with skill="ceh-x:y"` must
   target a skill in the same plugin or a declared dependency, and the target must not set
   `disable-model-invocation: true`.

References that look like edges but deliberately are not:

| Reference | Why it stays prose |
|-----------|--------------------|
| `ceh-coding-agent:refactor-repo` / `shrink-diff` → `ceh-testing`, `ceh-git-workflow` | Conditional, and Layer 1 declares nothing |
| `ceh-usability-audit` → `ceh-web-frontend:accessibility` | Conditional on the subject having a UI |
| `ceh-scaffolding` → the three stack plugins | Advisory: an edge would install all three stacks |
| `ceh-git-workflow` flows → `ceh-documentation:update-readme` | Conditional on the change being user-facing |
| `ceh-ops:deploy` → `ceh-git-workflow:release` | A precondition, not a call |
| `ceh-business-plan` → `ceh-plan-build-review` `plan-schema.md` | Removed by duplicating the file (see `docs/CROSS_REFERENCES.md`) |

## Checking and changing the graph

```bash
# Every declared edge
grep -H '"dependencies"' plugins/*/.claude-plugin/plugin.json

# Every cross-plugin agent preload
grep -A6 '^skills:' plugins/*/agents/*.md | grep -- '- ceh-'

# Enforces rules 4 and 5, acyclicity, resolution, the bundle shape, and that every bundle reaches core
python tools/validate-plugins/validate.py
```

Adding or removing a `dependencies` entry is a **MINOR** bump for that plugin, in both
`plugin.json` and `.claude-plugin/marketplace.json`. Update this page in the same commit.
