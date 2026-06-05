# Decision Log

### Entry 1

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-05-26
**Task:** Improve ceh-blog skill triggering reliability and token efficiency.

**Context:** The request — "go through the skill description and adapt them based on best practices, also make them token efficient without losing context" — was ambiguous about whether "them" meant the `description` frontmatter only or the full SKILL.md bodies.
**Decision:** Scoped the change to the four `description` frontmatter fields only. The description is the always-loaded field that drives triggering (the stated problem) and counts against the persistent skill-selection context budget, so it is the correct lever for both "best practices" and "token efficient." Bodies were left intact: they load one skill at a time (negligible always-on cost), `CROSS_REFERENCES.md` documents that the repo deliberately inlines duplicated body content, and trimming prose risks the "losing context" the user warned against. Rewrote each description to lead with what the skill does, keep high-signal trigger phrases, and preserve the inter-skill routing ("use X instead") — while cutting redundant framing (~95 words → ~75 words each).
**Impact / Risk:** Low. Fewer literal trigger phrases could marginally reduce recall; mitigated by keeping the most distinctive phrases and the discriminating input-state clause for each skill. Version bumped PATCH (1.0.2 → 1.0.3) in `plugin.json` and `marketplace.json` per repo versioning rules.
**Outcome:** Four descriptions rewritten; committed on branch `fix/blog-skill-triggering`.

---

### Entry 2

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Execute the plugin reorganization (`docs/PLUGIN_REORG_PLAN.md`).

**Context:** The user asked to "create a new feature branch and implement everything in the reorg."
The plan itself prescribes six phases, each shipped as its own PR with its own version bumps.
**Decision:** Honored the explicit instruction — one branch (`refactor/plugin-reorg`) — but kept the
six phases as six separate, self-consistent commits (each updates its own manifests/marketplace) so
the history stays reviewable phase-by-phase. The user's direct instruction overrides the plan's
per-PR guidance (authority hierarchy).
**Impact / Risk:** A single large PR instead of six; mitigated by clean per-phase commit boundaries.
**Outcome:** Six phase commits + one review-fix commit on the branch.

---

### Entry 3

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Distribute the `postgresql` skill content (Phase 3).

**Context:** The plan's per-skill map says "TRIM + MERGE postgresql into data moments
(`domain-modeling` + migrations)" but also lists the target as `ceh-python-service`. `domain-modeling`
is explicitly kept stack-agnostic in `ceh-architecture`, so folding Postgres-specific DDL into it
would re-pollute it with stack specifics — contradicting the reorg's goal.
**Decision:** Split by concern instead of dissolving the skill: tenant-isolation/query rules →
`asyncpg`; migration safety → `alembic`; and the Postgres schema-design content kept as a trimmed
`postgresql` skill **moved into `ceh-python-service`** (it is genuinely Postgres + service specific).
**Impact / Risk:** One more skill in `ceh-python-service` than a strict "merge everything" reading;
keeps `domain-modeling` stack-agnostic.
**Outcome:** `ceh-python-service` has `postgresql` (schema design), `asyncpg` (access + tenant
isolation), `alembic` (migrations).

---

### Entry 4

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Test agents for `ceh-python-library` (Phase 4).

**Context:** The plan's agent table notes the python tester agents are in `ceh-python-service`
"(share with library)" — ambiguous between duplicating the agents into the library plugin and
leaving them in the service plugin.
**Decision:** Did **not** duplicate the three tester agents (and their scripts) into
`ceh-python-library`. Library testing standards are carried by the duplicated `python-testing` skill;
duplicating heavy agent + script assets exceeded what Plan §4 scoped (env + testing *skills* only).
**Impact / Risk:** A pure library project does not get dedicated tester agents. Can be added later if
needed.
**Outcome:** Tester agents remain solely in `ceh-python-service`.

---

### Entry 5

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Handle `scripts/sync-stubs.ps1` (Phase 6).

**Context:** The script syncs stub reference files from
`ceh-python-backend/skills/python-backend/references` to other plugins — a path that did not exist
even before the reorg, and all of whose source/destination plugins were renamed or removed.
**Decision:** Deleted the script as dead code. The duplication mechanism of record is
`CROSS_REFERENCES.md` with same-session manual propagation (per CLAUDE.md), not an automated sync.
**Impact / Risk:** None — the script was non-functional. Only referenced historically in CHANGELOG.
**Outcome:** `scripts/sync-stubs.ps1` removed.

---

### Entry 6

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Versioning for the reorg (Phase 6).

**Context:** Renamed plugins are breaking changes; the plan accepts this. Unclear what bumps the
unchanged-but-affected plugins should take.
**Decision:** Bumped all four renamed plugins and `ceh-git-workflow` (lost the `gitignore` skill,
`open-pr` absorbed the definition-of-done gate — a breaking content removal) to **3.0.0**. New
plugins (`ceh-python-library`, `ceh-scaffolding`) start at **1.0.0**. Untouched plugins keep their
versions. The repo CHANGELOG entry is **3.0.0**, but the repo git tag was **not** cut on the feature
branch — tagging is a release action deferred to merge-to-main.
**Impact / Risk:** Breaking version jumps for renamed/`git-workflow` plugins (intended).
**Outcome:** Marketplace and per-plugin manifests consistent; CHANGELOG 3.0.0 added.

---

### Entry 7

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Post-review fix — orphaned "layer boundaries" invariant.

**Context:** After `repository-structure` moved to `ceh-scaffolding`, the architecture SessionStart
hook and README still attributed the always-on "layer boundaries" invariant to `domain-modeling`,
which no longer contained that content. Options: drop the invariant, point the hook at a scaffolding
skill, or give it a home in `domain-modeling`.
**Decision:** Added a "Layer Boundaries" section to `domain-modeling`. Layer boundaries are a
design-time invariant that belongs with domain modeling; the concrete directory layout stays in
`ceh-scaffolding`. This keeps the always-on hook tag accurate and the depth reference in the same
plugin. Registered the resulting overlap with `scaffold-python-service` in `CROSS_REFERENCES.md`.
**Impact / Risk:** New duplicated block (tracked).
**Outcome:** Fixed in commit `fix(reorg): correct post-review inconsistencies`.

---

### Entry 8

**Type:** Decision
**Mode:** Autonomous
**Timestamp:** 2026-06-05
**Task:** Remove `msg.txt` from history (user-directed).

**Context:** Per-phase commits had inadvertently tracked the temp commit-message file `msg.txt`
(swept in by `git add -A`). The user asked to remove it from all commits while not altering the
old commits' content for the review fixes.
**Decision:** Committed the review fixes first as a new commit, then rewrote the branch with
`git filter-branch --index-filter` over the reorg range to strip `msg.txt` from every commit, and
purged the `refs/original` backup + reflog + gc. Future commit messages are written to a temp file
outside the repo to prevent recurrence.
**Impact / Risk:** Commit SHAs were rewritten. Safe — the branch existed only locally at the time;
later pushed to origin fresh.
**Outcome:** `msg.txt` absent from all commits and all objects (`git rev-list --all` = 0 matches).
