# CEH Agent Skills Plugin

A Claude Code plugin providing engineering standards for AI coding agents. Skills cover the full
development lifecycle: behavioral contract, architecture design, Python backend, TypeScript
frontend, Git workflow, release ops, and chat summarization.

Skills come in two types:

- **Bundle skills** — load a full domain at the start of a session (explicit invocation)
- **Micro-skills** — narrow skills that auto-trigger based on what you are working on

---

## Bundle Skills

Load these explicitly at the start of a session or when you need the full domain context.

| Skill | Invoke as | When to load |
|-------|-----------|--------------|
| Agent Coding Contract | `/ceh:agent-coding-contract` | Start of any coding session — defines interactive vs autonomous modes and the five-step task workflow |
| Architecture Design | `/ceh:architecture-design` | Session covering API design, domain modeling, database schemas, or LLM integrations |
| Python Backend | `/ceh:python-backend` | Session writing or reviewing FastAPI + asyncpg + uv Python code |
| TypeScript Frontend | `/ceh:typescript-frontend` | Session writing or reviewing SvelteKit + Bun + Vitest TypeScript code |
| Git Workflow | `/ceh:git-workflow` | Session involving commits, PRs, branching, or dependency management |
| Release Ops | `/ceh:release-ops` | Session covering deployments, migrations, incident response, or observability |
| Summarize Chat | `/ceh:summarize-chat` | Summarizing the current session for handoff to a future LLM session |
| Lessons Learned | `/ceh:lessons-learned` | Extracting lessons learned from the current session into `LESSONS_LEARNED.md` |

---

## Micro-Skills

Narrow skills designed to auto-trigger based on what you are actively working on. Each points
to the relevant reference content in its parent bundle — no duplication.

### Architecture

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| ADR | `/ceh:adr` | Making a significant architectural decision |
| Domain Modeling | `/ceh:domain-modeling` | Designing entities, IDs, or status fields |
| Event Sourcing | `/ceh:event-sourcing` | Working with the event log or state snapshots |
| REST API | `/ceh:rest-api` | Building endpoints, choosing HTTP codes, shaping error responses |
| PostgreSQL | `/ceh:postgresql` | Writing SQL, designing schemas, or using asyncpg |
| LLM Integration | `/ceh:llm-integration` | Integrating LLM calls or handling LLM output |

### Python Backend

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| FastAPI | `/ceh:fastapi` | Writing route handlers, DI, middleware, or exception hierarchy |
| Python Testing | `/ceh:python-testing` | Writing Python unit or integration tests |

### TypeScript Frontend

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| SvelteKit | `/ceh:sveltekit` | Working on routes, stores, components, or the API client |
| Frontend Testing | `/ceh:frontend-testing` | Writing Vitest, Testing Library, MSW, or Playwright tests |
| Accessibility | `/ceh:accessibility` | Writing Svelte component markup |

### Operations

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| Observability | `/ceh:observability` | Adding logging, metrics, or health check code |
| Database Migrations | `/ceh:database-migrations` | Writing or running Alembic migrations |
| Incidents | `/ceh:incidents` | Responding to a production incident or writing a post-mortem |
| Definition of Done | `/ceh:definition-of-done` | Preparing to open a pull request |
| Security | `/ceh:security` | Handling secrets, CORS, rate limiting, or input validation |

### Git Workflow

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| Code Review | `/ceh:code-review` | Reviewing a PR or leaving review comments |
| Dependency Management | `/ceh:dependency-management` | Adding or upgrading a package |

---

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

If you prefer not to use a marketplace, clone this repo and point Claude Code at the `ceh/`
subdirectory directly:

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
