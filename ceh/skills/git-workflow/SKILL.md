---
name: "git-workflow"
description: >
  Load this skill when writing commit messages, naming branches, opening pull requests, reviewing
  code, configuring CI checks, or evaluating new dependencies. Covers the full team collaboration
  loop: trunk-based branching strategy and branch naming, Conventional Commits message format,
  squash merge strategy, pull request size guidelines and description template, author self-review
  checklist, code review comment conventions (blocking vs advisory), branch protection and required
  CI gates before merge, and dependency evaluation and security audit process. Use this skill any
  time you touch git operations, PR workflows, CI configuration, or package management decisions —
  regardless of language or framework.
---

# Git Version Control and Team Collaboration Standards: Trunk-Based Branching Strategy, Conventional Commits Message Format, Squash Merge Policy, Pull Request Size Guidelines and Description Template, Author Self-Review Checklist, Code Review Comment Conventions Blocking vs Advisory, Branch Protection Rules, Required CI Checks Before Merge, Dependency Evaluation Criteria and Security Audit

---

## Branching Strategy

Trunk-based development. `main` is always deployable.

- Feature branches are short-lived and scoped to a single task or change
- Direct commits to `main` are blocked — all changes go through a PR
- Branch from `main`. Never branch from another feature branch
- Delete branches after merge

### Branch Naming

```
<type>/<short-description>
```

| Prefix | When to use | Example |
|--------|------------|---------|
| `feat/` | New feature | `feat/session-replay` |
| `fix/` | Bug fix | `fix/token-expiry-edge-case` |
| `chore/` | Maintenance, tooling, dependency updates | `chore/update-dependencies` |
| `docs/` | Documentation only | `docs/add-onboarding-guide` |
| `test/` | Test additions or fixes with no source changes | `test/reasoning-engine-invariants` |
| `refactor/` | Code changes without feature or bug changes | `refactor/extract-auth-middleware` |

Short description: lowercase, hyphen-separated, 3–5 words.

---

## Commit Messages — Conventional Commits

```
<type>(<scope>): <short summary>

[optional body — explain why, not what]

[optional footer — breaking changes, issue refs]
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New feature or behavior |
| `fix` | Bug fix |
| `refactor` | Code change with no behavior change |
| `test` | Adding or changing tests |
| `docs` | Documentation only |
| `chore` | Build, tooling, dependency updates |
| `perf` | Performance improvement |

### Scope

Optional but recommended. Use the module, component, or layer changed:

```
feat(auth): add JWT refresh token rotation
fix(api): handle 429 response from upstream correctly
chore(deps): upgrade fastapi to 0.115.0
```

### Rules

- Subject line: imperative mood, lowercase, no period, ≤ 72 characters
- Body: explain *why*, not *what* — the diff already shows what changed
- Breaking changes: add `BREAKING CHANGE:` footer with migration notes
- Reference issues: `Closes #123` or `Refs #456` in footer

**Good:**
```
feat(orders): add bulk cancel endpoint

Supports cancelling up to 100 orders per request. Single-cancel
endpoint remains unchanged; no migration needed.

Closes #342
```

**Bad:**
```
WIP changes
fixed stuff
update auth
```

---

## Merging Strategy

**Squash merge only** — `main` history is one commit per PR.

- The squash commit message = the PR title (Conventional Commits format)
- Squash makes `git log` readable and `git bisect` effective
- Never use merge commits on `main`
- Rebase is fine locally during development
- Force-push is allowed only on personal feature branches (never on `main`)

---

## Pull Request Standards

### Size Guidelines

| PR type | Recommended | Max |
|---------|-------------|-----|
| Bug fix | ≤ 200 LOC | 300 LOC |
| New feature | ≤ 400 LOC | 600 LOC |
| Refactor | ≤ 500 LOC | 800 LOC |
| DB migration | Migration file only; split app changes into a separate PR |

If a PR exceeds the guideline, split it by layer (schema change PR → service layer PR → API layer PR). Large PRs without justification will be returned for splitting.

### PR Title

Must follow Conventional Commits format. This becomes the squash commit message.

### PR Description Template

