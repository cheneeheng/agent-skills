# Plugin Dependency & Scenario Bundle Plan

Status: **steps 1–9 implemented** on `feat/plugin-dependencies-and-scenario-bundles`; step 10 (repo
tag + `CHANGELOG.md`) and step 11 (owner-manual local cleanup) outstanding. Per-step commits in §6.
Author: dependency design session, 2026-08-22 (rev 2, same day)
Scope: all `ceh-*` plugins, `.claude-plugin/marketplace.json`, `tools/validate-plugins/validate.py`.
**This plan touches this repo only.** No change here depends on, or modifies, a plugin from another
marketplace.

Companion to `PLUGIN_REORG_PLAN.md`, which established the use-case axis. This plan sits one
level above it: how a user *installs* a coherent set, and how a skill *invokes* another skill
deterministically instead of relying on description matching.

Rev 2 folds in a full reference audit (102 cross-plugin references, every SKILL.md and agent file)
and the decisions taken from it. The audit invalidated most of rev 1's graph — see §5.

---

## 1. Why

Two problems, both raised by the repo owner:

- **Problem A — recall.** 23 plugins and ~77 skills is more than anyone remembers. A user
  should think about the situation they are in, not the catalogue.
- **Problem B — unreliable auto-trigger.** Skill descriptions match inconsistently because the
  phrasing that reaches the model varies with context. Where skill Z genuinely needs skill X,
  hoping X's description fires is not good enough.

The fix has two halves, and they are independent:

- **Invocation.** Skill Z's body instructs the call directly:
  `Invoke the Skill tool with skill="ceh-testing:design-test-cases".` The model is already
  inside Z reading a direct instruction, so this bypasses description matching entirely.
- **Installation.** Plugin `dependencies` guarantee X is installed and enabled, so the call
  above cannot fail with an unknown-skill error.

Dependencies solve installation only. They are the precondition for the invocation half, not a
substitute for it.

---

## 2. What the platform gives us

Source: https://code.claude.com/docs/en/plugin-dependencies (read 2026-08-22).

| Capability | Behavior |
|------------|----------|
| `dependencies` array in `plugin.json` | Bare string `"ceh-testing"` or object `{ "name": ..., "version": "~2.1.0", "marketplace": ... }` |
| Install | Dependencies are **resolved and installed automatically**, transitively |
| Enable | Enabling a plugin enables its dependencies, transitively, at the same scope |
| Disable | Refused while another enabled plugin depends on it; the error gives a chained disable command |
| `defaultEnabled: false` | **Does not protect a dependency** — a dep pulled in by an active plugin installs with `true` regardless of its own default |
| Version ranges | Resolved against git tags named `{plugin-name}--v{version}`, created by `claude plugin tag --push` |
| Bundle plugin | A manifest may be `name` + `version` + `dependencies` only, with no skills/agents/hooks |
| Where `dependencies` lives | `plugin.json` **or** the `marketplace.json` entry. This repo declares it in `plugin.json` only — the docs give no precedence when both are set, and the marketplace copy would be an unenforced duplicate |
| Cross-marketplace | Blocked unless allowlisted. Out of scope: every dependency in this plan is `ceh-*` within `ceh-plugins` |
| Cleanup | `claude plugin prune`, or `claude plugin uninstall <p> --prune` |

There is **no optional dependency**. A declared dependency is always installed. This is the
constraint that forces D13.

Error codes to expect: `dependency-unsatisfied`, `range-conflict`,
`dependency-version-unsatisfied`, `no-matching-tag`. Check with `claude plugin list --json`.

**Not covered by dependencies:** external tooling (a mutation-testing binary, `gh`, `uv`) and
plugins in other marketplaces. Prose fallbacks guarding those stay as they are.

---

## 3. Decisions

