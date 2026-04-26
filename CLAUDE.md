# Agent Skills Repo

Plugin repo for the `ceh-*` Claude Code plugins — engineering standards delivered as skills.
Each domain is a standalone plugin.

## Structure

```
.claude-plugin/               # Marketplace manifest (marketplace.json)
ceh-<plugin-name>/
├── .claude-plugin/           # Plugin manifest (plugin.json) — version lives here
├── agents/                   # Optional — subagents for complex autonomous tasks
├── scripts/                  # Optional — shell helpers (e.g. coverage, branch delete)
└── skills/
    ├── <bundle-skill>/
    │   ├── SKILL.md               # Required — frontmatter + description + body
    │   └── references/            # Optional — topic-split reference files
    │       └── <topic>.md
    └── <micro-skill>/
        └── SKILL.md               # Points to reference files in the sibling bundle skill
```

## Plugins

| Plugin directory | Domain |
|-----------------|--------|
| `ceh-agent-coding-contract` | Behavioral contract for coding agents |
| `ceh-architecture-design` | API design, domain modeling, event sourcing, LLM, PostgreSQL, REST |
| `ceh-python-backend` | FastAPI, asyncpg, uv, testing |
| `ceh-typescript-frontend` | SvelteKit, Bun, Vitest, Playwright, accessibility |
| `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review |
| `ceh-release-ops` | Deployments, migrations, incidents, observability, security |
| `ceh-summarize-chat` | Session summary for LLM handoff |
| `ceh-lessons-learned` | Session retrospectives |
| `ceh-dev-tools` | Repository exploration and codebase orientation agents |

## Skill Types

Two kinds of skills exist in each plugin:

- **Bundle skills** — load a full domain. Explicit session-wide invocation. SKILL.md has
  a short title, summary paragraph, and a references table pointing to files in `references/`.
- **Micro-skills** — narrow, auto-triggering. SKILL.md has a tight description (the trigger)
  and a single instruction to read the relevant reference file(s) from the parent bundle.

## Adding a Skill

1. Identify the correct plugin for the skill's domain.
2. Create `ceh-<plugin>/skills/<name>/SKILL.md` with frontmatter `name` and `description` fields.
3. For bundles: add topic files under `ceh-<plugin>/skills/<name>/references/`.
4. For micro-skills: point to existing reference files in the sibling bundle skill using relative paths.
5. Update `README.md` skills tables:
   - Bundle skill → add a row to the "Bundle Skills" table
   - Micro-skill → add a row under the correct group in the "Micro-Skills" section
6. Add a `CHANGELOG.md` entry and bump version in both:
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

# Check cross-bundle stubs are present
find . -path '*/python-backend/references/*.md' | sort
```

## Cross-bundle Micro-skills

Micro-skills that reference content from two different bundles (e.g. `postgresql`, `observability`,
`security`) live in one host plugin. The foreign reference files are duplicated into the host plugin
under a stub `skills/<foreign-bundle>/references/` directory so relative paths remain valid.

**Important:** No tooling enforces stub sync. When editing a source file in `ceh-python-backend`,
manually update the corresponding stub in the host plugin.

## Versioning

PATCH bump for new or updated skills. Follow Conventional Commits.
Bump versions only at commit time — not during iterative edits within a session.
Both the affected `plugin.json` and `marketplace.json` must be bumped in the same commit.
Current version: check `ceh-<plugin>/.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json`.

## Key Files

| File | Purpose |
|------|---------|
| `ceh-<plugin>/.claude-plugin/plugin.json` | Plugin version and metadata |
| `.claude-plugin/marketplace.json` | Marketplace listing (all plugins) |
| `CHANGELOG.md` | Release history |
| `docs/claude_logs/LESSONS_LEARNED.md` | Session retrospectives — append, never overwrite |
| `README.md` | User-facing docs — bundle and micro-skill tables both live here |
