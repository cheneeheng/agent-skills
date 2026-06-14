# Changelog

Versions follow [Semantic Versioning](https://semver.org/).
Versions refer to the Marketplace versions.

---

## [3.7.0] — 2026-06-14

New `write-less-code` skill in `ceh-agent-coding-contract`: the positive half of minimalism
(the contract already owns the negative rules), wired always-on via session-start load plus a
per-turn reinforcement hook.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.6.0 |

### Added

- **`ceh-agent-coding-contract`** (v2.6.0) — new skill `write-less-code`.
  - The minimalism ladder (YAGNI → stdlib → native platform feature → already-installed
    dependency → one line → minimum that works), native-platform-first, and the `// less-code:`
    shortcut convention. Framed as the *positive* delta over the contract's "Universal Non-Goals"
    (no new deps, no speculative abstractions, minimal diffs), not a restatement. Inspired by
    [ponytail](https://github.com/DietrichGebert/ponytail) (MIT, DietrichGebert).
  - Loaded at session start via a new `SessionStart` hook (`load-less-code.js`, firing on
    `startup`/`resume`/`clear`/`compact`) and reinforced every turn via a `UserPromptSubmit` hook
    (`less-code-payload.js`) that re-injects a compact ladder digest, so the reflex survives
    long-session context drift. No configuration or env var required.

---

## [3.6.0] — 2026-06-13

New `ceh-orchestration` plugin: consolidates a thin-orchestrator setup (cost-optimized,
delegate-only main session plus worker subagents) into the marketplace.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-orchestration` | v1.0.0 |

### Added

- **`ceh-orchestration`** (v1.0.0) — new plugin.
  - Skill `orchestrate` — thin-orchestrator mode: the main session restates the goal,
    decomposes into a dependency-ordered plan, dispatches subtasks to workers, and keeps a
    compact result ledger while doing no file I/O itself. Covers the context-isolation cost
    model, model routing (Opus → Sonnet → Haiku), spec discipline, ranked cost levers, and
    why subagents beat Agent Teams for a cost goal.
  - Agents `executor` (Sonnet, scoped implementation) and `verifier` (Haiku, PASS/FAIL
    acceptance check) — the workers the skill dispatches to. Both are scoped to
    thin-orchestrator mode and do not auto-invoke outside it, so installing the plugin does
    not divert ordinary edits into a subagent. Read-only exploration is delegated to Claude
    Code's built-in `Explore` agent (no custom explorer ships), since it skips `CLAUDE.md`
    inheritance and so carries the least context tax.

---

## [3.5.0] — 2026-06-11

Duplicated skill names made unique across plugins: the `python-environment` / `python-testing`
pairs shared by `ceh-python-service` and `ceh-python-library` are renamed to plugin-qualified
names so each skill name maps to exactly one plugin.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-python-service` | v3.1.0 |
| `ceh-python-library` | v1.2.0 |
| `ceh-scaffolding` | v1.0.1 |
| `ceh-web-frontend` | v3.0.3 |

### Changed

- **`ceh-python-service`** (v3.1.0) — skills renamed: `python-environment` →
  `python-service-environment`, `python-testing` → `python-service-testing`. Hook tags, tester
  agents' `skills:` lists, and in-plugin references updated.
- **`ceh-python-library`** (v1.2.0) — skills renamed: `python-environment` →
  `python-library-environment`, `python-testing` → `python-library-testing`. Hook tags and
  in-plugin references updated.
- **`ceh-scaffolding`** (v1.0.1) — scaffold skills' references updated to the new skill names.
- **`ceh-web-frontend`** (v3.0.3) — reference-text updates to the new skill names.
- `CROSS_REFERENCES.md` — new "Same Skill, Different Plugins" map tracking the renamed pairs;
  root and plugin READMEs updated.

Old invocations (`/ceh-python-service:python-environment` etc.) must switch to the new names;
auto-load behavior is unaffected (descriptions unchanged).

---

## [3.4.0] — 2026-06-11

New standalone `skills-sync` tool under `tools/` — copies Claude Code skills from this repo's
plugins into a project's `.claude/skills/`. Repo tooling only; no plugin versions change.

### Added

- **`tools/skills-sync`** — skill-sync tool in three equivalent implementations (`skills-sync.ps1`,
  `skills-sync.sh`, `skills-sync.py`) plus a Tidewater-themed `skills-sync.html` picker page
  (CSS/JS extracted into separate files) and a tools README. Syncs selected skills into
  `.claude/skills/`, ignoring individual skill folders rather than the whole `skills/` directory.
  Cross-implementation bugs from a second audit pass fixed.

---

## [3.3.2] — 2026-06-10

`ceh-agent-coding-contract` contract clarified after a cross-model evaluation (Haiku 4.5,
Sonnet 4.6, Opus 4.8, Fable 5): the blanket no-command-execution rule is replaced by a tiered
Validation Policy, and scope, authority, and sub-agent rules are tightened.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.5.1 |

### Changed

- **`ceh-agent-coding-contract`** (v2.5.1) —
  - **Validation Policy** (replaces the "no validation/command execution unless requested" hard
    rule): read-only inspection (`ls`, `grep`, `git status`/`log`/`diff`) and quick correctness
    checks scoped to the edit (syntax, type-check of changed files, import resolution, throwaway
    sanity snippets) are always allowed; writing tests, running test suites, builds, repo-wide
    lint/format, and any state-changing command require an explicit request. Unrequested heavier
    validation is reported in the summary with the exact command instead of run; delegation to a
    tester sub-agent now applies only to *requested* validation (closes a loophole).
  - **Scope** redefined as what is necessary to fulfill the request — not only files the user
    named; beyond that, no drive-by fixes or opportunistic refactors; unsure remains out-of-scope.
  - **Authority hierarchy**: project `CLAUDE.md` (then user-level) now ranks above the contract.
  - **Five-step workflow**: trivial tasks may compress steps 1, 2, and 5 to one sentence each;
    step 5 summaries must state what was *not* validated.
  - **Sub-agents**: on a Stop Condition, report to the calling agent (`AskUserQuestion` is
    unavailable to sub-agents).
  - **Decision Log**: entry IDs are sequential integers; creating/appending the log is
    pre-authorized. Fixed a duplicate "Entry 3" heading in this repo's log (now Entry 13).

---

## [3.3.1] — 2026-06-10

`ceh-blog` rewritten for a personal, non-influencer voice with series continuity; all four
skills compressed for token efficiency.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-blog` | v1.0.5 |

### Changed

- **`ceh-blog`** (v1.0.5) —
  - **Voice**: new Voice section (word-for-word identical in `blog-writer` and `blog-interviewer`)
    — first-person, reflective, the reader overhears the reasoning; banned influencer tells
    (standalone one-liner paragraphs, aphoristic closers, imperative lessons, "If you're building
    X, then Y", bold pseudo-headers, meta-takeaway sign-offs, CTA endings); a never-invent rule
    (every beat from the material or the author's words — flag missing beats, don't fabricate);
    and a `CLAUDE.md` blog-voice override.
  - **Endings**: all six post-type templates end on "The Open Thread" (honest current state —
    what's unresolved, what comes next; a reserved verdict is valid; closure only for a finished
    series' final post) instead of Takeaway/CTA/conviction conclusions. Ending lines are
    byte-identical across writer, interviewer, and editor.
  - **Series continuity**: the blog is treated as serials — each project a series, each post an
    episode. `blog-writer` gains a Series Awareness step (read prior posts, pick up the previous
    episode's thread, cross-link, check continuity facts); `blog-interviewer` reads the blog (not
    just the repo) in Phase 0, asks whether the new post answers the last post's open thread, and
    pins chronology relative to the previous episode.
  - **Interviewing**: four required story beats for story-voice posts (the turn, the moment, the
    verdict, the thread — the thread becomes the ending); hypothesis-option questions permitted;
    answer-drift handling (keep the answer, re-ask once at most); verbatim quote capture (the
    user's phrasing is the voice).
  - **`blog-editor`** aligned so it diagnoses influencer tells and series-continuity slips instead
    of "fixing" open endings into conviction closers. `blog-repurpose` voice rules unchanged —
    its CTA conventions are platform-native to social formats.
  - **Token efficiency**: all four skill bodies compressed (−23% chars, 56.4k → 43.7k) with no
    rule, trigger phrase, or template line dropped; the duplicated Voice and template blocks are
    registered in `CROSS_REFERENCES.md`.

---

## [3.3.0] — 2026-06-09

New `ceh-plan-build-review` plugin: the full plan-driven development loop (plan → implement →
review) in one plugin; the implement/review skills moved out of `ceh-agent-coding-contract`.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-plan-build-review` | v1.0.0 |
| `ceh-agent-coding-contract` | v2.5.0 |

### Added

- **`ceh-plan-build-review`** (v1.0.0) — new use-case plugin bundling four skills:
  - `plan-fullstack-app-iteratively` (new) — plans one release at a time; each session produces a
    single `SKELETON.md` / `ITER_NN.md` artifact scoped to the next build.
  - `plan-fullstack-app-to-mvp` (new) — plans the complete build to a working MVP in one session;
    a complexity gate hands off to the iterative planner when upfront planning is unsafe.
  - `implement-from-plan` (moved from `ceh-agent-coding-contract`) — implements a plan
    document section by section, including the `plan-schema.md` reference.
  - `review-against-plan` (moved from `ceh-agent-coding-contract`) — audits the
    codebase against a plan document and fixes gaps/deviations/errors.
- **`CROSS_REFERENCES.md`** — new "Plan document schema" entry registering the duplication between
  the consumer-side `plan-schema.md` copies and the two planners' `section-specs.md` (producer
  side). The duplication is intentional — the skills are also used standalone outside the plugin —
  and is the repo's only sanctioned exception to the no-duplicated-references rule.

### Changed

- **`ceh-plan-build-review`** — `plan-schema.md` reconciled to the planner skills' schema (the
  golden standard): `mvp: true` and `mvp_target` live on the terminator iteration only, non-terminal
  iterations omit the `mvp` key, and the SKELETON carries no MVP fields; the `## Out of MVP scope`
  block moved from the SKELETON to the terminator. `review-against-plan` now carries its own copy
  of `plan-schema.md` instead of reaching into `implement-from-plan/` by relative path, so every
  skill folder is self-contained for standalone use.

