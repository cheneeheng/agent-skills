# CEH Agent Skills Plugins

A collection of Claude Code plugins providing engineering standards for AI coding agents. Plugins are
organized around **use cases** — load the ones that match what you are building.

**Guides:** [`docs/TESTING_WORKFLOW.md`](docs/TESTING_WORKFLOW.md) — how `ceh-testing` and the three stack
testing skills route between each other, with the trigger phrases and sequence for each moment.

---

## Plugins

| Plugin | Install as | Contents |
|--------|-----------|---------|
| Agent Coding Contract | `ceh-agent-coding-contract` | Behavioral contract for coding agents (always-on via SessionStart hook, and preloaded into the `executor`, `github-actions` and `gitlab-ci` subagents); write-less-code minimalism skill (always-on via hooks); retroactive refactoring (`shrink-diff`, `refactor-repo`); usage-limit guard + handoff (`usage-limit-handoff`); explaining code to a person until it lands (`explain-until-understood`) |
| Plan Build Review | `ceh-plan-build-review` | Plan-driven development loop: plan a fullstack app, implement from the plan, review against it |
| Architecture | `ceh-architecture` | Living architecture docs (Mermaid diagrams + Key Decisions) and domain modeling (stack-agnostic design) |
| Python Service | `ceh-python-service` | FastAPI, asyncpg, PostgreSQL, Alembic, uv, testing, observability, security |
| Python Library | `ceh-python-library` | Packaging, public API, semver, uv, testing (no web deps) |
| Web Frontend | `ceh-web-frontend` | SvelteKit + React (Vite), Bun, TS style, ESLint/Prettier, Vitest, Playwright, accessibility |
| Scaffolding | `ceh-scaffolding` | Per-project-type setup: directory layout + config + `.gitignore` |
| Git Workflow | `ceh-git-workflow` | Commits, branching, PRs, merging, releases, code review, dependency management |
| Ops | `ceh-ops` | Incident response, rollback, deploy pipeline; CI agents |
| Summarize Chat | `ceh-summarize-chat` | Structured session summary for LLM handoff |
| Lessons Learned | `ceh-lessons-learned` | Session retrospectives into `LESSONS_LEARNED.md` |
| Dev Tools | `ceh-dev-tools` | Repository exploration and codebase orientation — explain a whole repo component by component into `.agents_workspace/CODEBASE_EXPLAINED.md`, or map its structure into `REPO_MAP.md` |
| Blog | `ceh-blog` | Interview-driven blog post writing — from rough idea to publication-ready draft |
| Documentation | `ceh-documentation` | End-user/operator docs — user guides, runbooks, install/config, troubleshooting; changelog & README maintenance |
| SEO | `ceh-seo` | SEO/GEO discoverability for anything internet-exposed — public web pages (meta, structured data, sitemap, llms.txt, rendering) and public-facing text (README first screen, package descriptions, repo topics) |
| Orchestration | `ceh-orchestration` | Thin-orchestrator mode for cost-optimized multi-step work: plan/delegate-only main session + executor/verifier subagents (and the built-in Explore agent) |
| Release Flow | `ceh-release-flow` | Orchestrate an end-to-end release in one pass: version bump → changelog → README → CLAUDE.md → PR → merge → tag → GitHub release, by sequencing the skills that own each step |
| Business Plan | `ceh-business-plan` | Turn a product idea or app plan into a validated business plan via a product-market-fit interview loop — draft, interrogate the weakest assumption, revise until a PMF gate passes |
| Evaluation | `ceh-evaluation` | Evaluate a skill or plugin you just wrote — derive its own criteria, measure structure/triggering/content/behavioral lift with evidence, loop fix→re-run until a readiness gate passes |
| Fabled | `ceh-fabled` | Frontier-grade reasoning discipline for any non-trivial task — deliberate thinking, alternative generation, adversarial self-review, verification, calibrated conviction |
| Advisor | `ceh-advisor` | Stronger-model second-opinion subagent for decision points, failure loops, irreversible actions, and pre-completion gates — plus hook backstops (destructive-command guard, failure watch) |
| Testing | `ceh-testing` | Stack-agnostic testing technique — reproduce-first bug fixes and bisection, systematic test-case design (partitions, boundaries, properties, metamorphic, fuzzing), suite audits (assertions, mutation, flakiness), behavior-preservation checks for refactors, and a pre-completion risk gate |
| Usability Audit | `ceh-usability-audit` | Measure whether a non-expert can actually use what you built — cold persona-constrained walkthroughs (`novice-walker`), a five-question interface audit across web UI/CLI/library/app surfaces, error-message rewrites, and a plain-language pass |

