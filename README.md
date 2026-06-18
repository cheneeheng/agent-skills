# CEH Agent Skills Plugins

A collection of Claude Code plugins providing engineering standards for AI coding agents. Plugins are
organized around **use cases** — load the ones that match what you are building.

---

## Plugins

| Plugin | Install as | Contents |
|--------|-----------|---------|
| Agent Coding Contract | `ceh-agent-coding-contract` | Behavioral contract for coding agents; write-less-code minimalism skill (always-on via hooks) |
| Plan Build Review | `ceh-plan-build-review` | Plan-driven development loop: plan a fullstack app, implement from the plan, review against it |
| Architecture | `ceh-architecture` | ADRs and domain modeling (stack-agnostic design) |
| Python Service | `ceh-python-service` | FastAPI, asyncpg, PostgreSQL, Alembic, uv, testing, observability, security |
| Python Library | `ceh-python-library` | Packaging, public API, semver, uv, testing (no web deps) |
| Web Frontend | `ceh-web-frontend` | SvelteKit + React (Vite), Bun, TS style, ESLint/Prettier, Vitest, Playwright, accessibility |
| Scaffolding | `ceh-scaffolding` | Per-project-type setup: directory layout + config + `.gitignore` |
| Git Workflow | `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review, dependency management |
| Ops | `ceh-ops` | Incident response, rollback, deploy pipeline; CI agents |
| Summarize Chat | `ceh-summarize-chat` | Structured session summary for LLM handoff |
| Lessons Learned | `ceh-lessons-learned` | Session retrospectives into `LESSONS_LEARNED.md` |
| Dev Tools | `ceh-dev-tools` | Repository exploration and codebase orientation agents |
| Blog | `ceh-blog` | Interview-driven blog post writing — from rough idea to publication-ready draft |
| Documentation | `ceh-documentation` | End-user/operator docs — user guides, runbooks, install/config, troubleshooting; changelog & README maintenance |
| Orchestration | `ceh-orchestration` | Thin-orchestrator mode for cost-optimized multi-step work: plan/delegate-only main session + executor/verifier subagents (and the built-in Explore agent) |
| Release Flow | `ceh-release-flow` | Orchestrate an end-to-end release in one pass: version bump → changelog → README → CLAUDE.md → PR → merge → tag → GitHub release, by sequencing the skills that own each step |

### Categorization

Plugins split on a single axis — **use case** — so you load exactly what your work needs. They fall
into three tiers:

| Tier | Loaded | Plugins |
|------|--------|---------|
| **Cross-cutting** | most sessions | `ceh-agent-coding-contract`, `ceh-git-workflow` |
| **Use-case workflow** | per activity | `ceh-plan-build-review`, `ceh-blog`, `ceh-documentation`, `ceh-ops`, `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-scaffolding`, `ceh-orchestration`, `ceh-release-flow` |
| **Stack / build** | per project type | `ceh-python-service`, `ceh-python-library`, `ceh-web-frontend`, `ceh-architecture` |

`ceh-dev-tools` is a standalone tooling plugin (agents only). Each plugin is self-contained: a
foundational standard needed by more than one plugin is duplicated into each rather than extracted
into a shared base, so one plugin per use case is all you load.

---

## Skills

| Plugin | Skill | Invoke as | When to use |
|--------|-------|-----------|-------------|
| `ceh-agent-coding-contract` | Agent Coding Contract | `/ceh-agent-coding-contract:agent-coding-contract` | Start of any coding session — core rules, five-step workflow, stop conditions, non-goals |
| `ceh-agent-coding-contract` | Write Less Code | `/ceh-agent-coding-contract:write-less-code` | Every coding session (auto — session-start load + per-turn reinforcement) — the minimalism ladder (YAGNI → stdlib → native → installed dep → one line) |
| `ceh-plan-build-review` | Plan Fullstack App Iteratively | `/ceh-plan-build-review:plan-fullstack-app-iteratively` | Planning one release at a time — a greenfield skeleton or the next iteration |
| `ceh-plan-build-review` | Plan Fullstack App to MVP | `/ceh-plan-build-review:plan-fullstack-app-to-mvp` | Planning the complete build to a working MVP in one session |
| `ceh-plan-build-review` | Implement From Plan | `/ceh-plan-build-review:implement-from-plan` | Implementing a SKELETON.md or ITER_NN.md planning document |
| `ceh-plan-build-review` | Review Against Plan | `/ceh-plan-build-review:review-against-plan` | Auditing implementation against a SKELETON.md or ITER_NN.md planning document |
| `ceh-architecture` | ADR | `/ceh-architecture:adr` | Making a significant architectural decision |
| `ceh-architecture` | Domain Modeling | `/ceh-architecture:domain-modeling` | Designing entities, IDs, status fields, or layer boundaries |
| `ceh-python-service` | FastAPI | `/ceh-python-service:fastapi` | Writing route handlers, DI, middleware, exception hierarchy, or REST API design |
| `ceh-python-service` | asyncpg | `/ceh-python-service:asyncpg` | Writing database queries, transactions, tenant isolation, or connection pool config |
| `ceh-python-service` | PostgreSQL | `/ceh-python-service:postgresql` | Designing a schema, choosing column types, or adding indexes |
| `ceh-python-service` | Alembic | `/ceh-python-service:alembic` | Creating or running database migrations; migration deploy safety |
| `ceh-python-service` | Python Service Environment | `/ceh-python-service:python-service-environment` | Setting up uv/pyproject.toml, writing type hints, configuring ruff/mypy |
| `ceh-python-service` | Python Service Testing | `/ceh-python-service:python-service-testing` | Writing Python unit or integration tests |
| `ceh-python-service` | Python Observability | `/ceh-python-service:python-observability` | Adding structlog logging, metrics, health checks, or correlation IDs |
| `ceh-python-service` | Python Security | `/ceh-python-service:python-security` | Secrets management, CORS, rate limiting, or input validation |
| `ceh-python-library` | Packaging | `/ceh-python-library:packaging` | Build backend, src layout, wheels/sdist, publishing to PyPI |
| `ceh-python-library` | Public API | `/ceh-python-library:public-api` | Defining `__all__`, changing a public signature, classifying a semver bump |
| `ceh-python-library` | Python Library Environment | `/ceh-python-library:python-library-environment` | Setting up uv/pyproject.toml for a library (no web deps) |
| `ceh-python-library` | Python Library Testing | `/ceh-python-library:python-library-testing` | Writing unit and public-API tests for a library |
| `ceh-web-frontend` | Environment | `/ceh-web-frontend:environment` | Bun/Vite setup, TypeScript style, ESLint/Prettier, type config |
| `ceh-web-frontend` | SvelteKit | `/ceh-web-frontend:sveltekit` | Working on Svelte routes, stores, components, or the API client |
| `ceh-web-frontend` | React + Vite | `/ceh-web-frontend:react-vite` | Working on React components, hooks, routing, or Vite config |
| `ceh-web-frontend` | Frontend Testing | `/ceh-web-frontend:frontend-testing` | Writing Vitest, Testing Library, MSW, or Playwright tests |
| `ceh-web-frontend` | Accessibility | `/ceh-web-frontend:accessibility` | Writing component markup (Svelte or React) |
| `ceh-scaffolding` | Scaffold Python Service | `/ceh-scaffolding:scaffold-python-service` | Starting a FastAPI/Python web service repo |
| `ceh-scaffolding` | Scaffold Python Library | `/ceh-scaffolding:scaffold-python-library` | Starting a distributable Python library/package |
| `ceh-scaffolding` | Scaffold Web Frontend | `/ceh-scaffolding:scaffold-web-frontend` | Starting a SvelteKit or React + Vite frontend |
| `ceh-scaffolding` | Scaffold Fullstack Web | `/ceh-scaffolding:scaffold-fullstack-web` | Starting a fullstack web app (service + frontend in one repo) |
| `ceh-git-workflow` | Branch | `/ceh-git-workflow:branch` | Creating or naming a branch |
| `ceh-git-workflow` | Commit | `/ceh-git-workflow:commit` | Writing a commit message or staging changes |
| `ceh-git-workflow` | Open PR | `/ceh-git-workflow:open-pr` | Opening a pull request, writing a PR description, or checking the definition of done |
| `ceh-git-workflow` | Merge | `/ceh-git-workflow:merge` | Merging a PR and deleting the branch afterward |
| `ceh-git-workflow` | Hotfix | `/ceh-git-workflow:hotfix` | Executing a critical production fix |
| `ceh-git-workflow` | Release | `/ceh-git-workflow:release` | Tagging a release or bumping a version |
| `ceh-git-workflow` | Code Review | `/ceh-git-workflow:code-review` | Reviewing a PR or leaving review comments |
| `ceh-git-workflow` | Dependency Management | `/ceh-git-workflow:dependency-management` | Adding or upgrading a package |
| `ceh-ops` | Deploy | `/ceh-ops:deploy` | Building/promoting images, staging→prod, post-deploy health checks, change classification |
| `ceh-ops` | Incidents | `/ceh-ops:incidents` | Responding to a production incident or writing a post-mortem |
| `ceh-ops` | Rollback | `/ceh-ops:rollback` | Deciding to roll back a deployment or recovering from a failed migration |
| `ceh-summarize-chat` | Summarize Chat | `/ceh-summarize-chat:summarize-chat` | Summarizing the current session for handoff to a future LLM session |
| `ceh-lessons-learned` | Lessons Learned | `/ceh-lessons-learned:lessons-learned` | Extracting lessons learned from the current session into `LESSONS_LEARNED.md` |
| `ceh-blog` | Blog Interviewer | `/ceh-blog:blog-interviewer` | Turn a rough idea, project, or experience into a compelling, publishable blog post |
| `ceh-blog` | Blog Writer | `/ceh-blog:blog-writer` | Draft straight from existing notes, bullets, or outline — no interview |
| `ceh-blog` | Blog Editor | `/ceh-blog:blog-editor` | Diagnose and polish an existing draft — diagnosis first, then a full revised version |
| `ceh-blog` | Blog Repurpose | `/ceh-blog:blog-repurpose` | Adapt a finished post into Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb |
| `ceh-documentation` | User & Operator Guide | `/ceh-documentation:user-operator-guide` | Writing a user guide, operator runbook, getting-started/install/config guide, or troubleshooting reference |
| `ceh-documentation` | Update Changelog | `/ceh-documentation:update-changelog` | Generate or update CHANGELOG.md, write release notes, summarize changes between versions |
| `ceh-documentation` | Update README | `/ceh-documentation:update-readme` | Refresh README after a significant change (new feature, changed install steps, new API surface) |
| `ceh-orchestration` | Orchestrate | `/ceh-orchestration:orchestrate` | Decompose and delegate a big multi-step task — plan/delegate-only main session, cheap isolated workers, to cap context/token cost |
| `ceh-release-flow` | Release Flow | `/ceh-release-flow:release-flow` | Ship a complete release in one pass — version bump → changelog → README → CLAUDE.md → PR → merge → tag → release, sequencing the skill that owns each step |
| `ceh-release-flow` | Direct Release Flow | `/ceh-release-flow:direct-release-flow` | PR-less variant — same release pipeline directly on `main` (no branch/PR/merge): version bump → changelog → README → CLAUDE.md → commit → tag → release |

---

## Agents

Agents run autonomously for a defined task and hand results back to the parent session.

> **Plugin-agent limitation:** every agent here ships inside a plugin. Claude Code
> **ignores** the `permissionMode`, `hooks`, and `mcpServers` frontmatter fields on
> plugin subagents (for security reasons). So `permissionMode: acceptEdits` in an agent
> file is a no-op — these agents still prompt for edit/write permissions. To grant them,
> use session `permissions.allow` in `settings.json`, not agent frontmatter. See the
> [subagents docs](https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope).

| Plugin | Agent | Invoke as | When to use |
|--------|-------|-----------|-------------|
| `ceh-dev-tools` | Repo Tree Mapper | `/ceh-dev-tools:repo-tree-mapper` | Map or document a repository's structure; auto-triggers on orientation requests |
| `ceh-python-service` | Python Unit Tester | `/ceh-python-service:python-unit-tester` | Write isolated pytest unit tests for functions, classes, or modules with mocked dependencies |
| `ceh-python-service` | Python Integration Tester | `/ceh-python-service:python-integration-tester` | Write tests for real component interactions — DB, HTTP between internal services, service boundaries |
| `ceh-python-service` | Python System Tester | `/ceh-python-service:python-system-tester` | Write full end-to-end / acceptance tests that exercise the entire application stack |
| `ceh-web-frontend` | TS Unit Tester | `/ceh-web-frontend:ts-unit-tester` | Write isolated Vitest unit tests for functions, classes, and modules with mocked dependencies |
| `ceh-web-frontend` | TS Integration Tester | `/ceh-web-frontend:ts-integration-tester` | Write tests wiring real stores, MSW handlers, and multiple components together |
| `ceh-web-frontend` | TS System Tester | `/ceh-web-frontend:ts-system-tester` | Write Playwright E2E tests that exercise the full running stack as a real user would |
| `ceh-ops` | GitHub Actions | `/ceh-ops:github-actions` | Create or fix GitHub Actions workflows, jobs, matrix builds, OIDC, reusable workflows |
| `ceh-ops` | GitLab CI | `/ceh-ops:gitlab-ci` | Create or fix `.gitlab-ci.yml` pipelines, DAG stages, rules, protected variables, runners |
| `ceh-orchestration` | Executor | `/ceh-orchestration:executor` | Implement a single scoped task: code changes, edits, multi-step work (Sonnet) |
| `ceh-orchestration` | Verifier | `/ceh-orchestration:verifier` | Check an executor's output against acceptance criteria — PASS/FAIL only (Haiku) |

---


## Installing in Claude Code

### Step 1 — Add the marketplace

```
/plugin marketplace add cheneeheng/agent-skills
```

### Step 2 — Install plugins

Install individual plugins for the use cases you need:

```
/plugin install ceh-agent-coding-contract@ceh-plugins --scope user
/plugin install ceh-plan-build-review@ceh-plugins --scope user
/plugin install ceh-git-workflow@ceh-plugins --scope user
/plugin install ceh-architecture@ceh-plugins --scope user
/plugin install ceh-python-service@ceh-plugins --scope user
/plugin install ceh-python-library@ceh-plugins --scope user
/plugin install ceh-web-frontend@ceh-plugins --scope user
/plugin install ceh-scaffolding@ceh-plugins --scope user
/plugin install ceh-ops@ceh-plugins --scope user
/plugin install ceh-summarize-chat@ceh-plugins --scope user
/plugin install ceh-lessons-learned@ceh-plugins --scope user
/plugin install ceh-dev-tools@ceh-plugins --scope user
/plugin install ceh-blog@ceh-plugins --scope user
/plugin install ceh-documentation@ceh-plugins --scope user
/plugin install ceh-orchestration@ceh-plugins --scope user
/plugin install ceh-release-flow@ceh-plugins --scope user
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
    { "path": "~/agent-skills/ceh-agent-coding-contract" },
    { "path": "~/agent-skills/ceh-plan-build-review" },
    { "path": "~/agent-skills/ceh-git-workflow" },
    { "path": "~/agent-skills/ceh-architecture" },
    { "path": "~/agent-skills/ceh-python-service" },
    { "path": "~/agent-skills/ceh-python-library" },
    { "path": "~/agent-skills/ceh-web-frontend" },
    { "path": "~/agent-skills/ceh-scaffolding" },
    { "path": "~/agent-skills/ceh-ops" },
    { "path": "~/agent-skills/ceh-summarize-chat" },
    { "path": "~/agent-skills/ceh-lessons-learned" },
    { "path": "~/agent-skills/ceh-dev-tools" },
    { "path": "~/agent-skills/ceh-blog" },
    { "path": "~/agent-skills/ceh-documentation" },
    { "path": "~/agent-skills/ceh-orchestration" },
    { "path": "~/agent-skills/ceh-release-flow" }
  ]
}
```

---

## Tools

| Tool | Path | Purpose |
|------|------|---------|
| skills-sync | `tools/skills-sync/` | Copy individual skills (from this repo or any other) into a project's `.claude/skills/` directory — install, update, add, remove, list. Python, bash, PowerShell, and browser-based HTML implementations. |

`tools/` holds standalone meta-tooling that isn't itself a `ceh-*` plugin, skill, or agent — see
`tools/skills-sync/README.md` for usage.