```markdown
## What
<!-- One sentence: what does this change do? -->

## Why
<!-- Why is this change needed? Link to ticket/issue. -->

## How
<!-- Brief explanation of approach if non-obvious. -->

## Testing
<!-- What was tested? What test cases were added? -->

## Checklist
- [ ] All CI checks pass
- [ ] Tests added or updated for new behavior
- [ ] No `any` / `@ts-ignore` / `# type: ignore` introduced
- [ ] No secrets or credentials in code
- [ ] Migrations (if any) are backward-compatible
- [ ] ARCHITECTURE_DECISIONS.md updated (if a durable decision was made)
```

### Author Self-Review Checklist

Before requesting review, the author must:

- [ ] Read the diff top-to-bottom as if seeing it for the first time
- [ ] No commented-out code
- [ ] No debug logs or `console.log` / `print()` left in
- [ ] No `TODO` without a linked ticket
- [ ] Branch is rebased on latest `main`
- [ ] PR description is complete
- [ ] PR is scoped to one concern (if not, split it)

### Required Approvals

- Bug fixes and small features: 1 approval
- New API surfaces, schema changes, security changes: 2 approvals
- Hotfixes: 1 approval minimum (do not bypass CI)
- The author may not approve their own PR

---

## Code Review Comment Conventions

Every comment must be clearly marked as **blocking** or **advisory**. Ambiguous comments slow merges and create guesswork.

| Prefix | Meaning | Author must |
|--------|---------|-------------|
| `[blocking]` | Must be resolved before merge | Fix or discuss with reviewer |
| `[advisory]` | Suggestion, nit, optional improvement | Address or explicitly acknowledge |
| `[question]` | Seeking understanding, not a change request | Answer the question |

**Examples:**
```
[blocking] This query is not parameterized — SQL injection risk on line 47.

[advisory] This helper could be extracted to a utility function for reuse.
           Not required for this PR but worth considering.

[question] Why is this retry limit set to 3? Is there a reason not to use
           the global default?
```

### Review Focus (Priority Order)

1. **Correctness** — does it do what it claims? Are edge cases handled?
2. **Security** — injection risks, secrets exposure, input validation gaps
3. **Test coverage** — is new behavior tested? Are tests testing behavior?
4. **Design** — is this the right abstraction? Does it fit existing patterns?
5. **Style** — only flag if linting tools don't catch it

Do not leave style comments that a linter would catch. Configure the linter instead.

Review does not re-litigate resolved decisions in `ARCHITECTURE_DECISIONS.md` unless new risk is identified.

---

## CI Requirements

All checks must pass before merge. No exceptions.

### Python Backend

```bash
uv run ruff check .           # Lint
uv run ruff format --check .  # Format check
uv run mypy .                 # Type check (strict)
uv run pytest --cov=app       # Tests + coverage gate
```

Coverage gates: 80% for `app/`, 95% for core business logic.

### TypeScript Frontend

```bash
bun run lint          # ESLint
bun run format:check  # Prettier
bun run check         # svelte-check (template + a11y)
bun run typecheck     # tsc --noEmit
bun run test          # Vitest
```

Coverage gate: 70% for `src/lib/`.

### Both

- Docker images (`backend/Dockerfile`, `frontend/Dockerfile`) must build successfully
- No committed secrets (Gitleaks or equivalent)

### Branch Protection Rules

- Direct pushes to `main` are blocked
- All required CI checks must pass before merge is allowed
- At least 1 approved review required
- Branch must be up-to-date with `main` before merge
- No force-push to `main`

---

## Tagging and Releases

- Tags follow semantic versioning: `v<major>.<minor>.<patch>`
- Tags are applied to `main` after a release
- Never tag a commit that hasn't passed all CI checks

---

## Dependency Management

### Evaluation Criteria — Before Adding Any Package

Ask all five questions:

1. **Necessity** — can this be done with < 20 lines of code in-house?
2. **Maintenance** — actively maintained? Last commit < 6 months?
3. **Popularity and trust** — download volume, stars, known maintainers?
4. **License** — compatible with the project? Avoid GPL for proprietary code.
5. **Size** — what is the bundle/install size impact?

If a dependency fails any of these, document why you're adding it anyway.

### Pinning Policy

| Environment | Pin level |
|-------------|-----------|
| Production dependencies | Exact version |
| Dev/test dependencies | Minor version (e.g. `^1.2.0`) |
| CI tool versions | Exact version |

Never use `*` or `latest` as a version specifier in any environment.

### Security Audits

Run before every release and as part of CI:

```bash
uv run pip-audit          # Python
bun audit                 # TypeScript/JavaScript
```

Address all high-severity findings before release. Document any accepted medium-severity exceptions in `DECISION_LOG.md`.

### Major Version Upgrades

Any dependency major version bump requires:
1. A dedicated PR (not bundled with feature work)
2. A brief ADR entry explaining the upgrade and breaking changes handled
3. Full test suite pass after upgrade

---

## .gitignore Expectations

Must include:
```
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
.mypy_cache/
.ruff_cache/
node_modules/
.svelte-kit/
dist/
build/
*.db
```