### Categorization

Plugins split on a single axis — **use case** — so you load exactly what your work needs. They fall
into three tiers:

| Tier | Loaded | Plugins |
|------|--------|---------|
| **Cross-cutting** | most sessions | `ceh-agent-coding-contract`, `ceh-git-workflow`, `ceh-fabled`, `ceh-advisor`, `ceh-testing` |
| **Use-case workflow** | per activity | `ceh-plan-build-review`, `ceh-blog`, `ceh-business-plan`, `ceh-evaluation`, `ceh-usability-audit`, `ceh-documentation`, `ceh-seo`, `ceh-ops`, `ceh-summarize-chat`, `ceh-lessons-learned`, `ceh-scaffolding`, `ceh-orchestration`, `ceh-release-flow` |
| **Stack / build** | per project type | `ceh-python-service`, `ceh-python-library`, `ceh-web-frontend`, `ceh-architecture` |

`ceh-dev-tools` is a standalone tooling plugin. Each plugin is self-contained: a
foundational standard needed by more than one plugin is duplicated into each rather than extracted
into a shared base, so one plugin per use case is all you load. Cross-cutting plugins are the
orthogonal tier — they hold a discipline that applies whatever you are building, so they load
*alongside* a use-case plugin rather than instead of one.

---

## Skills

