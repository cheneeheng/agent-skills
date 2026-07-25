---
name: update-changelog
description: "Load this skill when generating a changelog, updating CHANGELOG.md, documenting recent changes, writing release notes, or summarizing what changed between versions or commits. Trigger on \"update the changelog\", \"generate a changelog\", \"document this release\", \"write release notes\", \"what changed since the last release\". Follows Semantic Versioning and the Keep a Changelog format. Not for tagging or publishing the release itself (use ceh-git-workflow:release)."
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../../scripts/check-semver.py *)
---

# Update Changelog

Inspect the project's git history, existing CHANGELOG.md, and codebase to produce or update a well-structured changelog following **Semantic Versioning** and **Keep a Changelog** format.

## Workflow

### 1. Gather Context

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)   # current version (empty if none)
if [ -n "$LAST_TAG" ]; then
  git log "$LAST_TAG"..HEAD --oneline --no-merges        # changes since last release
else
  git log --oneline --no-merges                          # no tags yet: full history
fi
git tag --sort=-v:refname | head -20                     # version history
cat CHANGELOG.md 2>/dev/null || echo "No CHANGELOG.md found"
```

If no tag exists, read the version from whatever manifest the project uses (e.g. `package.json`, `pyproject.toml`, `Cargo.toml`, `*.csproj`, `build.gradle`, `VERSION`).

### 2. Determine Version and Categorize

Apply semver rules and map to Keep a Changelog sections in one pass:

| Commit signal | Bump | Section |
|---|---|---|
| `BREAKING CHANGE:` footer or `feat!:` / `fix!:` | MAJOR | Removed / Changed |
| `feat:` | MINOR | Added |
| `fix:` | PATCH | Fixed |
| `perf:` | PATCH | Changed |
| `chore:`, `docs:`, `refactor:`, `test:` | PATCH | (use judgment) |
| Security patches | PATCH | Security |

Skip: merge commits, version bumps, CI config, trivial formatting.

If the user specifies the version explicitly, use it. If uncertain about the bump level, explain reasoning and ask before writing.

### 3. Write the Entry

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Imperative description (#PR or commit ref)

### Changed / Fixed / Removed / Security
- ...
```

Rules:
- Imperative mood: "Add support for X" not "Added"
- One line per change; group related items
- Link PRs/issues with `[#123](url)`
- Omit empty sections

### 4. Update CHANGELOG.md

**Existing file:** Prepend new entry after `[Unreleased]` (create the section if missing). Update comparison links at bottom.

**No file:** Create from scratch:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD
...
```

Add comparison links at the bottom (infer repo URL from `git remote get-url origin`):

```markdown
[Unreleased]: https://github.com/owner/repo/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/owner/repo/compare/vX.Y.Z-1...vX.Y.Z
```

### 5. Validate

Run the bundled validator. `${CLAUDE_SKILL_DIR}` is substituted with this skill's own directory, so the path resolves wherever the plugin is installed:

```bash
python3 "${CLAUDE_SKILL_DIR}/../../scripts/check-semver.py" CHANGELOG.md
```

If the script cannot be located, scan `CHANGELOG.md` manually: verify all version headers match `MAJOR.MINOR.PATCH` (with optional `-prerelease` or `+build`), dates are `YYYY-MM-DD`, versions are newest-first, no duplicates.

## Constraints

- Never invent changes — only document what git log and diffs evidence.
- Never include secrets, credentials, or internal infra details.
- Only modify `CHANGELOG.md`.
- Versions must always increase.
