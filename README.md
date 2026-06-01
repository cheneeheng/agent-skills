# CEH Agent Skills Plugins

A collection of Claude Code plugins providing engineering standards for AI coding agents. Skills cover
the full development lifecycle, split into focused plugins — one per domain.

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
| Blog | `ceh-blog` | Interview-driven blog post writing — from rough idea to publication-ready draft |
| Documentation | `ceh-documentation` | End-user/operator docs — user guides, runbooks, install/config, troubleshooting; changelog & README agents |

---

## Skills

### Agent Coding Contract (`ceh-agent-coding-contract`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Agent Coding Contract | `/ceh-agent-coding-contract:agent-coding-contract` | Start of any coding session — core rules, five-step workflow, stop conditions, non-goals |
| Implement From Plan | `/ceh-agent-coding-contract:implement-from-plan` | Implementing a SKELETON.md or ITER_NN.md planning document |
| Review Against Plan | `/ceh-agent-coding-contract:review-against-plan` | Auditing implementation against a SKELETON.md or ITER_NN.md planning document |

### Architecture (`ceh-architecture-design`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| ADR | `/ceh-architecture-design:adr` | Making a significant architectural decision |
| Domain Modeling | `/ceh-architecture-design:domain-modeling` | Designing entities, IDs, or status fields |
| Event Sourcing | `/ceh-architecture-design:event-sourcing` | Working with the event log or state snapshots |
| REST API | `/ceh-architecture-design:rest-api` | Building endpoints, choosing HTTP codes, shaping error responses |
| PostgreSQL | `/ceh-architecture-design:postgresql` | Writing SQL, designing schemas, or using asyncpg |
| LLM Integration | `/ceh-architecture-design:llm-integration` | Integrating LLM calls or handling LLM output |
| Repository Structure | `/ceh-architecture-design:repository-structure` | Creating new directories, adding modules, or deciding where code belongs |

### Python Backend (`ceh-python-backend`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| FastAPI | `/ceh-python-backend:fastapi` | Writing route handlers, DI, middleware, or exception hierarchy |
| Python Testing | `/ceh-python-backend:python-testing` | Writing Python unit or integration tests |
| Python Environment | `/ceh-python-backend:python-environment` | Setting up uv/pyproject.toml, writing type hints, configuring ruff/mypy |
| asyncpg | `/ceh-python-backend:asyncpg` | Writing database queries, transactions, or connection pool config |
| Python Observability | `/ceh-python-backend:python-observability` | Adding structlog logging, correlation IDs, or choosing log levels |
| Python Security | `/ceh-python-backend:python-security` | Secrets management, CORS, rate limiting, or session token generation |
| Alembic | `/ceh-python-backend:alembic` | Creating or running database migrations |

### TypeScript Frontend (`ceh-typescript-frontend`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Environment | `/ceh-typescript-frontend:environment` | Setting up the project, running scripts, or managing Bun dependencies |
| SvelteKit | `/ceh-typescript-frontend:sveltekit` | Working on routes, stores, components, or the API client |
| Frontend Testing | `/ceh-typescript-frontend:frontend-testing` | Writing Vitest, Testing Library, MSW, or Playwright tests |
| Accessibility | `/ceh-typescript-frontend:accessibility` | Writing Svelte component markup |
| Coding Style | `/ceh-typescript-frontend:coding-style` | Applying TypeScript type conventions, tsconfig, or import ordering |
| Linting | `/ceh-typescript-frontend:linting` | Configuring or running ESLint, Prettier, or svelte-check |

### Git Workflow (`ceh-git-workflow`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Branch | `/ceh-git-workflow:branch` | Creating or naming a branch |
| Commit | `/ceh-git-workflow:commit` | Writing a commit message or staging changes |
| Open PR | `/ceh-git-workflow:open-pr` | Opening a pull request or writing a PR description |
| Hotfix | `/ceh-git-workflow:hotfix` | Executing a critical production fix |
| Release | `/ceh-git-workflow:release` | Tagging a release or bumping a version |
| Gitignore | `/ceh-git-workflow:gitignore` | Creating or editing a `.gitignore` file |
| Code Review | `/ceh-git-workflow:code-review` | Reviewing a PR or leaving review comments |
| Dependency Management | `/ceh-git-workflow:dependency-management` | Adding or upgrading a package |

### Operations (`ceh-release-ops`)

| Skill | Phase | Invoke as | When to use |
|-------|-------|-----------|-------------|
| Observability | implementation | `/ceh-release-ops:observability` | Adding logging, metrics, or health check code |
| Database Migrations | implementation | `/ceh-release-ops:database-migrations` | Writing or running Alembic migrations |
| Definition of Done | implementation | `/ceh-release-ops:definition-of-done` | Preparing to open a pull request |
| Security | implementation | `/ceh-release-ops:security` | Handling secrets, CORS, rate limiting, or input validation |
| Versioning | release | `/ceh-release-ops:versioning` | Bumping a version, tagging a release, or classifying a change |
| Incidents | operational | `/ceh-release-ops:incidents` | Responding to a production incident or writing a post-mortem |
| Rollback | operational | `/ceh-release-ops:rollback` | Deciding to roll back a deployment or recovering from a failed migration |