| Plugin | Skill | Invoke as | When to use |
|--------|-------|-----------|-------------|
| `ceh-agent-coding-contract` | Agent Coding Contract | `/ceh-agent-coding-contract:agent-coding-contract` | Start of any coding session — core rules, five-step workflow, stop conditions, non-goals |
| `ceh-agent-coding-contract` | Write Less Code | `/ceh-agent-coding-contract:write-less-code` | Every coding session (auto — session-start load + per-turn reinforcement) — the minimalism ladder (YAGNI → stdlib → native → installed dep → one line) |
| `ceh-agent-coding-contract` | Shrink Diff | `/ceh-agent-coding-contract:shrink-diff` | Branch functionally done, before the PR — retroactively apply write-less-code to the accumulated diff vs `main` |
| `ceh-agent-coding-contract` | Refactor Repo | `/ceh-agent-coding-contract:refactor-repo` | Manual only — propose-then-apply refactor campaign over the whole repo or a named module |
| `ceh-agent-coding-contract` | Usage Limit Handoff | `/ceh-agent-coding-contract:usage-limit-handoff` | Auto via PostToolUse guard hook when 5h or weekly usage crosses the threshold (default 90%) — stop cleanly, write a handoff artifact for the next session, end the turn |
| `ceh-agent-coding-contract` | Explain Until Understood | `/ceh-agent-coding-contract:explain-until-understood` | Manual only — explain a subsystem, design, or diff to the person in the session, starting from the assumption they know nothing about it: a stated floor, foundations first, plain language, verified claims, ASCII for structure and time, and the escalation ladder when an explanation misses |
| `ceh-plan-build-review` | Plan Fullstack App Iteratively | `/ceh-plan-build-review:plan-fullstack-app-iteratively` | Planning one release at a time — a greenfield skeleton or the next iteration |
| `ceh-plan-build-review` | Plan Fullstack App to MVP | `/ceh-plan-build-review:plan-fullstack-app-to-mvp` | Planning the complete build to a working MVP in one session |
| `ceh-plan-build-review` | Implement From Plan | `/ceh-plan-build-review:implement-from-plan` | Implementing a SKELETON.md or ITER_NN.md planning document |
| `ceh-plan-build-review` | Review Against Plan | `/ceh-plan-build-review:review-against-plan` | Auditing implementation against a SKELETON.md or ITER_NN.md planning document |
| `ceh-plan-build-review` | Patch Built Version | `/ceh-plan-build-review:patch-built-version` | Patching an already-implemented version — a small, non-feature change recorded as a patch ITER_NN.md; routes features to the iterative planner |
| `ceh-architecture` | Document Architecture | `/ceh-architecture:document-architecture` | Writing/updating the living `ARCHITECTURE.md` — Mermaid diagrams + a Key Decisions log |
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
| `ceh-web-frontend` | UI Design | `/ceh-web-frontend:ui-design` | Frontend UI visual design — layout, hierarchy, navigation, states, finishing recipes for first-pass polish, plus theme/brand from bundled templates |
| `ceh-scaffolding` | Scaffold Python Service | `/ceh-scaffolding:scaffold-python-service` | Starting a FastAPI/Python web service repo |
| `ceh-scaffolding` | Scaffold Python Library | `/ceh-scaffolding:scaffold-python-library` | Starting a distributable Python library/package |
| `ceh-scaffolding` | Scaffold Web Frontend | `/ceh-scaffolding:scaffold-web-frontend` | Starting a SvelteKit or React + Vite frontend |
| `ceh-scaffolding` | Scaffold Fullstack Web | `/ceh-scaffolding:scaffold-fullstack-web` | Starting a fullstack web app (service + frontend in one repo) |
| `ceh-git-workflow` | Branch | `/ceh-git-workflow:branch` | Creating or naming a branch |
| `ceh-git-workflow` | Commit | `/ceh-git-workflow:commit` | Writing a commit message or staging changes |
| `ceh-git-workflow` | Open PR | `/ceh-git-workflow:open-pr` | Opening a pull request, writing a PR description, checking the definition of done, or enabling auto-merge on repos that allow it |
| `ceh-git-workflow` | Merge | `/ceh-git-workflow:merge` | Merging a PR (immediate or auto-merge) or a local branch into `main`, then deleting the branch afterward |
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
| `ceh-dev-tools` | Explain Codebase | `/ceh-dev-tools:explain-codebase` | Go through a whole repo and write what each component does, how they connect, and key flows into git-ignored `.agents_workspace/CODEBASE_EXPLAINED.md` (per-file detail only on request) |
| `ceh-seo` | Web Discoverability | `/ceh-seo:web-discoverability` | Shipping a public web page/route — head checklist, sitemap/robots/llms.txt, JSON-LD, SSR/prerender, GEO citation rules |
| `ceh-seo` | Text Discoverability | `/ceh-seo:text-discoverability` | Writing public-facing repo/package text — README first screen, one-liner, GitHub topics, PyPI/npm descriptions and keywords |
| `ceh-orchestration` | Orchestrate | `/ceh-orchestration:orchestrate` | Decompose and delegate a big multi-step task — plan/delegate-only main session, cheap isolated workers, to cap context/token cost |
| `ceh-release-flow` | Release Flow | `/ceh-release-flow:release-flow` | Ship a complete release in one pass — version bump → changelog → README → CLAUDE.md → PR → merge → tag → release, sequencing the skill that owns each step |
| `ceh-release-flow` | Direct Release Flow | `/ceh-release-flow:direct-release-flow` | PR-less variant — same release pipeline directly on `main` (no branch/PR/merge): version bump → changelog → README → CLAUDE.md → commit → tag → release |
| `ceh-business-plan` | Develop Business Plan | `/ceh-business-plan:develop-business-plan` | Draft a business plan proactively from app plans or a product idea, then loop interview→revise until the product-market-fit readiness gate passes |
| `ceh-evaluation` | Evaluate Skill | `/ceh-evaluation:evaluate-skill` | Evaluate a skill or plugin you wrote — derive its criteria, measure structure/triggering/content/behavioral lift with evidence, loop fix→re-run until a 6-point gate passes |
| `ceh-evaluation` | Evaluate Skill — Lite | `/ceh-evaluation:evaluate-skill-lite` | Fast dev-loop check — structure + triggering (single pass) + content only; skips behavioral lift, reports a partial 4/6 gate for cheap iteration before the full ship verdict |
| `ceh-fabled` | Fabled | `/ceh-fabled:fabled` | Any non-trivial task with more than one plausible answer — deliberate reasoning, alternatives, adversarial self-review, verification, and calibrated conviction |
| `ceh-fabled` | Fabled Plan Review | `/ceh-fabled:fabled-plan-review` | Review an existing plan against frontier-grade planning discipline — problem fidelity, alternatives, decomposition, pre-mortem, verifiability — verdict plus concrete fixes |
| `ceh-fabled` | Fabled Stuck | `/ceh-fabled:fabled-stuck` | Escape a failure loop after repeated failed fixes — freeze, inventory attempts, attack their shared assumption, re-derive the diagnosis from evidence, probe before fixing |
| `ceh-testing` | Test a Bug Fix | `/ceh-testing:test-a-bug-fix` | Fixing a bug, crash, regression, or incident — reproduce-first: failing test before the fix, prove the test is coupled to it, bisect on it when the behavior used to work |
| `ceh-testing` | Design Test Cases | `/ceh-testing:design-test-cases` | Choosing which inputs and scenarios to cover — partitions, boundaries, decision tables, state transitions, pairwise, properties, metamorphic relations, fuzzing, forced dependency failure |
| `ceh-testing` | Audit Test Suite | `/ceh-testing:audit-test-suite` | Deciding whether a passing suite would actually catch a defect — assertion audit, delete-the-code check, mutation testing on the diff, flakiness, branch coverage |
| `ceh-testing` | Verify Behavior Preserved | `/ceh-testing:verify-behavior-preserved` | Before a no-behavior-change edit (refactor, extraction, dependency/runtime upgrade, port) — characterization tests, golden files, differential run |
| `ceh-testing` | Close Test Risk Gaps | `/ceh-testing:close-test-risk-gaps` | Pre-completion gate — triage concurrency/idempotency, contract drift, performance regression, authorization, and migration/rolling-deploy compatibility; skip each class explicitly when its trigger does not fire |
| `ceh-usability-audit` | First-Run Walkthrough | `/ceh-usability-audit:first-run-walkthrough` | Can a stranger reach first success — install, sign-up, setup, onboarding; cold persona walkers, ranked by observed stalls, milestones capped by an action budget set before the walk, looped to a 5-point gate |
| `ceh-usability-audit` | Audit Interface | `/ceh-usability-audit:audit-interface` | They are already in — the five questions every web UI/CLI/API/screen must answer unasked, a reject-on-sight anti-pattern sweep, the naming test, and the persona battery |
| `ceh-usability-audit` | Audit Error Messages | `/ceh-usability-audit:audit-error-messages` | Anything a user reads when something goes wrong — the three-part rule (what happened, what was wrong, what to do next) over every user-reachable string |
| `ceh-usability-audit` | Plain Language Pass | `/ceh-usability-audit:plain-language-pass` | Labels, help text, empty states, confirmation dialogs, onboarding copy — vocabulary floor, sentence rules, and an explicit never-simplify list |
| `ceh-fabled` | Fabled Voice | `/ceh-fabled:fabled-voice` | Always-on via SessionStart hook — deliver in fable's writing style — finding-first progress lines, verdict-first advisory answers closing on a calibration, and reports built from bold inline labels, hard numbers, a validated/not-validated ledger, and a standing offer |