Rev-1 decisions kept unless marked. New in rev 2: **D13–D18**.

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | **Scenario bundles**, not tier bundles | A bundle should answer "what am I doing", mirroring the repo's own "skills trigger on moments, not topics" rule one level up. A `ceh-core` tier bundle was rejected: it requires knowing the repo's internal structure before you can install anything. |
| D2 | **No `ceh-core` intermediate node** | It saves repeated lines but removes per-scenario control, needed precisely because `fabled` and `advisor` are experimental and must not be forced into every scenario. Cost accepted: editing several manifests instead of one when the cross-cutting set changes. |
| D3 | **Greenfield extends `-iterate`** | Everything needed to keep working on a thing is also needed while building it. Greenfield = `-iterate` + a planning delta. Avoids duplication and makes the phase transition a no-op — you never switch bundles, you just stop reaching for the planning skills. |
| D4 | **No `plugins-scenario/` folder** | `CLAUDE.md` already rules out tier subfolders; a sibling top-level folder is the same decision relabelled. The `ceh-scenario-` name prefix carries the distinction. The structural invariant (manifest only, no skills) is better enforced by `validate.py` than by a directory. |
| D5 | **Merge `ceh-dev-tools` into the contract plugin** | `explain-until-understood` and `explain-codebase` cross-reference each other purely to disambiguate — they belong in one plugin. Three whole-repo passes (`refactor-repo`, `explain-codebase`, `repo-tree-mapper`) end up co-located, so `refactor-repo` calling `explain-codebase` becomes an in-plugin call. `ceh-dev-tools` is one skill + one agent, below the weight of a standalone plugin. |
| ~~D6~~ | ~~Do not rename `ceh-agent-coding-contract`~~ | **Superseded by D14.** Rev 1 priced only today's cost and missed that every later step of this plan raises the price. |
| D7 | **`ceh-ops` is opt-in, not bundled** | Reported as "not really used". `defaultEnabled: false` cannot exclude it (§2), so the only lever is to omit it from `dependencies`. Says nothing about what `ceh-ops` itself requires — see D17 and §5.3. |
| D8 | **`fabled`, `advisor` and `orchestration` are experimental** | Excluded from every bundle; installed deliberately. Marked as such in the README and in their `plugin.json` `description` fields (that string is what `claude plugin list` shows). `ceh-advisor` warrants an explicit note that it installs always-on session hooks. |
| D9 | **Session-mechanics plugins belong to no scenario** | `summarize-chat`, `orchestration`, and `lessons-learned` are about how you run a *session*, not what you are building. Install once at user scope. |
| D10 | **Bare-string dependencies; no version ranges** | Ranges resolve against per-plugin `{name}--v{version}` git tags. This repo has only repo-wide snapshot tags (`v4.0.2`). Adding ranges requires changing the release flow to tag every plugin at every release. |
| D11 | **Only imperative references become dependencies** | Most cross-plugin references are negative routing in `description` ("Not for tagging, use X"). Those mark *alternatives*; declaring a dependency there installs a plugin the user deliberately steered away from. Refined by D13. |
| D12 | **A cross-cutting plugin may depend only on other cross-cutting plugins** | **Rationale corrected in rev 2.** Rev 1 justified this as "requiring anything creates a cycle" and claimed 4 cycles exist today. The audit found **zero cycles**: `ceh-git-workflow` and `ceh-testing` are true leaves, so an edge from the contract plugin to either is acyclic. The real invariant is layering, and acyclicity is enforced by `validate.py` (D16), not by a blanket prohibition. Stated this way the rule survives content edits; stated rev 1's way it was true only by coincidence — see §5.4. |
| **D13** | **A reference becomes a dependency only if it fires on *every* run of the skill** | The platform has no optional dependency, so a conditional handoff declared as a dependency installs a whole plugin for a branch most runs never reach. `ceh-usability-audit` delegating WCAG to `ceh-web-frontend:accessibility` fires only when the audited subject has a web UI — and anyone auditing a web UI already installed `ceh-web-frontend`. Conditional handoffs stay prose. This is the rule that keeps the graph at 6 edges instead of a 6-plugin closure. |
| **D14** | **Rename `ceh-agent-coding-contract` → `ceh-coding-agent`** | Reverses D6. The plugin holds a behavioral contract, a minimalism reflex, two retroactive-refactoring skills, a usage-limit hook, and an explanation skill; D5 adds `explain-codebase` and `repo-tree-mapper`. "Coding contract" names one of eight things. Every skill in it governs the coding agent's own behavior on a codebase, which `ceh-coding-agent` covers without stretching. Decisive factor: the install base is the owner's own machines, and the rename window closes at step 4 — after that the old string is a hard dependency key in 13 manifests. `ceh-agent-discipline` was rejected: "agent" alone reads as any agent, not the coding one. |
| **D15** | **Bundle set: 7, not 8** | Dropped `ceh-scenario-plugin-authoring` — it described work on *this* repo, which `CLAUDE.md` and `.claude/skills/add-plugin-component/` already own. Renamed `ceh-scenario-content` → **`ceh-scenario-editorial`**: "content" reads as CMS; "publishing" collides with package publishing; "editorial" is the standard name for the function owning everything a reader sees, and is one word like `service`/`library`/`webapp`. |
| **D16** | **`validate.py` enforces the invocation contract** | Any skill named in an `Invoke the Skill tool with skill="X"` instruction must (a) exist, (b) live in the source plugin itself or in a declared dependency, and (c) **not** set `disable-model-invocation: true`. 19 of 77 skills set that flag and the failure is silent (`DECISION_LOG.md:898` records the same degradation from the `fabled-voice` hook work). Also enforces acyclicity, replacing D12's lost justification. |
| **D17** | **`ceh-business-plan` duplicates `plan-schema.md` rather than declaring an edge** | `develop-business-plan:58` reads a file *path* inside `ceh-plan-build-review` — conditional (fires only when the input is an app plan) but unrecoverable if absent, the one case D13 handles badly. The file is already duplicated 3× inside `ceh-plan-build-review` and registered at `docs/CROSS_REFERENCES.md:202-204`; a 4th copy (121 lines) adds one row to an existing block and removes the only cross-plugin file read in the repo. Standard Shared-Standards Duplication Policy. |
| **D18** | **The post-launch suffix is `-iterate`, not `-maintenance`** | The axis is *before first release* vs *after first release*, and most feature work lives on the second side for years. "Maintenance" connotes bugfix-and-keep-the-lights-on, which is exactly why `ceh-plan-build-review` was filed on the wrong side (Q2). `-iterate` names the activity, so someone with a new feature to build picks the right bundle; it also matches the bundle's headline skill, `plan-fullstack-app-iteratively`, and the repo's own "moments, not topics" rule. Rejected: `-existing` and `-ongoing` (state a fact, not an activity), `-brownfield` (means inherited legacy code), `-live`/`-running` (false for a library), `-growth` (excludes patches), `-shipped` (good, but `-iterate` matches the plugin vocabulary). Cost: a verb pairs unevenly with the noun `greenfield`. |

