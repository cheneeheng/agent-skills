# Agent Skills Repo

Plugin repo for the `ceh` Claude Code plugin — engineering standards delivered as skills.

## Structure

```
.claude-plugin/        # Marketplace manifest (marketplace.json)
ceh/
├── .claude-plugin/    # Plugin manifest (plugin.json) — version lives here
└── skills/
    ├── <skill-name>/
    │   ├── SKILL.md               # Required — frontmatter + description + body
    │   └── references/            # Optional — topic-split reference files
    │       └── <topic>.md
```

## Skill Types

Two kinds of skills exist in this plugin:

- **Bundle skills** — load a full domain. Explicit session-wide invocation. SKILL.md has
  a short title, summary paragraph, and a references table pointing to files in `references/`.
- **Micro-skills** — narrow, auto-triggering. SKILL.md has a tight description (the trigger)
  and a single instruction to read the relevant reference file(s) from the parent bundle.

## Adding a Skill

1. Create `ceh/skills/<name>/SKILL.md` with frontmatter `name` and `description` fields.
2. For bundles: add topic files under `ceh/skills/<name>/references/`.
3. For micro-skills: point to existing reference files in sibling bundle skills.
4. Update `README.md` skills tables (bundles section or micro-skills section).
5. Add a `CHANGELOG.md` entry and bump version in both:
   - `ceh/.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`

## Versioning

PATCH bump for new or updated skills. Follow Conventional Commits.
Both `plugin.json` and `marketplace.json` must be bumped in the same commit.
Current version: **1.0.2**

## Key Files

| File | Purpose |
|------|---------|
| `ceh/.claude-plugin/plugin.json` | Plugin version and metadata |
| `.claude-plugin/marketplace.json` | Marketplace listing (also has version) |
| `CHANGELOG.md` | Release history |
| `LESSONS_LEARNED.md` | Session retrospectives — append, never overwrite |
| `README.md` | User-facing docs — bundle and micro-skill tables both live here |