---

## Agents

Agents run autonomously for a defined task and hand results back to the parent session.

> **Plugin-agent limitation:** every agent here ships inside a plugin. Claude Code
> **ignores** the `permissionMode`, `hooks`, and `mcpServers` frontmatter fields on
> plugin subagents (for security reasons), so no agent in this repo sets them. These
> agents inherit the permission context of your session and prompt for edit/write
> permissions accordingly. To avoid the prompts, put the session in `acceptEdits`
> (`Shift+Tab`) before dispatching — a parent `acceptEdits` or `bypassPermissions` takes
> precedence and is inherited — or add `permissions.allow` rules in `settings.json`. See
> the [subagents docs](https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope).
>
> **Background tool filter:** subagents run in the background by default, and a background
> subagent keeps only `Read`, `Grep`, `Glob`, `Bash`, `PowerShell`, `Edit`, `Write`,
> `NotebookEdit`, `WebFetch`, `WebSearch`, `TodoWrite`, `Skill`, `ToolSearch`,
> `EnterWorktree`, `ExitWorktree`, `Monitor`, `TaskStop`, `SendMessage`, and `Artifact`.
> Anything else is stripped silently, even when named in `tools:`. `AskUserQuestion` is
> removed from every subagent, so no agent here can stop to ask you a question.