---

## 4. Target graph

Arrow = "the left plugin's skills or agents invoke the right plugin's skills unconditionally, so it
must be installed". Six edges, all evidenced in §5.

```
LAYER 3 — scenario bundles (manifest only, no skills/agents/hooks)

  ceh-scenario-service-greenfield ──┐
  ceh-scenario-library-greenfield ──┼── each depends on its own -iterate bundle
  ceh-scenario-webapp-greenfield ───┘   plus the greenfield delta:
                                          + ceh-scaffolding
                                          + ceh-business-plan
                                        (ceh-architecture and ceh-plan-build-review
                                         are already in the base)
                    │
                    ▼
  ceh-scenario-service-iterate
  ceh-scenario-library-iterate
  ceh-scenario-webapp-iterate
                    │
                    ├── common to all three:
                    │     ceh-coding-agent        (renamed, D14; carries dev-tools content, D5)
                    │     ceh-git-workflow
                    │     ceh-testing
                    │     ceh-documentation
                    │     ceh-release-flow
                    │     ceh-architecture
                    │     ceh-usability-audit     (all three — its skills are stack-agnostic)
                    │     ceh-plan-build-review   (Q2 — post-launch feature work is planned work)
                    │
                    ├── service adds:  ceh-python-service
                    ├── library adds:  ceh-python-library
                    └── webapp adds:   ceh-web-frontend

  ceh-scenario-editorial          ceh-coding-agent, ceh-blog,
                                  ceh-documentation, ceh-seo         (no phase split)

LAYER 2 — plugins that depend on Layer 1 (the complete set; six edges)

  ceh-release-flow      ──► ceh-git-workflow, ceh-documentation   [13 unconditional step rows]
  ceh-python-service    ──► ceh-testing                           [3 agent `skills:` preloads]
  ceh-web-frontend      ──► ceh-testing                           [3 agent `skills:` preloads]
  ceh-python-library    ──► ceh-testing                           [after the step-5 text fix]
  ceh-ops               ──► ceh-coding-agent                      [2 agent `skills:` preloads]
  ceh-orchestration     ──► ceh-coding-agent                      [1 agent `skills:` preload]

LAYER 1 — cross-cutting leaves, declare nothing

  ceh-coding-agent   ceh-git-workflow   ceh-testing
  ceh-fabled         ceh-advisor        [experimental, D8]

NEVER BUNDLED

  experimental (D8):        ceh-fabled, ceh-advisor, ceh-orchestration
  session mechanics (D9):   ceh-summarize-chat, ceh-lessons-learned
  opt-in (D7):              ceh-ops
  declare nothing of own:   ceh-blog, ceh-business-plan, ceh-scaffolding, ceh-architecture,
                            ceh-seo, ceh-evaluation, ceh-usability-audit, ceh-plan-build-review,
                            ceh-documentation
```

