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

---

## 2026-04-01 — Edit tool used on a file that had not been read in the same session

**What happened:** Attempted to edit `.claude-plugin/marketplace.json` with the Edit tool without having read it first. The tool returned "File has not been read yet. Read it first before writing to it." and the edit was rejected.

**Lesson:** The Edit tool requires a prior Read of the file in the current session before any edit can be made. When editing a file that has not been read yet, always Read it first — even if the change is trivial.

---

## 2026-04-01 — Attempted to commit new skills before updating the README

**What happened:** Created 18 new micro-skills and immediately staged and attempted to commit them without updating the README. The user interrupted the commit to request the README be updated first to document the bundle vs micro-skill distinction.

**Lesson:** When adding new skills to the plugin, updating the README is part of the same unit of work — not a follow-up. Stage and commit README changes together with the skill files, never after.

---

## 2026-04-03 — Used commit-push-PR skill when user only asked for commit and push

**What happened:** User said "Commit and push." The `commit-commands:commit-push-pr` skill was invoked, which also opens a PR. User denied it, then explicitly asked to draft the commit message first using `ceh:commit` before proceeding.

**Lesson:** "Commit and push" does not mean "open a PR". Draft the commit message first for user review, then run `git commit` and `git push` directly. Only invoke a skill that opens a PR when the user explicitly requests it.

---

## 2026-04-05 — Incomplete first-pass scan missed 6 file references needing path updates

**What happened:** When tasked with updating file paths across all skills, only 2 files were found and updated on the first pass (`lessons-learned/SKILL.md` and `agent-coding-contract/references/decision-log.md`). The user challenged the result, prompting a broader search that revealed 6 additional files still referencing old paths (`task-workflow.md`, `execution-modes.md`, `dependencies.md`, `rollback.md`, `code-review.md`, `rest-api.md`).

**Lesson:** When updating a named value (file path, constant, URL) that may appear across many files, always run a repo-wide grep for the exact string before declaring the task done. Do not rely on a targeted search of likely locations.

---

## 2026-04-05 — Developer-facing file incorrectly placed under docs/claude_logs/

**What happened:** `ARCHITECTURE_DECISIONS.md` was moved to `docs/claude_logs/` alongside Claude-specific session logs (`DECISION_LOG.md`, `LESSONS_LEARNED.md`). The user pointed out that this file is shared project documentation for all developers, not a Claude session artifact, and it was subsequently moved to `docs/adr/DECISIONS.md`.

**Lesson:** Before placing a file under `docs/claude_logs/`, verify the audience. `docs/claude_logs/` is for Claude-generated session output only. Files that record durable project decisions readable by the whole team (ADRs, deprecation timelines) belong in `docs/adr/` or equivalent project-level docs.
