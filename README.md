# CEH Agent Skills Plugins

A collection of Claude Code plugins providing engineering standards for AI coding agents. Skills cover
the full development lifecycle, split into focused plugins — one per domain.

Skills come in two types:

- **Bundle skills** — load a full domain at the start of a session (explicit invocation)
- **Micro-skills** — narrow skills that auto-trigger based on what you are working on

---

## Plugins

| Plugin | Install as | Contents |
|--------|-----------|---------|
| Agent Coding Contract | `ceh-agent-coding-contract` | Behavioral contract for coding agents |
| Architecture Design | `ceh-architecture-design` | API design, domain modeling, event sourcing, LLM integration, PostgreSQL, REST API |
| Python Backend | `ceh-python-backend` | FastAPI, asyncpg, uv, testing, observability, security |
| TypeScript Frontend | `ceh-typescript-frontend` | SvelteKit, Bun, Vitest, Playwright, accessibility |
| Git Workflow | `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review, dependency management |
| Release Ops | `ceh-release-ops` | Deployments, migrations, incident response, observability, security, definition of done |
| Summarize Chat | `ceh-summarize-chat` | Structured session summary for LLM handoff |
| Lessons Learned | `ceh-lessons-learned` | Session retrospectives into `LESSONS_LEARNED.md` |
| Dev Tools | `ceh-dev-tools` | Repository exploration and codebase orientation agents |

---

## Bundle Skills

Load these explicitly at the start of a session or when you need the full domain context.

| Skill | Plugin | Invoke as | When to load |
|-------|--------|-----------|--------------|
| Agent Coding Contract | `ceh-agent-coding-contract` | `/ceh-agent-coding-contract:agent-coding-contract` | Start of any coding session — defines interactive vs autonomous modes and the five-step task workflow |
| Architecture Design | `ceh-architecture-design` | `/ceh-architecture-design:architecture-design` | Session covering API design, domain modeling, database schemas, or LLM integrations |
| Python Backend | `ceh-python-backend` | `/ceh-python-backend:python-backend` | Session writing or reviewing FastAPI + asyncpg + uv Python code |
| TypeScript Frontend | `ceh-typescript-frontend` | `/ceh-typescript-frontend:typescript-frontend` | Session writing or reviewing SvelteKit + Bun + Vitest TypeScript code |
| Git Workflow | `ceh-git-workflow` | `/ceh-git-workflow:git-workflow` | Session involving commits, PRs, branching, or dependency management |
| Release Ops | `ceh-release-ops` | `/ceh-release-ops:release-ops` | Session covering deployments, migrations, incident response, or observability |
| Summarize Chat | `ceh-summarize-chat` | `/ceh-summarize-chat:summarize-chat` | Summarizing the current session for handoff to a future LLM session |
| Lessons Learned | `ceh-lessons-learned` | `/ceh-lessons-learned:lessons-learned` | Extracting lessons learned from the current session into `LESSONS_LEARNED.md` |

---

## Agents

Agents run autonomously for a defined task and hand results back to the parent session.

| Agent | Plugin | Invoke as | When to use |
|-------|--------|-----------|-------------|
| Repo Tree Mapper | `ceh-dev-tools` | `/ceh-dev-tools:repo-tree-mapper` | Map or document a repository's structure; auto-triggers on orientation requests |

---

## Micro-Skills

Narrow skills designed to auto-trigger based on what you are actively working on. Each points
to the relevant reference content in its parent bundle — no duplication.

### Architecture (`ceh-architecture-design`)

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| ADR | `/ceh-architecture-design:adr` | Making a significant architectural decision |
| Domain Modeling | `/ceh-architecture-design:domain-modeling` | Designing entities, IDs, or status fields |
| Event Sourcing | `/ceh-architecture-design:event-sourcing` | Working with the event log or state snapshots |
| REST API | `/ceh-architecture-design:rest-api` | Building endpoints, choosing HTTP codes, shaping error responses |
| PostgreSQL | `/ceh-architecture-design:postgresql` | Writing SQL, designing schemas, or using asyncpg |
| LLM Integration | `/ceh-architecture-design:llm-integration` | Integrating LLM calls or handling LLM output |

### Python Backend (`ceh-python-backend`)

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| FastAPI | `/ceh-python-backend:fastapi` | Writing route handlers, DI, middleware, or exception hierarchy |
| Python Testing | `/ceh-python-backend:python-testing` | Writing Python unit or integration tests |

### TypeScript Frontend (`ceh-typescript-frontend`)

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| SvelteKit | `/ceh-typescript-frontend:sveltekit` | Working on routes, stores, components, or the API client |
| Frontend Testing | `/ceh-typescript-frontend:frontend-testing` | Writing Vitest, Testing Library, MSW, or Playwright tests |
| Accessibility | `/ceh-typescript-frontend:accessibility` | Writing Svelte component markup |
| Coding Style | `/ceh-typescript-frontend:coding-style` | Applying TypeScript type conventions or import ordering |
| Linting | `/ceh-typescript-frontend:linting` | Configuring or running ESLint, Prettier, or svelte-check |

### Operations (`ceh-release-ops`)

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| Observability | `/ceh-release-ops:observability` | Adding logging, metrics, or health check code |
| Database Migrations | `/ceh-release-ops:database-migrations` | Writing or running Alembic migrations |
| Incidents | `/ceh-release-ops:incidents` | Responding to a production incident or writing a post-mortem |
| Definition of Done | `/ceh-release-ops:definition-of-done` | Preparing to open a pull request |
| Security | `/ceh-release-ops:security` | Handling secrets, CORS, rate limiting, or input validation |
| Versioning | `/ceh-release-ops:versioning` | Bumping a version, tagging a release, or classifying a change |
| Rollback | `/ceh-release-ops:rollback` | Deciding to roll back a deployment or recovering from a failed migration |

### Git Workflow (`ceh-git-workflow`)

| Skill | Invoke as | Auto-triggers when |
|-------|-----------|-------------------|
| Branch | `/ceh-git-workflow:branch` | Creating or naming a branch |
| Commit | `/ceh-git-workflow:commit` | Writing a commit message or staging changes |
| Open PR | `/ceh-git-workflow:open-pr` | Opening a pull request or writing a PR description |
| Merge | `/ceh-git-workflow:merge` | Merging a branch or choosing a merge strategy |
| Hotfix | `/ceh-git-workflow:hotfix` | Executing a critical production fix |
| Release | `/ceh-git-workflow:release` | Tagging a release or bumping a version |
| Gitignore | `/ceh-git-workflow:gitignore` | Creating or editing a `.gitignore` file |
| Code Review | `/ceh-git-workflow:code-review` | Reviewing a PR or leaving review comments |
| Dependency Management | `/ceh-git-workflow:dependency-management` | Adding or upgrading a package |

---

## Cross-Bundle Reference Stubs

Three micro-skills reference content from two different plugins. To keep relative paths valid,
the foreign reference file is duplicated as a read-only stub inside the host plugin.

| Micro-skill | Host plugin | Stub file | Source |
|-------------|-------------|-----------|--------|
| `postgresql` | `ceh-architecture-design` | `skills/python-backend/references/database.md` | `ceh-python-backend` |
| `observability` | `ceh-release-ops` | `skills/python-backend/references/observability.md` | `ceh-python-backend` |
| `security` | `ceh-release-ops` | `skills/python-backend/references/security.md` | `ceh-python-backend` |

When updating `ceh-python-backend/skills/python-backend/references/database.md`,
`observability.md`, or `security.md`, also update the corresponding stub file in the host plugin.

---

## Installing in Claude Code

### Step 1 — Add the marketplace

```
/plugin marketplace add cheneeheng/agent-skills
```

### Step 2 — Install plugins

Install individual plugins for the domains you need:

```
/plugin install ceh-git-workflow@ceh-plugins --scope user
/plugin install ceh-python-backend@ceh-plugins --scope user
/plugin install ceh-typescript-frontend@ceh-plugins --scope user
/plugin install ceh-architecture-design@ceh-plugins --scope user
/plugin install ceh-release-ops@ceh-plugins --scope user
/plugin install ceh-agent-coding-contract@ceh-plugins --scope user
/plugin install ceh-summarize-chat@ceh-plugins --scope user
/plugin install ceh-lessons-learned@ceh-plugins --scope user
/plugin install ceh-dev-tools@ceh-plugins --scope user
```

Or install all at once using `--scope project` for project-specific installs.

### Step 3 — Verify

```
/help
```

The `ceh-*:` skills should appear in the skills list.

---

### Manual installation (alternative)

Clone this repo and point Claude Code at the plugin subdirectories directly:

```bash
git clone https://github.com/cheneeheng/agent-skills.git ~/agent-skills
```

Then add plugin paths to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "plugins": [
    { "path": "~/agent-skills/ceh-git-workflow" },
    { "path": "~/agent-skills/ceh-python-backend" },
    { "path": "~/agent-skills/ceh-typescript-frontend" },
    { "path": "~/agent-skills/ceh-architecture-design" },
    { "path": "~/agent-skills/ceh-release-ops" },
    { "path": "~/agent-skills/ceh-agent-coding-contract" },
    { "path": "~/agent-skills/ceh-summarize-chat" },
    { "path": "~/agent-skills/ceh-lessons-learned" },
    { "path": "~/agent-skills/ceh-dev-tools" }
  ]
}
```