| Plugin | Agent | Invoke as | When to use |
|--------|-------|-----------|-------------|
| `ceh-dev-tools` | Repo Tree Mapper | `/ceh-dev-tools:repo-tree-mapper` | Map or document a repository's structure; auto-triggers on orientation requests |
| `ceh-python-service` | Python Unit Tester | `/ceh-python-service:python-unit-tester` | Write isolated pytest unit tests for functions, classes, or modules with mocked dependencies |
| `ceh-python-service` | Python Integration Tester | `/ceh-python-service:python-integration-tester` | Write tests for real component interactions — DB, HTTP between internal services, service boundaries |
| `ceh-python-service` | Python System Tester | `/ceh-python-service:python-system-tester` | Write full end-to-end / acceptance tests that exercise the entire application stack |
| `ceh-web-frontend` | TS Unit Tester | `/ceh-web-frontend:ts-unit-tester` | Write isolated Vitest unit tests for functions, classes, and modules with mocked dependencies |
| `ceh-web-frontend` | TS Integration Tester | `/ceh-web-frontend:ts-integration-tester` | Write tests wiring real stores, MSW handlers, and multiple components together |
| `ceh-web-frontend` | TS System Tester | `/ceh-web-frontend:ts-system-tester` | Write Playwright E2E tests that exercise the full running stack as a real user would |
| `ceh-testing` | Test Suite Auditor | `/ceh-testing:test-suite-auditor` | Run the slow, high-output suite audit out of session — mutation testing on the diff, flakiness and isolation runs — and hand back a ranked read-only report (Sonnet) |
| `ceh-git-workflow` | Commit Author | `/ceh-git-workflow:commit-author` | Create one commit in an isolated subagent; derives the change from git diff, pass only the why (Sonnet, medium effort) |
| `ceh-git-workflow` | PR Opener | `/ceh-git-workflow:pr-opener` | Push the branch and open the PR in an isolated subagent; queues auto-merge where allowed (Sonnet, medium effort) |
| `ceh-git-workflow` | Branch Merger | `/ceh-git-workflow:branch-merger` | Merge a PR or local branch into `main` and clean up, gate-checked, in an isolated subagent (Sonnet, medium effort) |
| `ceh-git-workflow` | Release Cutter | `/ceh-git-workflow:release-cutter` | Tag `main` and publish the release in an isolated subagent; bump commit only if not landed (Sonnet, medium effort) |
| `ceh-ops` | GitHub Actions | `/ceh-ops:github-actions` | Create or fix GitHub Actions workflows, jobs, matrix builds, OIDC, reusable workflows |
| `ceh-ops` | GitLab CI | `/ceh-ops:gitlab-ci` | Create or fix `.gitlab-ci.yml` pipelines, DAG stages, rules, protected variables, runners |
| `ceh-orchestration` | Executor | `/ceh-orchestration:executor` | Implement a single scoped task: code changes, edits, multi-step work (Sonnet) |
| `ceh-orchestration` | Verifier | `/ceh-orchestration:verifier` | Check an executor's output against acceptance criteria — PASS/FAIL only (Haiku) |
| `ceh-usability-audit` | Novice Walker | `/ceh-usability-audit:novice-walker` | Walk a target cold under one persona toward one goal and report where it stalled — may not use what it already knows about how such tools usually work (Sonnet, read-only) |
| `ceh-advisor` | Advisor | `/ceh-advisor:ceh-advisor` | Verdict-first second opinion before an architectural commit, after 2+ failed fixes, before an irreversible action, or before declaring a complex task done (Opus, high effort); requires a handoff block — also hard-triggered by the plugin's hooks on destructive commands and failure streaks |