`ceh-scaffolding` deliberately declares nothing: it references all three stack plugins, but
those references are advisory (it scaffolds whichever type you name). Declaring them would
install Python service + library + web frontend on someone who only writes libraries.

Worst-case install closure is **3 plugins** (`ceh-ops` → `ceh-coding-agent`; `ceh-release-flow` →
`ceh-git-workflow` + `ceh-documentation`). No transitive blow-up, because every Layer 1 plugin is a
true leaf.

### Example manifests

```json
// plugins/ceh-scenario-service-iterate/.claude-plugin/plugin.json
{
  "name": "ceh-scenario-service-iterate",
  "version": "1.0.0",
  "description": "CEH scenario: building on a Python backend service that already ships.",
  "dependencies": [
    "ceh-coding-agent", "ceh-git-workflow", "ceh-testing",
    "ceh-python-service", "ceh-architecture", "ceh-documentation",
    "ceh-release-flow", "ceh-usability-audit", "ceh-plan-build-review"
  ]
}
```

```json
// plugins/ceh-scenario-service-greenfield/.claude-plugin/plugin.json
{
  "name": "ceh-scenario-service-greenfield",
  "version": "1.0.0",
  "description": "CEH scenario: starting a new Python backend service from nothing.",
  "dependencies": [
    "ceh-scenario-service-iterate",
    "ceh-scaffolding", "ceh-business-plan"
  ]
}
```

---

## 5. Reference audit

Full sweep of every `SKILL.md` and `agents/*.md`, frontmatter and body separated: **102
cross-plugin references** (36 frontmatter, 66 body). Rev 1's figure of 33 undercounted by 3×; it
missed agent frontmatter and most body routing tables.

### 5.1 Reference classes