### Summarize Chat (`ceh-summarize-chat`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Summarize Chat | `/ceh-summarize-chat:summarize-chat` | Summarizing the current session for handoff to a future LLM session |

### Lessons Learned (`ceh-lessons-learned`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Lessons Learned | `/ceh-lessons-learned:lessons-learned` | Extracting lessons learned from the current session into `LESSONS_LEARNED.md` |

### Blog (`ceh-blog`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| Blog Interviewer | `/ceh-blog:blog-interviewer` | Turn a rough idea, project, or experience into a compelling, publishable blog post |
| Blog Writer | `/ceh-blog:blog-writer` | Draft straight from existing notes, bullets, or outline — no interview |
| Blog Editor | `/ceh-blog:blog-editor` | Diagnose and polish an existing draft — diagnosis first, then a full revised version |
| Blog Repurpose | `/ceh-blog:blog-repurpose` | Adapt a finished post into Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb |

### Documentation (`ceh-documentation`)

| Skill | Invoke as | When to use |
|-------|-----------|-------------|
| User & Operator Guide | `/ceh-documentation:user-operator-guide` | Writing a user guide, operator runbook, getting-started/install/config guide, or troubleshooting reference |

---

## Agents

Agents run autonomously for a defined task and hand results back to the parent session.

> **Plugin-agent limitation:** every agent here ships inside a plugin. Claude Code
> **ignores** the `permissionMode`, `hooks`, and `mcpServers` frontmatter fields on
> plugin subagents (for security reasons). So `permissionMode: acceptEdits` in an agent
> file is a no-op — these agents still prompt for edit/write permissions. To grant them,
> use session `permissions.allow` in `settings.json`, not agent frontmatter. See the
> [subagents docs](https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope).

### Dev Tools (`ceh-dev-tools`)

| Agent | Invoke as | When to use |
|-------|-----------|-------------|
| Repo Tree Mapper | `/ceh-dev-tools:repo-tree-mapper` | Map or document a repository's structure; auto-triggers on orientation requests |

### Documentation (`ceh-documentation`)

| Agent | Invoke as | When to use |
|-------|-----------|-------------|
| Changelog Agent | `/ceh-documentation:changelog-agent` | Generate or update CHANGELOG.md, write release notes, summarize changes between versions |
| README Updater | `/ceh-documentation:readme-updater` | Refresh README after a significant change (new feature, changed install steps, new API surface) |

### Python Backend (`ceh-python-backend`)

| Agent | Invoke as | When to use |
|-------|-----------|-------------|
| Python Unit Tester | `/ceh-python-backend:python-unit-tester` | Write isolated pytest unit tests for functions, classes, or modules with mocked dependencies |
| Python Integration Tester | `/ceh-python-backend:python-integration-tester` | Write tests for real component interactions — DB, HTTP between internal services, service boundaries |
| Python System Tester | `/ceh-python-backend:python-system-tester` | Write full end-to-end / acceptance tests that exercise the entire application stack |

### TypeScript Frontend (`ceh-typescript-frontend`)

| Agent | Invoke as | When to use |
|-------|-----------|-------------|
| TS Unit Tester | `/ceh-typescript-frontend:ts-unit-tester` | Write isolated Vitest unit tests for functions, classes, and modules with mocked dependencies |
| TS Integration Tester | `/ceh-typescript-frontend:ts-integration-tester` | Write tests wiring real Svelte stores, MSW handlers, and multiple components together |
| TS System Tester | `/ceh-typescript-frontend:ts-system-tester` | Write Playwright E2E tests that exercise the full running stack as a real user would |

### Release Ops (`ceh-release-ops`)

| Agent | Invoke as | When to use |
|-------|-----------|-------------|
| GitHub Actions | `/ceh-release-ops:github-actions` | Create or fix GitHub Actions workflows, jobs, matrix builds, OIDC, reusable workflows |
| GitLab CI | `/ceh-release-ops:gitlab-ci` | Create or fix `.gitlab-ci.yml` pipelines, DAG stages, rules, protected variables, runners |

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
/plugin install ceh-blog@ceh-plugins --scope user
/plugin install ceh-documentation@ceh-plugins --scope user
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
    { "path": "~/agent-skills/ceh-dev-tools" },
    { "path": "~/agent-skills/ceh-blog" },
    { "path": "~/agent-skills/ceh-documentation" }
  ]
}
```
