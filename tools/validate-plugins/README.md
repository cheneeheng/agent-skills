# validate-plugins

Repo-integrity checker for the `ceh-*` plugins. Stdlib-only Python — runs locally on any OS
and in CI with no install step. Used by `.github/workflows/validate.yml`.

```bash
python tools/validate-plugins/validate.py
```

Exits non-zero and prints a grouped list of problems if any check fails.

## Checks

| Group | What it verifies |
|-------|------------------|
| `manifests`  | Each `ceh-*/.claude-plugin/plugin.json` is valid JSON, `name` matches its directory, `version` is semver. `marketplace.json` lists every plugin with a matching version and an existing `source` path; no plugin is missing or unlisted. |
| `skills`     | Every `skills/<name>/SKILL.md` has `name` + `description` frontmatter and `name` matches the directory. |
| `agents`     | Every `agents/<name>.md` has `name` + `description` frontmatter. |
| `references` | `references/...` mentions and `${CLAUDE_PLUGIN_ROOT}/scripts/...` mentions in skill/agent files resolve to a real file. |
| `skill-refs` | `plugin:component` references resolve to an existing skill or agent. |
| `scripts`    | `*.sh` pass `bash -n` (and `shellcheck` when available); `*.py` pass `py_compile`. |

`shellcheck` and `bash` are used when present and skipped otherwise, so a missing tool never
causes a false failure — CI runs them because GitHub-hosted Ubuntu runners ship both.