| Class | Count | Becomes a dependency? |
|-------|-------|----------------------|
| Agent `skills:` frontmatter preload | 6 | **Yes** — hardest form; the agent cannot load its own contract without it |
| Unconditional body invocation | 13 | **Yes** — all in `ceh-release-flow` step tables |
| Negative routing in `description` ("Not for X, use Y") | ~30 | No — marks an alternative (D11) |
| Conditional body handoff ("if it's a UI, delegate to…") | ~20 | No — D13 |
| Boundary/advisory prose ("see X for the mechanics", "pairs with X") | ~30 | No |
| Cross-plugin file-path read | 1 | No — duplicate instead (D17) |

### 5.2 Rev-1 edges that the audit invalidated

Eleven of rev 1's sixteen Layer-2 edges had no supporting reference:

- **No reference in either direction:** `ceh-python-service → ceh-coding-agent`,
  `ceh-python-library → ceh-coding-agent`, `ceh-python-library → ceh-testing`,
  `ceh-web-frontend → ceh-coding-agent`, `ceh-plan-build-review → ceh-coding-agent`.
  Rev 1 assumed `ceh-python-library → ceh-testing` by symmetry with `ceh-python-service`, but the
  service edge comes from three tester agents, and `ceh-python-library` has no agents at all.
  Step 5 makes this edge real by fixing the text, not by asserting it in a manifest.
- **Negative routing only:** `ceh-documentation → ceh-git-workflow` (`update-changelog:8`),
  `ceh-evaluation → ceh-git-workflow` (`evaluate-skill:11`),
  `ceh-seo → ceh-documentation` (3 boundary statements),
  `ceh-usability-audit → ceh-documentation` and `→ ceh-seo` (routing tables).
- **Conditional with an OR-alternative:** `ceh-plan-build-review → ceh-git-workflow`
  (`patch-built-version:111` offers `ceh-git-workflow:release` *or* `ceh-release-flow`).

### 5.3 Edge the audit added

`ceh-ops → ceh-coding-agent`. Both `agents/github-actions.md:16` and `agents/gitlab-ci.md:16`
preload `agent-coding-contract` in `skills:` frontmatter. Rev 1 gave `ceh-ops` no Layer-2 row at
all. Unrelated to D7: not bundling `ceh-ops` says nothing about what `ceh-ops` requires.

### 5.4 Why D12's rationale had to change

`ceh-coding-agent` is Layer 1 and declares nothing — but three of its own references point at other
plugins: `refactor-repo:87` and `shrink-diff:91` name `ceh-testing:verify-behavior-preserved`, and
`refactor-repo:69` names `ceh-git-workflow:branch`. D12 survives only because all three happen to be
conditional under D13 (`refactor-repo:87` fires "for anything past a mechanical transform";
`refactor-repo:69` sits inside Phase 3, gated on user approval; `shrink-diff:77` cites `open-pr` for
its *size limits*, a value rather than a call).

That is a property of six lines of prose, not a structural fact. Rewriting `refactor-repo:87` to
"always pin behavior before refactoring" — a defensible standard and a one-line edit — would make
rev 1's D12 false with nothing to catch it. Hence the restatement in D12 plus the `validate.py`
acyclicity check in D16.

### 5.5 Invocation targets are all callable

All eight targets of the step-5 upgrades are clean of `disable-model-invocation`:
`ceh-git-workflow:{release,branch,commit,open-pr,merge}`,
`ceh-documentation:{update-changelog,update-readme}`, `ceh-testing:design-test-cases`.

`release-flow` and `direct-release-flow` **do** set the flag, correctly: it governs whether the
model may invoke *that* skill, not what the skill's body invokes once a human has typed it.

---

## 6. Implementation checklist

Ordered so each step leaves the repo green. Steps 1–3 are independent of the bundles.

Steps 1–9 landed on `feat/plugin-dependencies-and-scenario-bundles`, verified 2026-08-23 against a
clean tree with `validate.py` green:

