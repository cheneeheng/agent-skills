# Lessons Learned

---

## 2026-03-31 — Confirm directory structure before writing many files

**What happened:** Created 8+ files (plugin manifest + 7 skill files) at the repo root level. The user then asked to restructure everything under a `ceh/` subdirectory, requiring all files to be moved.

**Lesson:** When the task involves creating a non-trivial file tree, confirm the intended root location with the user before writing any files. A single clarifying question ("Should the plugin live at the repo root or in a subdirectory?") would have avoided the rework.

---

## 2026-03-31 — Create parent directories before using `mv`

**What happened:** Ran `mv .claude-plugin ceh/.claude-plugin` without first creating `ceh/`. The command failed with "No such file or directory". Had to re-run with `mkdir -p ceh &&` prepended.

**Lesson:** `mv` does not create missing parent directories. When moving into a new directory, always `mkdir -p <dest>` in the same command chain before the `mv`, or verify the destination exists first.

---

## 2026-03-31 — A plugin in the repo does not auto-install; old user-level skills persist

**What happened:** After packaging the skills as a `ceh` namespace plugin under `ceh/`, the system skill list still showed the old `ceh-*` flat names (e.g. `ceh-summarize-chat`). The user invoked `/ceh-summarize-chat`, not `/ceh:summarize-chat`. This is because the old skills remained installed at the user level (`~/.claude/skills/ceh-*/`) and the new plugin was never installed.

**Lesson:** Moving skills into a plugin directory in the repo does not install or activate the plugin. The user must explicitly run `/plugin install` (or manually update `settings.json`) for the new plugin to take effect. Additionally, old user-level skills with the same names will continue to shadow the plugin until they are removed from `~/.claude/skills/`. When completing a plugin migration, call out these two follow-up steps explicitly.

---

## 2026-04-01 — New skill added to plugin but not reflected in README

**What happened:** The `ceh:lessons-learned` skill was created and committed to the plugin, but the README skills table was not updated in the same commit. The omission was only caught and fixed later when the README was being edited for unrelated marketplace changes.

**Lesson:** When adding a new skill to the plugin, update the README skills table in the same commit. Treat the README table as part of the skill definition, not optional documentation.

---

## 2026-04-01 — Placeholder repo URL used in plugin.json

**What happened:** `ceh/.claude-plugin/plugin.json` was created with `"repository": "https://github.com/chen/agent-skills"` — a placeholder using a guessed username. The actual GitHub username is `cheneeheng`. The incorrect URL persisted across multiple commits until it was caught and fixed when creating `marketplace.json`.

**Lesson:** Never use a placeholder repo URL in a manifest file. Look up the actual remote URL with `git remote get-url origin` before writing it, or leave the field empty until it can be verified.

---

## 2026-04-01 — Read tool returns "File unchanged" after a rejected read, even though content is not in context

**What happened:** A Read call for `release-ops/SKILL.md` was rejected by the user mid-session. When the same file was re-read in a follow-up attempt, the Read tool returned "File unchanged since last read" — but the content was never actually available in context. The workaround was to fall back to `Bash cat` to retrieve the content.

**Lesson:** "File unchanged since last read" does not mean the content is in context — it only means the file on disk hasn't changed. If a prior Read was rejected or interrupted and the content is absent from context, use Bash to cat the file directly instead of relying on the Read tool's cache response.
