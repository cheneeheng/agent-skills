# Merging Strategy

**Squash merge only** — `main` history is one commit per PR.

- The squash commit message = the PR title (Conventional Commits format)
- Squash makes `git log` readable and `git bisect` effective
- Never use merge commits on `main`
- Rebase is fine locally during development
- Force-push is allowed only on personal feature branches (never on `main`)