| Step | Commit | Note |
|------|--------|------|
| 1 | `9e4d665` | rename `ceh-agent-coding-contract` → `ceh-coding-agent` |
| 2 | `484fd47` | absorb `ceh-dev-tools` |
| 3 | `9641997` | 4th `plan-schema.md` copy + `CROSS_REFERENCES.md:205` |
| 4, 5 | `d6f461c`, `0390149`, `d00c416` | six edges + 16 invocations; later commits fixed the bump level and removed the `marketplace.json` duplicate |
| 6 | `6e549bb` | seven bundles |
| 7 | `cf60012` | scenario shape, dependency resolution, acyclicity, invocation contract |
| 8 | `09d28e0` | scenario table first; experimental marks |
| 9 | `0f9d789`, `4f8230d` | scenario tier, D12/D13, naming rule, rename |

Step 10 lands as repo tag **v5.0.0** (MAJOR: D14 renames a plugin, D5 removes one). Step 11
remains open — owner-manual, after the tag is pushed.

1. **Execute D14 — rename `ceh-agent-coding-contract` → `ceh-coding-agent`**, as its own commit,
   first. 180 occurrences repo-wide. Beyond the obvious (directory, `plugin.json`,
   `marketplace.json`, both READMEs, `CLAUDE.md`, `docs/CROSS_REFERENCES.md`), the non-obvious
   sites are `hooks/load-contract.sh`, `hooks/usage-limit-watch.py`, the `skills:` preloads in
   `ceh-ops/agents/{github-actions,gitlab-ci}.md` and `ceh-orchestration/agents/executor.md`, and
   `ceh-fabled/hooks/load-voice.sh`. Must land before step 4, after which the old string becomes a
   hard dependency key in 13 manifests.
2. **Execute D5** — move `explain-codebase` and `repo-tree-mapper` into `ceh-coding-agent`; remove
   `ceh-dev-tools` from `marketplace.json`; update every `ceh-dev-tools:` reference across skills,
   both README tiers, `CLAUDE.md`, and `docs/CROSS_REFERENCES.md`. MINOR bump. Sequence after
   step 1 so `explain-codebase`'s reference to the contract collapses to an in-plugin one.
3. **Execute D17** — copy `plan-schema.md` to
   `ceh-business-plan/skills/develop-business-plan/references/`, repoint
   `develop-business-plan:58`, add the row to the existing `docs/CROSS_REFERENCES.md` block
   (now 4 copies in lockstep).
4. **Add `dependencies`** to the six Layer-2 plugins per §4. Bare strings only (D10).
5. **Convert the 16 invocation sites** — see §7. Same commit as step 4 for `ceh-release-flow`, so
   the fallbacks never outlive the guarantee that replaces them.
6. **Create the 7 scenario bundles** in `plugins/`, each with `plugin.json` + `README.md`, plus a
   `marketplace.json` entry each.
7. **Extend `validate.py`** per D16:
   - a `ceh-scenario-*` directory contains only `.claude-plugin/plugin.json` and `README.md`;
   - its manifest has a non-empty `dependencies`, every entry present in `marketplace.json`;
   - every `Invoke the Skill tool with skill="X"` names a skill that exists, is in-plugin or in a
     declared dependency, and does **not** set `disable-model-invocation: true`;
   - the dependency graph is acyclic;
   - confirm `plugin_dirs()` at `validate.py:47` tolerates a plugin with no `skills/` or `agents/`.
8. **Restructure `README.md`** — a scenario table above the existing Plugins table, so the install
   path reads scenario-first and the use-case plugins become the reference list underneath. Mark
   `fabled` and `advisor` experimental (D8) in the Categorization table and in their manifest
   `description` fields.
9. **Update `CLAUDE.md`** — the scenario tier, D12 as restated, D13, the `ceh-scenario-` naming
   rule, D4, and the `ceh-coding-agent` rename throughout.
10. **Repo tag + `CHANGELOG.md` entry** per the existing versioning policy. MAJOR: D14 renames a
    plugin and D5 removes one.
11. **Local cleanup** — **manual, done by the repo owner**, after the tag is pushed. See §9.

---

## 7. The 16 invocation sites

