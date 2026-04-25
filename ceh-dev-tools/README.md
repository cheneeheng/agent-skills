# ceh-dev-tools

Developer productivity agents for repository exploration and codebase orientation.

## Agents

### `repo-tree-mapper`

Generates an annotated, clickable `REPO_MAP.md` from any repository. Every file and folder is linked and labeled with its purpose.

**Triggers automatically on:** "map this codebase", "show me the repo tree", "what's in this repo", "give me an overview", "document the project structure", or any onboarding/orientation request.

**Output:** A Markdown file (default `REPO_MAP.md`) with:
- Nested link tree — folders and files with relative links
- Descriptions that explain purpose, not just names
- Highlights section covering entry points, architecture patterns, and notable gaps

## Scripts

### `scripts/walk-repo.sh`

Bash helper used by `repo-tree-mapper` to enumerate repository contents efficiently.

- Uses `git ls-files` inside a git repo (respects `.gitignore` automatically)
- Falls back to `find` outside git repos
- Prunes noise directories: `node_modules/`, `.git/`, `venv/`, `__pycache__/`, `dist/`, etc.

```bash
bash scripts/walk-repo.sh [target_dir] [max_depth]
```

## Installation

Add to your Claude Code plugin path or install via the marketplace.