---


## Installing in Claude Code

### Prerequisites

`python3` on `PATH` — required by the hooks in `ceh-advisor` and `ceh-agent-coding-contract`
(`ceh-fabled`'s SessionStart hook needs only `bash`)
(stdlib only, no packages). Every other plugin works without it.

This matters most for `ceh-advisor`: its destructive-command guard **fails closed**, so without
`python3` it blocks every `rm -rf`, `git push --force`, `terraform destroy`, and similar until the
interpreter is available. Install with `winget install Python.Python.3.12` / `brew install python`
/ `apt install python3`.

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
/plugin install ceh-business-plan@ceh-plugins --scope user
/plugin install ceh-evaluation@ceh-plugins --scope user
/plugin install ceh-fabled@ceh-plugins --scope user
/plugin install ceh-advisor@ceh-plugins --scope user
/plugin install ceh-testing@ceh-plugins --scope user
/plugin install ceh-usability-audit@ceh-plugins --scope user
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
    { "path": "~/agent-skills/plugins/ceh-agent-coding-contract" },
    { "path": "~/agent-skills/plugins/ceh-plan-build-review" },
    { "path": "~/agent-skills/plugins/ceh-git-workflow" },
    { "path": "~/agent-skills/plugins/ceh-architecture" },
    { "path": "~/agent-skills/plugins/ceh-python-service" },
    { "path": "~/agent-skills/plugins/ceh-python-library" },
    { "path": "~/agent-skills/plugins/ceh-web-frontend" },
    { "path": "~/agent-skills/plugins/ceh-scaffolding" },
    { "path": "~/agent-skills/plugins/ceh-ops" },
    { "path": "~/agent-skills/plugins/ceh-summarize-chat" },
    { "path": "~/agent-skills/plugins/ceh-lessons-learned" },
    { "path": "~/agent-skills/plugins/ceh-dev-tools" },
    { "path": "~/agent-skills/plugins/ceh-blog" },
    { "path": "~/agent-skills/plugins/ceh-documentation" },
    { "path": "~/agent-skills/plugins/ceh-orchestration" },
    { "path": "~/agent-skills/plugins/ceh-release-flow" },
    { "path": "~/agent-skills/plugins/ceh-business-plan" },
    { "path": "~/agent-skills/plugins/ceh-evaluation" },
    { "path": "~/agent-skills/plugins/ceh-fabled" },
    { "path": "~/agent-skills/plugins/ceh-advisor" },
    { "path": "~/agent-skills/plugins/ceh-seo" },
    { "path": "~/agent-skills/plugins/ceh-testing" },
    { "path": "~/agent-skills/plugins/ceh-usability-audit" }
  ]
}
```

---

## Tools

| Tool | Path | Purpose |
|------|------|---------|
| skills-sync | `tools/skills-sync/` | Copy individual skills (from this repo or any other) into a project's `.claude/skills/` directory — install, update, add, remove, list. Python, bash, PowerShell, and browser-based HTML implementations. |
| validate-plugins | `tools/validate-plugins/` | Repo-integrity checker run by CI (`.github/workflows/validate.yml`): validates plugin manifests, skill/agent frontmatter (including a 1024-char cap on `description`), file and skill references, and script syntax. Stdlib-only Python. |

`tools/` holds standalone meta-tooling that isn't itself a `ceh-*` plugin, skill, or agent — see
`tools/skills-sync/README.md` for usage.
