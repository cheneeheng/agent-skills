# Git Workflows

Step-by-step command sequences for common operations. Each sequence enforces the standards
defined in the other reference files — branch naming, commit format, merge policy, etc.

Use the Bash tool to execute these commands.

---

## Start new work

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-description>   # see branching.md for naming rules
```

---

## Commit changes

```bash
git add <files>
git commit -m "<type>(<scope>): <short summary>"   # see commits.md for format rules
```

For multi-line commit messages (body or footer needed):

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <short summary>

<body — explain why, not what>

<footer — BREAKING CHANGE or Closes #NNN>
EOF
)"
```

---

## Keep branch up to date with main

```bash
git fetch origin
git rebase origin/main
# if conflicts arise, resolve them, then:
git rebase --continue
```

---

## Push and open a PR

```bash
git push -u origin <branch-name>
gh pr create \
  --title "<type>(<scope>): <short summary>" \
  --body "$(cat <<'EOF'
## What
<!-- one sentence -->

## Why
<!-- reason + ticket link -->

## How
<!-- approach if non-obvious -->

## Testing
<!-- what was tested -->

## Checklist
- [ ] All CI checks pass
- [ ] Tests added or updated
- [ ] No `any` / `@ts-ignore` / `# type: ignore` introduced
- [ ] No secrets or credentials in code
- [ ] Migrations (if any) are backward-compatible
- [ ] DECISIONS.md updated (if a durable decision was made)
EOF
)"
```

The PR title must follow Conventional Commits format — it becomes the squash commit message on merge.

---

## After PR is merged

```bash
git checkout main
git pull origin main
git branch -d <branch-name>
git push origin --delete <branch-name>
```

---

## Hotfix

```bash
# 1. Branch
git checkout main && git pull origin main
git checkout -b fix/critical-<description>

# 2. Fix and commit (minimal scope only)
git add <files>
git commit -m "fix(<scope>): <description>"

# 3. Push and open PR (1 approval minimum, all CI must pass)
git push -u origin fix/critical-<description>
gh pr create --title "fix(<scope>): <description>"

# 4. After merge — bump PATCH version, tag, clean up
git checkout main && git pull origin main
git tag v<X.Y.Z>
git push origin v<X.Y.Z>
git branch -d fix/critical-<description>
```

---

## Tag a release

```bash
# 1. Bump version in pyproject.toml and package.json, commit
git add pyproject.toml package.json
git commit -m "chore: bump version to v<X.Y.Z>"

# 2. Tag and push
git tag v<X.Y.Z>
git push origin main
git push origin v<X.Y.Z>
```

Never tag a commit that hasn't passed all CI checks.