Convert each to `Invoke the Skill tool with skill="<plugin>:<skill>"`.

| Source | Sites | Target(s) |
|--------|-------|-----------|
| `ceh-release-flow:release-flow` `SKILL.md:30-39` | steps 1, 2, 4, 5, 7, 8, 9, 10 | `ceh-git-workflow:{release,branch,commit,open-pr,merge}`, `ceh-documentation:{update-changelog,update-readme}` |
| `ceh-release-flow:direct-release-flow` `SKILL.md:31-38` | steps 1, 4, 5, 7, 8 | same set, minus branch/PR/merge |
| `ceh-python-service:python-service-testing` | before `## Unit Tests` (`:33`) | `ceh-testing:design-test-cases` |
| `ceh-python-library:python-library-testing` | before `## Unit Tests` (`:34`) | `ceh-testing:design-test-cases` |
| `ceh-web-frontend:frontend-testing` | before `## Unit Tests` (`:30`) | `ceh-testing:design-test-cases` |

The step tables currently route through a **trigger-phrase indirection** —
`| 4 | Write the changelog | "update the changelog" → ceh-documentation:update-changelog |` — which
is the exact description-matching gamble this plan exists to remove.

The three testing skills are not bookkeeping: `ceh-testing:design-test-cases` is reachable today
**only** through six agent preloads, so the in-conversation path has no access to the technique at
all.

### Fallbacks deleted in the same commit

`release-flow:66,105` and `direct-release-flow:65,101` — "if a step's owning skill is not installed,
apply it inline" and "when the `ceh-git-workflow` agents are installed, dispatch each…".

### Deliberately left as prose

Converting these would drag the closure back to ~6 plugins per install:

| Reference | Why it stays |
|-----------|--------------|
| `ceh-coding-agent:refactor-repo` → `ceh-testing:verify-behavior-preserved`, `ceh-git-workflow:branch` | D12 — Layer 1 declares nothing |
| `ceh-usability-audit` → `ceh-web-frontend:accessibility` (4 sites) | D13 — conditional on the subject having a UI |
| `ceh-scaffolding` → the three stack plugins | Advisory by design; would install all three |
| `ceh-plan-build-review:patch-built-version` → `ceh-git-workflow:release` | Offers an OR with `ceh-release-flow` |
| `ceh-ops:deploy` → `ceh-git-workflow:release` | A precondition, not a call |
| `ceh-testing:audit-test-suite:102` → mutation-testing binary | External tooling, not a plugin |
| `release-flow` step 6 → `revise-claude-md` | Another marketplace; out of this plan's scope (§2) |

The failure mode to guard against is a well-meaning sweep converting every backtick-quoted skill
name into an invocation.

---

## 8. Open questions

- ~~**Q1 — `ceh-seo` in the service bundle?**~~ **Retired.** `ceh-seo` is dropped from all three
  `-iterate` bundles. SEO is a "this thing has a public surface" moment, a property of one release
  rather than of a whole phase, so it is installed deliberately — same shelf as `ceh-ops`
  under D7. `ceh-scenario-editorial` keeps it, where a public surface is the premise.
- ~~**Q2 — `ceh-plan-build-review` phase.**~~ **Resolved: it belongs in the `-iterate` bundles.** Rev 1 put it
  in the greenfield delta on a claimed 3-of-4 majority; the skill descriptions say the opposite.
  `plan-fullstack-app-iteratively` states it "covers greenfield skeletons **and iterative feature
  planning for existing apps**", and `implement-from-plan` / `review-against-plan` consume any plan
  artifact regardless of phase — 4 of 5 skills work post-launch, and only
  `plan-fullstack-app-to-mvp` is greenfield-exclusive. Adding features to a shipped thing is the
  normal case after first release, and it is planned work. Under D3 the greenfield bundles inherit
  the plugin anyway, so the greenfield delta shrinks to `ceh-scaffolding` + `ceh-business-plan` and
  nothing is lost. The deferred refactor is dropped: `patch-built-version` explicitly routes
  feature work to `plan-fullstack-app-iteratively`, which is an argument for keeping them in one
  plugin, not for splitting them.