### Removed

- **`ceh-agent-coding-contract`** (v2.5.0, MINOR per the v2.3.0 skill-removal precedent) —
  `implement-from-plan` and `review-against-plan` moved to `ceh-plan-build-review`. The contract
  plugin is now contract-only (skill + SessionStart hook); README updated with a pointer to the
  new plugin.

---

## [3.2.0] — 2026-06-07

New `merge` skill, and the `open-pr` skill triggers more reliably.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.1.0 |

### Added

- **`ceh-git-workflow`** — new `merge` skill owning the merge-and-cleanup moment: pre-merge gate
  (CI green, approvals, rebased, clean history), merge-commit strategy (no squash/rebase-merge),
  and post-merge cleanup (delete remote + local branch, return to `main`, prune). Triggers on
  "merge it", "merge and delete the branch", "clean up the branch", and the merge half of compound
  requests like "create a PR, merge it, delete the branch".

### Changed

- **`ceh-git-workflow`** — the `open-pr` skill under-triggered on compound requests (e.g. "create
  pr, merge and delete branch") because its description named only "opening a pull request".
  Rewrote it to match any phrasing (create/open/raise/make/submit/send a PR, pull request, or merge
  request) and to scope the PR-creation half of compound requests, deferring merge/cleanup to the
  new `merge` skill. Moved the merge-commit policy out of `open-pr` (now a one-line pointer) so the
  `merge` skill owns it with no duplication.

---

## [3.1.4] — 2026-06-06

The `release` skill triggers more reliably and is no longer stack-specific.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.0.1 |

### Changed

- **`ceh-git-workflow`** — the `release` skill under-triggered: its description named only
  `pyproject.toml`/`package.json` for version bumps (missing `plugin.json`/`marketplace.json` and
  other ecosystems), carried no literal user-phrasings, and stopped at the git tag without covering
  GitHub releases. Rewrote the description with quoted trigger phrases ("cut a release", "create a
  release", "bump the version(s)", etc.) and a manifest-agnostic file list (examples, not a closed
  set). Updated the command sequence to use an annotated tag (`git tag -a -m`, avoiding the "no tag
  message" failure on repos that enforce it) and to include the optional `gh release create` step.

---

## [3.1.3] — 2026-06-06

SessionStart hooks now surface a user-visible note when they fire.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.6 |
| `ceh-architecture` | v3.0.2 |
| `ceh-python-service` | v3.0.1 |
| `ceh-python-library` | v1.1.1 |
| `ceh-web-frontend` | v3.0.2 |

### Changed

- **`ceh-agent-coding-contract`, `ceh-architecture`, `ceh-python-service`, `ceh-python-library`,
  `ceh-web-frontend`** — each plugin's SessionStart hook injected its directive/invariants only via
  `additionalContext`, which reaches Claude but is never shown to the user, so there was no signal
  in the conversation UI that the hook had fired. Added a `systemMessage` field to each hook so the
  user sees a short note (e.g. "ceh-python-service: loading Python service invariants for this
  session.") on session start, `/clear`, and compaction. The `additionalContext` payloads are
  unchanged.

---

## [3.1.2] — 2026-06-06

Plan skills now auto-trigger on version-tagged phrasing.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.5 |

### Changed

- **`ceh-agent-coding-contract`** — `implement-from-plan` and `review-against-plan` handled
  version-tagged plans in their bodies (v3.1.1) but their `description` frontmatter carried no
  version phrasing, so prompts like "implement v2 iter plans" never auto-triggered. Added
  version-tagged trigger phrases and noted `SKELETON_v2.md` / `v2_ITER_03.md` variants and
  `depends_on`-chain resolution in both descriptions. No body changes.

---

## [3.1.1] — 2026-06-05

Plan skills support version-tagged plan files and `depends_on`-based resolution.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.4 |

### Changed

- **`ceh-agent-coding-contract`** — `implement-from-plan` and `review-against-plan` were hardcoded
  to `SKELETON.md` / `ITER_NN.md`. Generalized discovery to match optional version tags (prefix or
  suffix, e.g. `SKELETON_v2.md`, `v2_ITER_03.md`) and grouped files into plan families. Resolution
  now follows the `depends_on` chain backward (never forward), crossing into a base version where a
  later version builds on it.
- **`plan-schema.md`** — aligned to the canonical section spec: added `mvp_target` (SKELETON) and
  the `mvp` terminator + `depends_on` (ITER, artifact stems); documented the SKELETON
  `## Out of MVP scope` block. Clarified that `mvp` / `mvp_target` are optional (no terminator
  inferred when absent), that skeletons carry no `depends_on`, and the same-sequence vs
  cross-version `depends_on` chain forms.

---

## [3.1.0] — 2026-06-05

SessionStart hook audit: added one missing invariants hook and fixed two that were silently failing.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-architecture` | v3.0.1 |
| `ceh-python-library` | v1.1.0 |
| `ceh-web-frontend` | v3.0.1 |

### Added

- **`ceh-python-library`** — SessionStart invariants hook (`hooks/hooks.json` → `hooks/load-invariants.js`)
  injecting the passive `python-environment` style/type and minimal-dependency rules, mirroring
  `ceh-python-service`. Closes a shared-standards gap: the library carried the same invariant skill
  but no hook to enforce it. Added a parallel `## Hooks` section to the plugin README.

### Fixed

- **`ceh-architecture`**, **`ceh-web-frontend`** — the SessionStart hook scripts had an escaped
  closing backtick (`\``) that left the template literal unterminated, so `node` threw a
  `SyntaxError` and the hook injected nothing. Both invariants blocks were silently never reaching
  sessions. Both now emit valid JSON.

---

## [3.0.0] — 2026-06-05

Use-case-based plugin reorganization (see `docs/PLUGIN_REORG_PLAN.md`). **Breaking:** four plugins
were renamed; there are no alias shims. Net 11 → 13 plugins.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.3 |
| `ceh-architecture` | v3.0.0 |
| `ceh-blog` | v1.0.4 |
| `ceh-dev-tools` | v1.1.2 |
| `ceh-documentation` | v1.0.1 |
| `ceh-git-workflow` | v3.0.0 |
| `ceh-lessons-learned` | v2.0.3 |
| `ceh-ops` | v3.0.0 |
| `ceh-python-library` | v1.0.0 |
| `ceh-python-service` | v3.0.0 |
| `ceh-scaffolding` | v1.0.0 |
| `ceh-summarize-chat` | v2.0.3 |
| `ceh-web-frontend` | v3.0.0 |

### Renamed (breaking)

- `ceh-release-ops` → **`ceh-ops`**; `ceh-python-backend` → **`ceh-python-service`**;
  `ceh-typescript-frontend` → **`ceh-web-frontend`**; `ceh-architecture-design` → **`ceh-architecture`**.

### Added

- **`ceh-python-library`** (NEW) — packaging/publishing, public-API surface, semver, plus uv environment
  and pytest testing duplicated-and-trimmed from `ceh-python-service` (no web deps).
- **`ceh-scaffolding`** (NEW) — per-project-type setup (service, library, web frontend, fullstack); folds
  in the former `gitignore` skill's entries.
- **`ceh-web-frontend`** — new `react-vite` skill; now covers Svelte and React in one plugin.

### Changed

- **`ceh-ops`** — deduped: security/observability/database-migrations merged into `ceh-python-service`,
  definition-of-done merged into `ceh-git-workflow:open-pr`, versioning split (semver → git-workflow,
  deploy pipeline → new `deploy` skill). Keeps incidents, rollback, deploy + CI agents.
- **`ceh-python-service`** — `fastapi` absorbs rest-api design; `asyncpg` absorbs postgresql driver rules;
  `postgresql` moved in (schema design); observability/security adopt the richer ops content.
- **`ceh-web-frontend`** — consolidated `coding-style` + `linting` into `environment`; generalized
  `accessibility`/`frontend-testing` to `.svelte` and `.tsx`.
- **`ceh-architecture`** — trimmed to `adr` + `domain-modeling`; hook invariants trimmed accordingly.
- **`ceh-git-workflow`** — `open-pr` absorbed the definition-of-done quality gate.
- **`ceh-agent-coding-contract`** (PATCH) — Decision Log section now states the log is the required
  channel and is not satisfied by a commit message/PR/summary; log at the moment of the decision.

### Removed

- `event-sourcing` and `llm-integration` skills (app-specific, not reusable standards).
- standalone `rest-api`, `postgresql` (moved), `repository-structure` (folded into scaffolding),
  and `gitignore` (folded into scaffolding) skills.
- dead `scripts/sync-stubs.ps1`.

---

## [2.8.0] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.2 |
| `ceh-architecture-design` | v2.2.2 |
| `ceh-blog` | v1.0.4 |
| `ceh-dev-tools` | v1.1.2 |
| `ceh-documentation` | v1.0.1 |
| `ceh-git-workflow` | v2.5.3 |
| `ceh-lessons-learned` | v2.0.3 |
| `ceh-python-backend` | v2.3.1 |
| `ceh-release-ops` | v2.2.5 |
| `ceh-summarize-chat` | v2.0.3 |
| `ceh-typescript-frontend` | v2.3.0 |

### Added

- **`ceh-architecture-design`**, **`ceh-python-backend`**, **`ceh-typescript-frontend`** (MINOR) — each ships a `SessionStart` invariants hook that injects always-on domain invariants (the rules that under-trigger as auto-load skills because they fire on implicit mid-turn decisions). Skills remain the on-demand depth reference, routed via `<plugin>:<skill>` tags. Process plugins (release-ops, git-workflow) intentionally keep discrete-event skills with no hook.

### Changed

- **`ceh-architecture-design`** (MINOR) — scoped to backend: removed the asyncpg transaction/pool code (now sole-owned by `ceh-python-backend:asyncpg`) and the frontend structure (now in `ceh-typescript-frontend:sveltekit`); added an `adr` storage convention; standardized PostgreSQL on `entity_*` vocabulary.
- **`ceh-typescript-frontend`** (MINOR) — modernized all skill examples to Svelte 5 runes (`$props`, `$state`, `$derived`, `onclick`); `bun.lockb` → `bun.lock`.
- **`ceh-agent-coding-contract`** (PATCH) — clarified the authority hierarchy (an in-session user instruction overrides the contract) and the authorization rule; made the Decision Log path overridable; added the `compact` hook event.
- **`ceh-python-backend`** (PATCH) — fastapi error handler now includes `correlation_id`; lifespan pool uses the standard sizing; synced the pip-audit command and coverage labels to the release-ops canonical.
- **`ceh-release-ops`** (PATCH) — rollback Decision Log path made overridable.
- **`ceh-git-workflow`** (PATCH) — synced open-pr's two checklist blocks and standardized the `docs/adr/DECISIONS.md` path.

---

## [2.7.2] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.1 |
| `ceh-architecture-design` | v2.1.2 |
| `ceh-blog` | v1.0.4 |
| `ceh-dev-tools` | v1.1.2 |
| `ceh-documentation` | v1.0.1 |
| `ceh-git-workflow` | v2.5.2 |
| `ceh-lessons-learned` | v2.0.3 |
| `ceh-python-backend` | v2.2.3 |
| `ceh-release-ops` | v2.2.4 |
| `ceh-summarize-chat` | v2.0.3 |
| `ceh-typescript-frontend` | v2.2.3 |

### Changed

- **All plugins** (PATCH) — standardized author metadata across every `plugin.json` and the marketplace manifest. Author is now `{ "name": "cheneeheng", "email": "eeheng.chen@gmail.com" }` (six manifests previously read `"Chen"` with no email); the marketplace `owner` gained the same email.

---

## [2.7.1] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-documentation` | v1.0.0 |
| `ceh-git-workflow` | v2.5.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.3 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Changed

- **`ceh-git-workflow`** (v2.5.1) — switched the PR merge policy from squash-merge to merge-commit. `main` now preserves every commit per PR (intentionally, as source material for write-ups/blog posts) via `gh pr merge --merge`; squash and rebase-merge are prohibited. Updated `open-pr` (Merge Strategy + PR-title note), `hotfix`, and the plugin README accordingly. Conventional Commits now applies per-commit, with a pre-merge branch-cleanup note.
- **`ceh-release-ops`** (v2.2.3) — mirrored the hotfix merge step in `incidents` (squash → merge commit) to stay consistent with the cross-referenced `ceh-git-workflow/hotfix` skill.

---

## [2.7.0] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-documentation` | v1.0.0 |
| `ceh-git-workflow` | v2.5.0 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Added

- **`ceh-agent-coding-contract`** (v2.4.0) — the plugin now ships its own `SessionStart` hook (`hooks/hooks.json` → `hooks/load-contract.js`) that injects the mandatory directive to load the `agent-coding-contract` skill on the `startup` and `clear` events. Previously this lived in the user's global `~/.claude/settings.json`; bundling it makes contract auto-loading opt-in per project by simply enabling the plugin — no global hook configuration required.

---

## [2.6.0] — 2026-06-01

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.3.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-documentation` | v1.0.0 |
| `ceh-git-workflow` | v2.5.0 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Added

- **`ceh-documentation`** (v1.0.0) — new plugin for end-user and operator-facing documentation. Ships the `user-operator-guide` skill: task-oriented user guides and operator runbooks with strict audience separation, a no-invention/`[VERIFY]` rule, document-type selection, and single- or multi-file output rooted at `docs/guide/` with `index.md` as the entry point.

### Changed

- **`ceh-git-workflow`** (v2.5.0) — moved the `changelog-agent` and `readme-updater` agents (and the `check-semver.py` helper) into the new `ceh-documentation` plugin. Their invoke paths change from `/ceh-git-workflow:*` to `/ceh-documentation:*`.

---

## [2.5.1] — 2026-05-30

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.3.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Changed

- **`ceh-python-backend`** (v2.2.2) — wired the `python-testing` skill into all three tester agents via `skills:` frontmatter, and sharpened their descriptions to clarify when to delegate to an agent (many tests / broad coverage / isolated run) versus handle one or two tests inline. Dropped the duplicated Test Structure block from `python-unit-tester` now that the skill carries it.
- **`ceh-typescript-frontend`** (v2.2.2) — wired the `frontend-testing` skill into all three tester agents via `skills:` frontmatter and sharpened their delegation descriptions to match. Added a Vitest/Jest/Mocha runner-detection note to the `frontend-testing` skill.
- **Repo docs** — documented the plugin-agent frontmatter limitation (`permissionMode`, `hooks`, `mcpServers` ignored on plugin subagents) in `CLAUDE.md` and `README.md`, and re-synced `CROSS_REFERENCES.md` for definition-of-done checklist and coverage-target label drift.

---

## [2.5.0] — 2026-05-29

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.3.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Removed

- **`ceh-agent-coding-contract`** (v2.3.0) — deleted the `execution-modes` skill. Sessions are always autonomous in practice, making the separate interactive/autonomous mode switch redundant.

### Changed

- **`ceh-agent-coding-contract`** (v2.3.0) — folded autonomous-by-default behavior and the authority hierarchy into the `agent-coding-contract` skill: new Execution Mode section, "Ask, don't guess" reframed as "Decide, don't guess silently", and the Interactive/Autonomous parentheticals removed from the task workflow and decomposition rules. READMEs and plugin description updated accordingly.

---

## [2.4.3] — 2026-05-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.3 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Changed

- **`ceh-blog`** (v1.0.3) — sharpened all four skill `description` fields for reliable, disambiguated triggering: each now leads with what the skill does, states the discriminating input state (topic/repo → interviewer, raw notes → writer, written prose → editor, finished post → repurpose), keeps high-signal trigger phrases, and preserves inter-skill routing — while trimming redundant framing (~95 → ~75 words each) for tighter always-loaded token use.

---

## [2.4.2] — 2026-05-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.3 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.2 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Changed

- **`ceh-blog`** (v1.0.2) — rewrote all four skill `description` fields to use the directive "Trigger when…" pattern with explicit trigger phrases and "Do NOT trigger" exclusions; matches the `ceh-agent-coding-contract` style for unambiguous skill dispatch.

---

## [2.4.1] — 2026-05-25

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.3 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.1 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Fixed

- **All plugins** — collapsed multiline `description` block scalars (`>`, `|`) to single-line inline strings in skill and agent frontmatter (56 files across all 10 plugins).
- **`ceh-blog`** — removed redundant `ceh-` prefix from skill `name` fields (`ceh-blog-editor` → `blog-editor`, etc.); the prefix is already carried by the plugin namespace.

---

## [2.4.0] — 2026-05-25

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.2 |
| `ceh-architecture-design` | v2.1.0 |
| `ceh-blog` | v1.0.0 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.4.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.2.0 |
| `ceh-release-ops` | v2.2.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.2.0 |

### Added

- **`ceh-blog` plugin (new, v1.0.0)** — interview-driven blog writing end-to-end:
  - `blog-interviewer`: structured interview skill to extract ideas, audience, and key points from the user.
  - `blog-writer`: drafts a full publication-ready blog post from interview output.
  - `blog-editor`: iterative editing pass — tone, clarity, and structure review.
  - `blog-repurpose`: repurposes a finished post for Twitter/X, LinkedIn, TL;DR, and newsletter formats.

### Changed

- **`ceh-agent-coding-contract`** (v2.2.2): Karpathy-derived rules added to the coding contract — opinionated heuristics on scope discipline, implementation order, and change minimalism.

---

## [2.3.0] — 2026-05-16

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.1 |
| `ceh-architecture-design` | v2.1.0 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.4.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.2.0 |
| `ceh-release-ops` | v2.2.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.2.0 |

### Added

- **`ceh-agent-coding-contract`** (v2.2.1): New `execution-modes` micro-skill extracted from references — covers interactive vs. autonomous mode rules and stop conditions.
- **`ceh-python-backend`** (v2.2.0): Four new micro-skills promoted from the former `python-backend` bundle:
  - `alembic`: Alembic migration setup, autogenerate, upgrade/downgrade workflow.
  - `asyncpg`: asyncpg query patterns, connection pool, and database reference (replaces `references/database.md`).
  - `python-environment`: uv environment setup, dependency management, and linting (ruff, mypy).
  - `python-observability`: structured logging, metrics, and health-check patterns.
  - `python-security`: secrets handling, CORS, rate limiting, and input validation.
- **`ceh-typescript-frontend`** (v2.2.0): New `environment` micro-skill covering Bun/Node setup, Vite config, and toolchain commands — extracted from the former `typescript-frontend` bundle.
- **Repo**: `scripts/sync-stubs.ps1` added — synchronises cross-plugin stub reference files in one pass.
- **Repo**: `CROSS_REFERENCES.md` added — tracks content duplicated across skills with canonical source and all copy locations.

### Changed

- **`ceh-agent-coding-contract`** (v2.2.1): All reference files (`core-rules.md`, `decision-log.md`, `execution-modes.md`, `non-goals.md`, `stop-conditions.md`, `task-workflow.md`) inlined into `agent-coding-contract/SKILL.md`; reference files removed. `implement-from-plan` and `review-against-plan` skills updated to inline their reference content.
- **`ceh-architecture-design`** (v2.1.0): Former `architecture-design` bundle skill and all its `references/` files removed. Content inlined into the existing micro-skills: `adr`, `domain-modeling`, `event-sourcing`, `llm-integration`, `postgresql`, `repository-structure`, `rest-api`.
- **`ceh-git-workflow`** (v2.4.0): Former `git-workflow` bundle skill and all its `references/` files removed. Content inlined into the existing micro-skills: `branch`, `code-review`, `commit`, `dependency-management`, `gitignore`, `hotfix`, `open-pr`, `release`. `merge` skill removed; merge strategy content consolidated into `open-pr`.
- **`ceh-python-backend`** (v2.2.0): Former `python-backend` bundle skill and all its `references/` files removed. Content distributed into `fastapi`, `python-testing`, and the four new micro-skills above. Agent descriptions trimmed (`python-integration-tester`, `python-system-tester`).
- **`ceh-release-ops`** (v2.2.1): Former `release-ops` bundle skill and all its `references/` files removed. Content inlined into existing micro-skills: `database-migrations`, `definition-of-done`, `incidents`, `observability`, `rollback`, `security`, `versioning`. Lifecycle phase labels added to micro-skill descriptions.
- **`ceh-typescript-frontend`** (v2.2.0): Former `typescript-frontend` bundle skill and all its `references/` files removed. Content inlined into existing micro-skills: `accessibility`, `coding-style`, `frontend-testing`, `linting`, `sveltekit`, plus new `environment`.
- **`ceh-git-workflow`** (v2.4.0): `readme-updater` agent — `maxTurns` tuned; `effort` field removed.
- **Repo**: `CLAUDE.md` updated — bundle/micro-skill distinction removed; versioning and plugin table updated to reflect new structure.
- **Repo**: All plugin `README.md` files updated to reflect bundle removal and current skill lists.
- **Repo**: `ceh-dev-tools/CHANGELOG.md` removed (stale, not maintained).

---

## [2.2.3] — 2026-05-14

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.1.2 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.3 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Added

- **`ceh-git-workflow`** (v2.2.3): Attribution footer guidance added to commit (`commits.md`) and PR (`pull-requests.md`) standards. Test-run delegation rule added to `task-workflow.md` — test execution should be handed off to background subagents (auto-triggered tester agents take precedence; `Agent(run_in_background=True)` as fallback).
- **Repo**: `LICENSE.md` added.

### Changed

- **`ceh-git-workflow`** (v2.2.3): `branch` skill inlines start-new-work commands, dropping the `workflows.md` pointer (~135 lines/invocation saved).
- **`ceh-agent-coding-contract`** (v2.1.2): `agent-coding-contract` skill trigger narrowed to explicit phrases only, removing broad auto-load on refactors and multi-file changes. `review-against-plan` skill drops §01/§03 audit rows and tightens wording (~10 lines/run saved).
- **Repo**: `CLAUDE.md` updated — "Adding an Agent" section added parallel to "Adding a Skill"; `ceh-dev-tools` flagged as agents-only in the Plugins table; cross-bundle stub check command narrowed to `skills/python-backend` path; versioning rules clarified (PATCH for updates, MINOR for new skills/agents).

---

## [2.2.2] — 2026-05-02

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.1.0 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.1 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Added

- **`ceh-agent-coding-contract`** (v2.1.0): Two new bundle skills for plan-driven development:
  - `implement-from-plan`: implements a SKELETON.md or ITER_NN.md planning document section by section, resolving iteration pointers and respecting scope boundaries.
  - `review-against-plan`: audits the codebase against a planning document, categorizes findings as Gap / Deviation / Error, fixes them in-line, and produces a Plan Compliance Report.
  - `plan-schema.md` reference: defines SKELETON and ITER frontmatter, section table (§01–§06), pointer rules, and resolution order.

---

## [2.2.1] — 2026-04-29

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.2 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.1 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Changed

- **`ceh-agent-coding-contract`** (v2.0.2): Added built-in tool guidance across reference files — `AskUserQuestion` in `core-rules.md` (ask-don't-guess rule), `execution-modes.md` (Interactive Mode stop), and `stop-conditions.md`; `TaskCreate`/`TaskUpdate` and `Agent` tool in `task-workflow.md` for subtask tracking and parallel execution.

- **`ceh-git-workflow`** (v2.2.1): Added tool guidance — `Read`/`Grep`/`Bash` for code inspection in `code-review.md`; `Bash` with `git diff main...HEAD` in `pull-requests.md` author self-review checklist; `Bash` for audit commands in `dependencies.md`.

- **`ceh-python-backend`** (v2.1.2): Added `Bash` tool notes to `environment.md` (command table), `linting.md` (pre-PR checks), `migrations.md` (alembic workflow), `testing.md` (coverage run), and `security.md` (`pip-audit`).

- **`ceh-typescript-frontend`** (v2.1.2): Added `Bash` tool notes to `environment.md` (command table) and `linting.md` (pre-PR checks).

- **`ceh-release-ops`** (v2.1.2): Added `Bash` tool notes to `migrations.md` (alembic commands), `versioning.md` (release checklist), `security.md` (audit commands), and `rollback.md` (rollback procedure).

### Fixed

- Removed stale `docs/claude_logs/LESSONS_LEARNED.md` session log.

---

## [2.2.0] — 2026-04-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.1 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.1 |
| `ceh-release-ops` | v2.1.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.1 |

### Changed

- **`ceh-dev-tools`** (v1.1.0):
  - `repo-tree-mapper` agent: defaults to running in background.

- **`ceh-git-workflow`** (v2.2.0):
  - `changelog-agent` agent: defaults to running in background.
  - `readme-updater` agent: defaults to running in background.

---

## [2.1.1] — 2026-04-26

### Fixed

- Added full list of agents to the readme.

---

## [2.1.0] — 2026-04-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.1 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.0.1 |
| `ceh-git-workflow` | v2.1.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.1 |
| `ceh-release-ops` | v2.1.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.1 |

### Added

- **`ceh-dev-tools` plugin (new, v1.0.1)** — developer productivity agents:
  - `repo-tree-mapper` agent: walks a repo and produces an annotated `REPO_MAP.md`; trimmed description ~50%, `maxTurns` 25 → 8.
  - `walk-repo.sh` script: git-aware directory walker (fixed non-portable `$skip && continue` → `[[ $skip == true ]] && continue`).
  - Registered in top-level `README.md`, `CLAUDE.md`, and `marketplace.json`.

- **`ceh-git-workflow`** (v2.1.0) — new agents and scripts:
  - `changelog-agent`: generates or updates `CHANGELOG.md` (Keep a Changelog + semver).
  - `readme-updater`: applies surgical README edits after feature changes.
  - `check-semver.py` script: validates all version headers in a changelog file.

- **`ceh-python-backend`** (v2.1.1) — new agents, scripts, and references:
  - `python-unit-tester`, `python-integration-tester`, `python-system-tester` agents.
  - `run-unit-tests.sh`, `run-integration-tests.sh`, `run-system-tests.sh` scripts (use `uv run pytest`).
  - `references/migrations.md`: Alembic setup, autogenerate, upgrade/downgrade, test DB management.

- **`ceh-typescript-frontend`** (v2.1.1) — new agents, scripts, and micro-skills:
  - `ts-unit-tester`, `ts-integration-tester`, `ts-system-tester` agents.
  - `detect-test-framework.sh`, `run-unit-tests.sh`, `run-integration-tests.sh`, `check-coverage.sh`, `run-e2e.sh` scripts.
  - `skills/linting/SKILL.md`: new micro-skill for ESLint/Prettier/svelte-check/tsc.
  - `skills/coding-style/SKILL.md`: new micro-skill for TypeScript type conventions and naming.
  - `references/accessibility.md`: expanded with ARIA patterns, focus management, keyboard nav, form labelling, and color contrast rules.

- **`ceh-release-ops`** (v2.1.1) — new agents, scripts, and micro-skills:
  - `github-actions`, `gitlab-ci` agents for creating, reviewing, and debugging CI pipelines.
  - `gh-detect-stack.sh`, `gh-scaffold.sh`, `gh-validate.sh`, `gh-analyze-failure.sh` scripts.
  - `gl-detect-stack.sh`, `gl-scaffold.sh`, `gl-validate.sh`, `gl-analyze-failure.sh` scripts.
  - `skills/versioning/SKILL.md`: micro-skill for version bumps and release tagging.
  - `skills/rollback/SKILL.md`: micro-skill for deployment health-check failures.

- **READMEs and CHANGELOGs** added to all plugins that were missing them (`ceh-agent-coding-contract`, `ceh-architecture-design`, `ceh-git-workflow`, `ceh-python-backend`, `ceh-release-ops`, `ceh-lessons-learned`, `ceh-summarize-chat`, `ceh-typescript-frontend`, `ceh-dev-tools`).

### Fixed

- **`ceh-agent-coding-contract`** (v2.0.1): merged `agent-role.md` into `core-rules.md`; updated `SKILL.md` to load all references (full contract, not selective).
- **`ceh-python-backend`**: `references/exceptions.md` — removed contradictory rule about route handlers converting domain exceptions; `references/coding-style.md` — replaced deprecated `asyncio.get_event_loop()` with `asyncio.get_running_loop()`; `references/security.md` — `uv run pip-audit` → `uvx pip-audit`; `references/testing.md` — added `system/` to test structure tree.
- **`ceh-typescript-frontend`**: `references/error-handling.md` — component example now uses `onSuccess` callback instead of writing `sessionStore` directly; removed `scripts/setup-test-db.sh` (Postgres setup does not belong in a frontend plugin).
- **`ceh-release-ops`**: `references/definition-of-done.md` — corrected core domain services coverage target from 90% → 95%, matching `ceh-python-backend/references/testing.md` and `ceh-git-workflow/references/ci.md`; trimmed `references/observability.md` (removed redundant bad-example block); synced `skills/python-backend/references/observability.md` stub.
- **`ceh-git-workflow`**: `references/workflows.md` — added `git push origin --delete <branch-name>` to the "After PR is merged" sequence.

### Changed

- Token optimizations across reference files (no content removed): `ceh-summarize-chat/SKILL.md`, `ceh-lessons-learned/SKILL.md`, `ceh-architecture-design/references/domain-modeling.md`, `ceh-architecture-design/references/postgresql.md`, `ceh-python-backend/references/database.md`, `ceh-release-ops/references/observability.md`, `ceh-python-backend/references/coding-style.md`, `ceh-python-backend/references/testing.md`; both database stubs kept in sync.

---

## [2.0.0] — 2026-04-08 (all plugins)

### Changed

- **Breaking**: split the monolithic `ceh` plugin into 8 standalone plugins, one per domain:
  `ceh-agent-coding-contract`, `ceh-architecture-design`, `ceh-python-backend`,
  `ceh-typescript-frontend`, `ceh-git-workflow`, `ceh-release-ops`,
  `ceh-summarize-chat`, `ceh-lessons-learned`.
- Each bundle skill and its associated micro-skills now live in the same plugin. Skill invoke
  prefixes changed from `ceh:*` to `ceh-<plugin>:*` (e.g. `ceh:commit` → `ceh-git-workflow:commit`).
- Cross-bundle micro-skills (`postgresql`, `observability`, `security`) retain identical relative
  reference paths; foreign reference files are duplicated into the host plugin where needed.
- `marketplace.json` updated to list all 8 plugins; old `ceh` entry removed.

---

## [1.0.5] — 2026-04-06

### Fixed

- `lessons-learned` skill: clarified append instruction to always add new entries at the very end of `LESSONS_LEARNED.md`, never before the last existing entry.

---

## [1.0.4] — 2026-04-05

### Changed

- Standardised all Claude-generated log file paths to `docs/claude_logs/`: `LESSONS_LEARNED.md`, `DECISION_LOG.md` (referenced across `lessons-learned`, `agent-coding-contract`, `git-workflow`, and `release-ops` skills).
- Moved `ARCHITECTURE_DECISIONS.md` references out of `docs/claude_logs/` to `docs/adr/DECISIONS.md` — this file is shared developer documentation, not a Claude session artifact (`git-workflow/references/code-review.md`, `architecture-design/references/rest-api.md`).

---

## [1.0.3] — 2026-04-03

### Added

7 micro-skills extracted from `git-workflow` for fine-grained auto-triggering on individual
git operations.

| Micro-skill | Sources | Auto-triggers when |
|---|---|---|
| `branch` | git-workflow/branching + workflows | Creating or naming a branch |
| `commit` | git-workflow/commits + workflows | Writing a commit message or staging changes |
| `open-pr` | git-workflow/pull-requests + workflows | Opening a pull request or writing a PR description |
| `merge` | git-workflow/merging | Merging a branch or choosing a merge strategy |
| `hotfix` | git-workflow/workflows + releases | Executing a critical production fix |
| `release` | git-workflow/releases + workflows | Tagging a release or bumping a version |
| `gitignore` | git-workflow/gitignore | Creating or editing a `.gitignore` file |

---

## [1.0.2] — 2026-04-01

### Added

18 micro-skills for precise auto-triggering. Each is a thin skill that points to the relevant
reference file(s) already defined in the bundle skills — no content duplication.

| Micro-skill | Sources | Auto-triggers when |
|---|---|---|
| `adr` | architecture-design/adrs | Making significant design decisions |
| `domain-modeling` | architecture-design/domain-modeling | Designing entities, IDs, status fields |
| `event-sourcing` | architecture-design/event-sourcing | Working with event log or state snapshots |
| `rest-api` | architecture-design/rest-api | Building endpoints, choosing HTTP codes |
| `postgresql` | architecture-design/postgresql + python-backend/database | Writing SQL, asyncpg queries, schema changes |
| `llm-integration` | architecture-design/llm-integration | Integrating LLM calls or handling output |
| `fastapi` | python-backend/fastapi + python-backend/exceptions | Writing route handlers, DI, exception hierarchy |
| `python-testing` | python-backend/testing | Writing Python tests |
| `sveltekit` | typescript-frontend/sveltekit + typescript-frontend/error-handling | Routes, stores, components, API client |
| `frontend-testing` | typescript-frontend/testing | Writing frontend tests |
| `accessibility` | typescript-frontend/accessibility | Writing Svelte component markup |
| `observability` | python-backend/observability + release-ops/observability | Logging, metrics, health checks |
| `database-migrations` | release-ops/migrations | Writing or running Alembic migrations |
| `incidents` | release-ops/incidents + release-ops/hotfix | Production incidents, post-mortems |
| `definition-of-done` | release-ops/definition-of-done | Preparing to open a PR |
| `security` | python-backend/security + release-ops/security | Secrets, CORS, rate limiting, input validation |
| `code-review` | git-workflow/code-review | Reviewing PRs, leaving review comments |
| `dependency-management` | git-workflow/dependencies | Adding or upgrading packages |

---

## [1.0.1] — 2026-04-01

### Changed

- Refactored `agent-coding-contract`, `architecture-design`, `python-backend`, `typescript-frontend`, and `release-ops` skills: replaced long, keyword-stuffed `SKILL.md` titles with a short title and a summary paragraph, and moved all detailed content into topic-specific files under a `references/` folder — matching the pattern established by `git-workflow`.
- Updated `summarize-chat` skill: replaced the verbose title with a short title and summary paragraph (no reference files needed).

### Reference files added

| Skill | New reference files |
|-------|-------------------|
| `agent-coding-contract` | agent-role, core-rules, decision-log, execution-modes, non-goals, stop-conditions, task-workflow |
| `architecture-design` | adrs, domain-modeling, event-sourcing, llm-integration, postgresql, repository-structure, rest-api |
| `python-backend` | coding-style, database, environment, exceptions, fastapi, linting, observability, security, testing |
| `release-ops` | definition-of-done, hotfix, incidents, migrations, observability, rollback, security, versioning |
| `typescript-frontend` | accessibility, coding-style, environment, error-handling, linting, sveltekit, testing |

---

## [1.0.0] — 2026-03-31

### Added

- Initial release of the `ceh` plugin.
- Skills: `agent-coding-contract`, `architecture-design`, `git-workflow`, `lessons-learned`, `python-backend`, `release-ops`, `summarize-chat`, `typescript-frontend`.
- `git-workflow` ships with reference files: branching, ci, code-review, commits, dependencies, gitignore, merging, pull-requests, releases, workflows.
- `LESSONS_LEARNED.md` for capturing session retrospectives.
- `marketplace.json` for plugin discovery.
