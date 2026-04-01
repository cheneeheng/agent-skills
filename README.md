# CEH Agent Skills Plugin

A Claude Code plugin providing engineering standards for AI coding agents. Skills cover the full development lifecycle: behavioral contract, architecture design, Python backend, TypeScript frontend, Git workflow, release ops, and chat summarization.

## Skills

| Skill | Invoke as | When to load |
|-------|-----------|--------------|
| Agent Coding Contract | `/ceh:agent-coding-contract` | Start of any coding session — defines interactive vs autonomous modes and the five-step task workflow |
| Architecture Design | `/ceh:architecture-design` | Designing APIs, domain models, database schemas, or LLM integrations |
| Git Workflow | `/ceh:git-workflow` | Writing commits, opening PRs, reviewing code, or managing dependencies |
| Python Backend | `/ceh:python-backend` | Writing or reviewing FastAPI + asyncpg + uv Python code |
| TypeScript Frontend | `/ceh:typescript-frontend` | Writing or reviewing SvelteKit + Bun + Vitest TypeScript code |
| Release Ops | `/ceh:release-ops` | Deployments, migrations, incident response, or observability setup |
| Summarize Chat | `/ceh:summarize-chat` | Summarizing the current session for handoff to a future LLM session |
| Lessons Learned | `/ceh:lessons-learned` | Extracting lessons learned from the current session into `LESSONS_LEARNED.md` |

## Installing in Claude Code

### Step 1 — Add the marketplace

```
/plugin marketplace add cheneeheng/agent-skills
```

### Step 2 — Install the plugin

For the current project only:

```
/plugin install ceh@ceh-plugins --scope project
```

For all projects (user-wide):

```
/plugin install ceh@ceh-plugins --scope user
```

### Step 3 — Verify

```
/help
```

The `ceh:` skills should appear in the skills list.

---

### Manual installation (alternative)

If you prefer not to use a marketplace, clone this repo and point Claude Code at the `ceh/` subdirectory directly:

```bash
git clone https://github.com/cheneeheng/agent-skills.git ~/agent-skills
```

Then add the plugin path to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "plugins": [
    { "path": "~/agent-skills/ceh" }
  ]
}
```