- ~~**Q5 — is "maintenance" the right word?**~~ **Resolved: no. The suffix is now `-iterate`.**
  See D18.
- **Q3 — is `ceh-ops` unused because you rarely deploy, or because `deploy` / `incidents` /
  `rollback` never auto-trigger?** If the second, D7 treats a symptom: the fix belongs in those
  three descriptions, and that is the same reliability problem that motivated this whole plan.
- **Q4 — `ceh-scenario-` prefix.** Confirmed. Makes the tier obvious in `claude plugin list` and
  sorts the greenfield/iterate pairs adjacently, at the cost of long names.

---

## 9. Local cleanup after the rename

> **Manual step — the repo owner runs this personally.** It is recorded here for reference only.
> No agent should execute any part of this section, and checklist step 11 is not agent work: it
> touches the owner's global Claude Code state and 26 unrelated project directories, all outside
> this repo.

Owner's machines only; run after step 10's tag is pushed, because the `ceh-plugins` marketplace is
`github: cheneeheng/agent-skills` with `autoUpdate: true` and would otherwise reinstall the old
names.

1. `claude plugin marketplace remove ceh-plugins` then
   `claude plugin marketplace add cheneeheng/agent-skills`. Rebuilds `installed_plugins.json`
   (115 stale local-scope entries across 20 project paths), the `plugins/cache/ceh-plugins/`
   extracted copies, the `plugins/marketplaces/ceh-plugins/` checkout, and
   `plugin-catalog-cache.json`.
2. `claude plugin prune` for anything the remove missed.
3. Per-project `enabledPlugins` keys are **not** covered by either command — 26
   `.claude/settings.local.json` files hold 164 stale `@ceh-plugins` keys. Four of them also carry
   a `permissions` block, so strip keys rather than deleting files. Script:
   `.agents_workspace/strip-ceh-plugins.py`, dry-run by default, `--apply` to write:
   `python .agents_workspace/strip-ceh-plugins.py <projects-root> [--apply]`.

Unverified: whether a stale `enabledPlugins` key naming a nonexistent plugin errors or is silently
ignored. The cleanup does not depend on the answer.

---

## 10. Risks

- **Disable lock-in.** Once `ceh-ops` and `ceh-orchestration` depend on `ceh-coding-agent`,
  `claude plugin disable ceh-coding-agent` is refused until both are disabled first. For an
  intentional always-on contract this is the point, but it is a real behavior change.
- **Rename breakage.** D14 orphans every existing install of `ceh-agent-coding-contract`. Accepted
  because the install base is the owner's own machines (§9), and because the cost only grows.
  Land the rename and the `dependencies` rollout in **separate commits** — a typo in a dependency
  key fails at install time with `dependency-unsatisfied`, not at edit time.
- **Silent invocation failure.** A future session setting `disable-model-invocation: true` on an
  invocation target breaks a release flow with no error at author time. D16's validator rule is
  the only thing standing in front of this; 19 of 77 skills already set the flag.
- **`range-conflict` at scale.** Not a risk under D10 (bare strings). It becomes one the moment
  version ranges are introduced across many plugins constraining the same few cross-cutting deps.
- **Per-plugin tagging cost.** D10 defers this, but any future version constraint requires
  `{plugin}--v{version}` tags on every plugin at every release — a change to the release flow.
- **The duplication policy is untouched.** Dependencies install whole plugins; they give one skill
  no way to reference another plugin's content. The uv/pytest block duplicated across
  `ceh-python-service` and `ceh-python-library` stays duplicated, `plan-schema.md` gains a 4th copy
  (D17), and `docs/CROSS_REFERENCES.md` stays load-bearing.
- **The `CLAUDE.md` tier table becomes wrong** the moment the rename lands — step 9 is not
  optional bookkeeping.
