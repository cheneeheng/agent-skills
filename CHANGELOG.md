# Changelog

Versions follow [Semantic Versioning](https://semver.org/).
Versions refer to the Marketplace versions.

---

## [3.29.4] — 2026-08-11

`gh pr merge --merge --auto --delete-branch` no longer runs. Claude Code's auto-mode permission
classifier reads `--delete-branch` as a destructive flag and blocks the command, so the flag does
not cost you a deleted branch — it costs you the merge. Every `gh pr merge` in the repo drops it:
two in `merge` (the auto-merge probe and its direct fallback), two in `open-pr` (the Auto-Merge
section and the tail of the Command block).

Dropping the flag removes the only thing that deleted the remote branch, so the skills replace it
with a report rather than pretending the cleanup still happens. `merge` gains a *Reporting the
remote branch* section: read `gh api repos/{owner}/{repo} --jq .delete_branch_on_merge`, then say
either that GitHub deleted the branch or that the branch is still there and
`git push origin --delete <branch>` removes it. The same applies when auto-merge is queued rather
than merged now — the branch outlives the queue either way. `branch-merger` reports the branch
state instead of claiming "branch deleted (remote/local)", and `release-flow` step 9 asks for it in
its gate.

The standalone git deletion commands are untouched. `git branch -d` and `git push origin --delete`
in the local-branch path and in `hotfix` are separate commands, not the blocked one, and removing
them would drop cleanup that still works.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.2.8 |
| `ceh-release-flow` | v1.1.9 |

### Fixed

- **`ceh-git-workflow` / `merge`, `open-pr`** — removed `--delete-branch` from all four
  `gh pr merge` invocations, with an inline note naming the permission classifier as the reason so
  it is not re-added.

### Changed

- **`ceh-git-workflow` / `merge`** — new *Reporting the remote branch* section keyed on
  `delete_branch_on_merge`, covering both the merged-now and queued-auto-merge cases; the
  description's cleanup summary now says "delete the local branch, report whether the remote branch
  survived".
- **`ceh-git-workflow` / `open-pr`** — the Auto-Merge section and the Command block check
  `delete_branch_on_merge` and tell the user when the branch will still be there after the PR lands.
- **`ceh-git-workflow` / `branch-merger` agent** — rules ban the flag; the return format reports
  remote-branch state rather than asserting deletion.
- **`ceh-release-flow` / `release-flow`** — step 9 renamed "Merge and clean up"; its gate now
  includes the remote-branch state being reported.
- **`CROSS_REFERENCES.md`** — the auto-merge probe entry records the `--delete-branch` ban and the
  `delete_branch_on_merge` check as shared, and the direct-merge fallback as `merge`-only.

---

## [3.29.3] — 2026-08-11

v3.29.2 gave `user-operator-guide` a filename for every page and nothing else. A reader who landed
on `how-to/HT-02-export-data.md` — from a search, a link, a pasted path — had no way back to the
index and no way on to `HT-03`, and the numbering that encoded reading order was visible only to
whoever listed the directory. The new Phase 4 closes that: a breadcrumb under the H1, a prev/next
footer at the bottom of every subfolder page, and an H1 that repeats the file's ID so a printed or
pasted page still says where it came from. Chains run **within a subfolder**, which is where the
contiguous numbering lives, so prev/next point at siblings and need no `../`; root-level pages are
unnumbered, belong to no chain, and get the breadcrumb alone.

The second half of Phase 4 is about Markdown that renders the way it reads in source. A single
newline is not a line break — two lines separated by one collapse into a paragraph, which is the
most common way a finished guide arrives looking wrong. The rules that follow are the ones that
actually bite: blank lines before and after every list, table, fence, blockquote and heading; three
spaces of indent to keep a nested fence inside a numbered step instead of restarting the list at 1;
no hard-wrapping at a fixed column. The procedure template in Phase 5 now applies its own rule to
itself — When/Prerequisites/Time were stacked bold labels relying on single newlines, and are a
bullet list.

Both halves are salvaged from `docs/guide-file-naming-and-nav` (`90ed1b7`, 2026-07-31), a branch
that solved the v3.29.2 naming problem a different way — prefix by audience, `HT`/`OP` only,
numbering global per prefix across the whole tree — and was superseded. Its page-furniture content
was orthogonal to that disagreement and worth keeping, so it was rebased onto the released scheme
rather than merged: chains became per-subfolder, and root pages left the chain entirely. The branch
carries nothing unsalvaged now.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-documentation` | v1.1.6 |

### Added

- **`ceh-documentation` / `user-operator-guide`** — Phase 4 *Page furniture and markdown that
  renders*: per-page breadcrumb and per-subfolder prev/next footer with dead-link and relative-path
  rules, `index.md` as the unfootered hub listing every page, H1 repeating the file ID, and a
  line-break section covering the single-newline trap, blank lines around block elements, 3-space
  continuation indent, heading levels, and table shape.

### Changed

- **`ceh-documentation` / `user-operator-guide`** — phases renumbered (write-each-procedure 4 → 5,
  self-review 5 → 6); the Output section now cites Phases 3-4; two self-review checklist items added
  (navigation present with no dead or cross-chain links; no reliance on a single newline for a
  break). Renumbering a subfolder now explicitly requires fixing the affected footers, not only the
  links in prose.

---

## [3.29.2] — 2026-08-11

`user-operator-guide` told an agent to build a cross-linked tree under `docs/guide/` for anything
broader than a single topic, and then said nothing about what to call the files in it. The example
tree used plain names — `how-to/reset-password.md`, `operations/install.md` — so every guide invented
its own layout, and the order a reader should follow the pages in existed only inside `index.md`.
Sort a subfolder and you learned the alphabet, not the sequence.

Files directly under `docs/guide/` keep plain names. Every file inside a subfolder is now
`<PREFIX>-<NN>-<name>.md`: a capitalized abbreviation of the subfolder name, at least two characters
and unique across the tree (`how-to/` → `HT`, `operations/` → `OP`), then a two-digit number
restarting at `01` in each subfolder. A nested folder chains its parent prefix and starts its own
sequence — `operations/database/` → `OP-DB-01-backup.md`. A subfolder holds at least two files; one
file is not a folder, and a root-level topic that grows to two moves down into one.

Two choices in that scheme are the kind that get quietly reversed later, so both carry their
reasoning in `ceh-documentation/README.md`. **Numbers stay contiguous**: the number *is* reading
order, so inserting or deleting a guide renumbers the rest of that subfolder and every link to a
renamed file is updated in the same pass. Appending at the end — the common case — renumbers nothing.
The alternative, append-only numbers with gaps, was rejected because it demotes the number to an
arbitrary ID, at which point numbering earns nothing; it only becomes the better trade if these
filenames ever get referenced from outside the repo. **The scheme beats the docs system**: Docusaurus,
MkDocs and mdBook derive nav order from filenames and would otherwise compete with the prefix, so
nav order and page metadata go in frontmatter (`sidebar_position`, `title`) or nav config, never in
a rename out of the scheme.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-documentation` | v1.1.5 |

### Changed

- **`ceh-documentation` / `user-operator-guide`** — Phase 3 gains a *How to name the files* section
  and an example tree showing prefixes, per-subfolder numbering and a nested chained prefix; the
  docs-system deference sentence now points nav order at frontmatter instead of at filenames; Phase 5
  gains two checklist items (naming shape, contiguous numbering with links updated); the Output
  section names the scheme. The plugin README documents the two reversible choices and why the
  alternatives lost.

---

## [3.29.1] — 2026-08-10

Four more scenario passes over `explain-until-understood`, the skill v3.29.0 shipped. The eight-
scenario audit before that release found gaps in what the skill *covered*; these passes found
places where the text the skill already had either dead-ended, contradicted itself, or pushed the
agent toward output it cannot honestly produce. That is a different class of defect, and it only
shows up by walking a reader through the procedure rather than checking the procedure has a step
for each case.

The sharpest one was in the escalation ladder, the part of the skill that exists precisely for when
an explanation has already failed. Attempt 3's next-step cell read "stop escalating — you skipped
step 2", while attempt 4 is *defining the primitives*, which is step 2. An agent reading the table
literally stopped one row short of the fix the prose underneath then prescribed. Two others were
self-contradictions: "grep before giving either" made the grep erase one of the two answers it was
meant to choose between, and step 3 gated state-changing commands while leaving a full test suite or
build — read-only, expensive, and gated by the contract — allowed by its own wording.

The remaining fixes are about what the skill demands of a reply. Step 5 is listed as required reply
content, so an agent explaining straightforward code was pressed to produce a "what you would
wrongly conclude" for code that has no subtle failure — a fabrication, against the skill's own
evidence rule. Step 7 routed any wrong self-test answer into a full re-explanation, when a wrong
answer localizes the miss and the rest landed. And step 1 had one branch for "no artifact", covering
both a repo file behind a wall and a subject that has no artifact by nature, so explaining a
protocol produced every sentence tagged unverified.

One fix crosses plugins. The shared "Don't paste code" rule capped snippets at three lines with no
exception, which made an agent paraphrase a constant, threshold, regex, or status string that *is*
the behavior — and a paraphrased value loses the mechanism. Such a literal is now quoted verbatim
outside the ceiling. That bullet is a `CROSS_REFERENCES.md` shared block, so the same wording landed
in `explain-codebase` as canonical and the block description was updated with it.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.9.1 |
| `ceh-dev-tools` | v1.2.2 |

### Fixed

- **`ceh-agent-coding-contract` / `explain-until-understood`** — escalation ladder no longer
  dead-ends at attempt 3; the Honesty rule no longer makes a grep erase the answer it selects
  between; step 3 now gates read-only-but-heavy runs (test suite, build, repo-wide lint) as the
  contract does, not just state-changing ones; step 5 permits saying a path is straightforward
  instead of inventing a failure mode; step 7 scopes a re-explanation to the idea the wrong answer
  missed, and routes a wrong answer about a primitive straight to attempt 4; step 1 separates an
  artifact you cannot reach (mark every claim unverified) from a subject that has none by nature
  (say once that it comes from knowledge); *Scale to the ask* gains an upper bound — name the slices
  and explain one rather than compressing a subject too large for a single explanation.
- Earlier passes on the same branch: the *Persisting* section granted the one repo path it had
  described as unowned and then forbidden, `git log` was ordered after the diff and labelled claimed
  intent for a "what changed since `<tag>`" ask, the ladder stated what carries over between
  attempts, step 3 was named as both what you do and what the reply contains, an unfamiliar tool
  with no read-only run got a defined move, and silence after a self-test stopped reading as a miss
  signal.

### Changed

- **`ceh-dev-tools` / `explain-codebase`** and **`explain-until-understood`** — the shared "Don't
  paste code" rule now exempts a literal that *is* the behavior (a constant, threshold, regex, or
  status string), quoted verbatim. `CROSS_REFERENCES.md` updated to match.

---

## [3.29.0] — 2026-08-09

A new skill in `ceh-agent-coding-contract`, `explain-until-understood`, for the moment when someone
needs to understand code rather than change it. It comes out of a session where three attempts at
explaining the same two concepts failed and the fourth worked. Every failed attempt had restated
the previous one with more words; the one that worked opened by defining the primitives the earlier
three had all assumed. That is the skill's content — establish foundations before the specific case,
verify claims by running them rather than describing them, draw structure and time in ASCII, frame a
subtle failure as "what you would wrongly conclude", and when an explanation misses, change the
representation instead of restating it.

The plugin choice was the argued part. `ceh-documentation` was wrong: every skill there produces a
persisted artifact for a third party, and this one's output is a conversation. `ceh-dev-tools` is
the closest sibling by content but is per-need tooling, so it is not loaded when someone says "I'm
lost" mid-session. `ceh-agent-coding-contract` is the plugin loaded in every session, which is what
makes the skill reachable at all. Its manifest description widened from "agent coding contract" to
"agent behavior contract" to admit a second skill that is not about writing code — `usage-limit-handoff`
was the first.

`disable-model-invocation: true` is set, so the skill never auto-fires; it is typed, like
`refactor-repo`. That removed any trigger competition with `ceh-dev-tools:explain-codebase` and let
that skill's frontmatter stay exactly as it was. The two skills are genuinely different jobs — one
writes a repo-wide file for an absent reader and has an accounting requirement, the other holds a
conversation with a present reader and has an escalation ladder for when it misses — but three of
their rules are identical, so those are now copied word for word and registered in
`CROSS_REFERENCES.md` with `explain-codebase` as canonical.

An audit against eight scenarios after the skill was written found five gaps, all fixed before
release. Four were coverage: a release catch-up and an unfamiliar tool both fell outside "read the
real code first", a cold invocation had no way to locate its rung on the escalation ladder, and
nothing scaled the procedure down for a one-line question. The fifth was safety — "run the tool, the
command, the throwaway script" authorized a state-changing command as an illustration, which the
contract's Validation Policy requires be requested first.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.9.0 |
| `ceh-dev-tools` | v1.2.1 |

### Added

- **`ceh-agent-coding-contract` / `explain-until-understood`** — manual-only skill for explaining a
  subsystem, a design, a set of changes, or an unfamiliar tool to the person in the session. Seven
  procedure steps, the prose → steps → pictures → primitives escalation ladder with the rule that a
  miss at pictures means a skipped foundation, an explicit boundary on persisting the explanation
  (nothing by default, `.agents_workspace/` scratch notes in scope, repo docs hand off), and a
  scale-to-the-ask clause so a one-line question does not draw all seven steps. Writes no files.
- `CROSS_REFERENCES.md` — an entry registering the three rules shared word for word between
  `explain-codebase` (canonical) and `explain-until-understood`: "Evidence over inference", "Don't
  paste code", and "Describe what exists today".

### Changed

- **`ceh-agent-coding-contract`** — manifest description widened from "agent coding contract:
  autonomous execution mode and the five-step task workflow" to "agent behavior contract", covering
  write-less-code minimalism and how the agent explains its work.
- **`ceh-dev-tools` / `explain-codebase`** — one row added to its "Not the same as" table pointing at
  the manual `explain-until-understood` command. Frontmatter unchanged.

---

## [3.28.2] — 2026-08-07

Every skill in `ceh-git-workflow` asserts "CI must be green" as a pre-merge gate item. Exactly one
place named a command for reading it — the `branch-merger` agent — and that command was
`gh pr checks`, which returns HTTP 403 on a fine-grained PAT lacking `checks=read`. The failure mode
is not that a check is unavailable; it is that the agent cannot tell a **permissions error from a red
build**, and the gate's own wording ("never merge red") pushes it to treat the 403 as red and stop.
A green build reads as failed CI.

The second half of the problem is what the silence invites. Skills that say "CI green" without
naming a command leave the agent to improvise, and the most natural improvisation is
`gh api repos/{owner}/{repo}/commits/<sha>/status` — which returns HTTP 200 and therefore looks
correct. It is the legacy Commit Statuses API; Actions writes check runs and never touches it, so it
returns `{"state":"pending","total_count":0}` indefinitely. A gate built on that call fails in the
opposite and worse direction: it never sees red at all.

The fix is a canonical **Reading CI status** block in `ceh-git-workflow:merge`, the skill that owns
the pre-merge gate, specifying commit-anchored `gh run list -c "$(git rev-parse HEAD)"` and naming
both traps outright — including that a 403 is a permissions error and must not be reported as a red
gate or merged around. Commit-anchored matters: `gh run list --branch <name>` resolves to whichever
run the branch tip last produced and will happily report a stale commit's result after a force-push.

Two limits are stated in the block rather than left to be discovered. `gh run` sees only GitHub
Actions runs in the current repo, so on a repo with Codecov, Sonar, or any GitHub App posting checks
it is not the full gate — that is the point at which granting `checks=read` becomes the right call
rather than a workaround. And `gh pr view --json mergeStateStatus`, which does work without the
`checks` permission, cannot distinguish a pending non-required check from a failing one: it gates,
it does not diagnose.

Deliberately not duplicated into `open-pr`, `release`, `hotfix`, or `release-flow`. Those say
"CI green" without naming a command and inherit the fix through the merge skill; five copies of a
command set is precisely the drift the cross-reference policy exists to bound.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.2.7 |

### Fixed

- **`ceh-git-workflow` / `branch-merger`** — no longer instructs the agent to read the pre-merge gate
  with `gh pr view`/`gh pr checks`. Now names `gh pr view --json state,mergeable,mergeStateStatus,reviewDecision`
  plus `gh run list -c`, and states that a 403 from `gh pr checks` is a permissions error rather than
  a red gate.

### Added

- **`ceh-git-workflow` / `merge`** — a "Reading CI status" subsection under the Pre-Merge Gate:
  commit-anchored `gh run list -c`, the blocking `gh run watch --exit-status` form that chains into a
  merge command, `gh run view --log-failed` for diagnosis, and the three traps (403-is-not-red, the
  legacy Commit Statuses API, and `gh run`'s blindness to non-Actions checks).
- `CROSS_REFERENCES.md` — an entry registering the two-file duplication between the `merge` skill's
  canonical block and `branch-merger`'s one-line echo.

---

## [3.28.1] — 2026-08-07

`validate` fired on exactly two events: a push to `main` and a pull request. Both are automatic, and
neither has a manual counterpart — so when a PR's check failed to fire at all, there was no run to
re-run and no button to press. The repo's only CI gate was unreachable by hand.

The distinction that makes this a real gap rather than a duplicate of the Actions UI: `gh run rerun`
needs a run to exist. It is the right tool for a run that fired and failed spuriously, and it
re-executes in the original PR context. It has nothing to offer when the trigger itself never
matched — a skipped event, a workflow edit that landed after the push, a PR opened while Actions was
degraded. `workflow_dispatch` is the native trigger for that case, and it is one line.

Two limits are worth stating rather than discovering. GitHub only exposes the Run workflow button —
and only accepts `gh workflow run` — once a workflow carrying `workflow_dispatch` exists on the
**default branch**, so this does nothing for the PR that introduces it and takes effect from the
merge onward. And a dispatch runs against a branch ref, not the PR's merge ref, so it validates the
branch as it stands rather than the merge result. For this repo's validator, which reads manifests
and skill files off the checkout, that difference is immaterial.

No plugin changed. The workflow is repo infrastructure and ships in neither the marketplace nor any
plugin.

### Plugin versions

None. This release touches repo-level CI configuration only.

### Added

- `.github/workflows/validate.yml` — a `workflow_dispatch` trigger, so `validate` can be started by
  hand from the Actions tab or with `gh workflow run validate.yml --ref <branch>`.

---

## [3.28.0] — 2026-08-06

Every plugin here asks whether the thing is correct. None asked whether anyone outside the team
could use it. `ceh-usability-audit` takes that question, and its whole design follows from one
admission: **you cannot run this audit on yourself.** You already know the answers, and every gap a
newcomer would fall into gets silently bridged by what you know. So the method is not a checklist —
it is a way of constraining who does the looking. Cold subagents get exactly what a newcomer
actually receives (a frozen artifact set: README, landing page, `--help` — never the source, never
this conversation), hold one persona constraint the whole way, and stop at the first thing they
cannot get past.

The framing is a five-year-old and a ninety-five-year-old, which is a pair of constraints rather
than sentiment. The five-year-old has no vocabulary and no prior model of what this is; the
ninety-five-year-old will not act without knowing the consequence and needs to see what happened
after every step. Nearly everything that makes software unusable fails one of those two.

Severity is the load-bearing rule and the one most likely to be wrong: it is assignable **only from
an observed stall**. Something the auditor merely noticed — a real anti-pattern, an obviously bad
label — is demoted to an unranked `Hypotheses` list and cannot affect the gate. That under-reports,
and the README says so plainly under a `Known weak points` heading that also names the second
weakness: subagents lose the Chrome tools, so live web-UI walks fall back to the main session and
forfeit the cold-context guarantee that makes the method work. Both are documented as attack
surfaces for whoever evaluates this next, because the alternative — a report ranked by whatever the
auditor happened to care about — is the failure mode of every usability checklist ever written.

Scenario traces over the four skills then found three defects that would have broken real runs, and
one gap the design never covered.

`Blank Slate` was unfalsifiable. Specified as "no domain vocabulary and no prior product knowledge —
any word you would have to already know is a stall the moment you meet it", read literally by a
walker it stalls on "clone", "terminal", and "browser tab" at line one of any README ever written.
It therefore returned a Blocker on 100% of targets and gate criterion 1 was unreachable. The fix is
an **audience baseline** declared before dispatch — one line naming what the intended audience
already knows, inside which everything is free and outside which everything about *this* product
still is not. `plain-language-pass` already carried the idea as a stop condition ("establish who the
reader is"); the walkthrough skills did not.

Turn exhaustion was manufacturing Blockers. The walk report only had `Reached goal: yes | no`, so a
walker that hit `maxTurns` reported `no`, which the severity table reads as "could not complete the
goal" — a finding invented out of the instrument's own ceiling. There are three ways a walk ends and
the report now names which.

And five walkers were dispatched in parallel while permitted to run any non-global install, which
puts five concurrent `uv sync` runs in one shared checkout. Parallelism now keys on whether the walk
writes.

The gap was length. Nothing bounded a walk, so a README taking forty steps passed as clean because
nobody stalled outright — and length is the most common usability failure after an outright blocker.
The bound is in **actions, not minutes**: walker wall-clock measures model throughput rather than
the product, so that ban stands. The goal splits into milestones, each budgeted before dispatch
(declared up front it is a prediction; declared afterwards it is a rationalization), and overrun
feeds the existing severities instead of adding an axis. Where no number is defensible the budget is
the step count the documentation itself prescribes — which turns "the doc omits steps reality
requires" from a complaint into a measurement. Minutes are still reported, but only as a translation
through a fixed published cost model and labelled `(model, not measured)`. Machine wait — the real
seconds spent watching an install — is carved out as the one genuine clock and measured.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-usability-audit` | v1.0.1 (new) |

### Added

- **`ceh-usability-audit`** — new use-case-workflow plugin for the comprehension layer, with four
  skills and one agent:
  - `first-run-walkthrough` — can a stranger get from "just arrived" to first real success. Freezes
    the artifact set, declares an audience baseline and per-milestone action budgets, dispatches one
    cold walker per persona, ranks stalls by observed outcome, loops to a 5-point gate.
  - `audit-interface` — they are already in: the five questions every surface must answer unasked, a
    twelve-item reject-on-sight anti-pattern sweep, the naming test, and the persona battery, branched
    by surface (web UI, CLI, library API, app screen).
  - `audit-error-messages` — the three-part rule (what happened, what specifically was wrong with the
    offending value quoted, what to do next) over every user-reachable string, plus nine rules the
    three parts do not cover, placement, and a rewrite table.
  - `plain-language-pass` — a vocabulary floor, swap table, seven sentence rules, define-on-first-use,
    and an explicit **never simplify** list covering legal wording, destructive consequences, auth
    failure detail, and exact identifiers.
  - `novice-walker` agent — walks a target cold under one persona toward one goal and reports where it
    stalled. Read-only. Runs on Sonnet deliberately: a weaker reader is a more honest novice proxy.
- Milestones with a declared **action budget** in `first-run-walkthrough`, plus a fixed cost model
  translating actions into an estimated newcomer time-to-first-success, and real measurement of
  machine wait.
- An **audience baseline** as a required dispatch input, recorded verbatim in every report — two
  audits of one target under different baselines are not comparable.
- `ERROR_MESSAGES.md` in the shared run folder, so `audit-error-messages` writes its triage table
  down like its three siblings instead of leaving it in a chat log.

### Changed

- `Blank Slate` is now scoped by the audience baseline in all four places the persona table is
  duplicated, registered in `CROSS_REFERENCES.md`.
- Gate criterion 5 of `first-run-walkthrough` replaced. It compared actions-to-success across
  personas, which differ by construction — `Wrong Turn` takes a wrong turn first — so the spread
  always had an instrument explanation. It now checks conformance to the declared budget.
- `novice-walker` `maxTurns` 25 → 35, and the walk report gained a stop-reason field, a per-milestone
  table, and a machine-wait column.

### Fixed

- Turn exhaustion is no longer scored as a Blocker. Re-dispatch advice is a narrower goal rather than
  a higher `maxTurns`, since a caller cannot override agent frontmatter per dispatch.
- Parallel walkers no longer share one mutable checkout: a walk that writes to the working tree runs
  one persona at a time, or gives each its own copy.
- `audit-interface` restates the browser limitation at the point of dispatch, not only in a table cell
  three sections earlier.

---

## [3.27.1] — 2026-07-31

`CLAUDE.md` and the repo-local `add-plugin-component` skill had been carrying the same checklist
since the skill was written: pick the plugin, write the frontmatter, update both README tables,
register the duplication, bump both manifests, run the validator. Two copies of one checklist is
exactly the drift this repo's own duplication policy accepts only when the copies genuinely
differ — and these did not. `CLAUDE.md` simply held the older, less complete version.

The 67 lines of `## Adding a Component` / `## Adding an Agent` / `## Adding a Skill` collapse to a
13-line pointer. What stays behind is the half a silent skill-load failure would actually cost: the
four registration chores that fail CI — a row in the root README, a row in the plugin README, a
bump in both `plugin.json` and `marketplace.json`, and a green `validate.py`. The agent gotchas are
deliberately not in the stub, because a green validator never caught them anyway.

Four facts lived only in `CLAUDE.md` and were ported into the skill before the deletion: that
`isolation: worktree` is deliberately unused here (subagent worktrees branch from the default
branch rather than the parent session's `HEAD` unless `worktree.baseRef: "head"` is set, which
under this repo's feature-branch rule hands an agent a copy of `main` without your work); that
`SessionStart` hooks never fire for subagents, making `skills:` preload the only route a
hook-loaded standard has into one; that `AskUserQuestion` is stripped from *every* subagent rather
than only background ones; and that `model` defaults to `inherit`.

No plugin changed, so no plugin version moved. `CLAUDE.md` and `.claude/skills/` are repo-level
contributor documentation — they ship in neither the marketplace nor any plugin.

### Plugin versions

None. This release touches repo-level documentation only.

### Changed

- `CLAUDE.md` — the three `## Adding …` sections replaced by one `## Adding a Component` section
  that points at `.claude/skills/add-plugin-component/` and lists the four CI-failing registration
  chores. The file drops from 277 to 226 lines.
- `.claude/skills/add-plugin-component/SKILL.md` — absorbed the `isolation: worktree` policy, the
  `SessionStart`-hooks rationale behind `skills:` preload, the every-subagent scope of the
  `AskUserQuestion` strip, and the `model: inherit` default.

### Removed

- The `acceptEdits` note on avoiding edit prompts (the skill already directs permission grants
  through `permissions.allow` in `settings.json`) and the link to the subagents docs — both dropped
  rather than ported, as session mechanics rather than component-authoring rules.

---

## [3.27.0] — 2026-07-31

Testing was split across three stack plugins that each owned a runner, and nothing owned the
question those runners cannot answer: *which* inputs, and whether a green suite would catch
anything. `ceh-testing` takes that half. The split test is whether the content would be
byte-identical across stacks — equivalence partitions, boundary analysis, mutation testing, and
characterization tests are; `asyncio_mode` and MSW handlers are not. Duplicating the technique into
`ceh-python-service`, `ceh-python-library`, and `ceh-web-frontend` would have produced three copies
with nothing stack-specific to justify their divergence, so it sits in the cross-cutting tier
alongside `ceh-git-workflow`: a Python service has commits and it has test design, and the stack
plugin owns neither.

Its five skills fire on moments rather than topics — a bug is being fixed, inputs are being chosen,
a suite is being distrusted, a refactor is about to start, a feature is about to be called done. Two
of them were reshaped by evaluation runs before release: `close-test-risk-gaps` had triggers that
only fired on vocabulary the user would have to already know (so it now also fires on the unnamed
situations — a shared counter decrements, a retry could double-charge), and `design-test-cases` was
reframed around over-testing, since the failure mode in practice is a suite padded past the point
where any test adds information, not one that is too small.

The plugin then had to actually reach the work. Delegated test writing was losing the technique
layer entirely: `SessionStart` hooks do not fire for subagents, so a stack skill named in `skills:`
was the only standard reaching the six tester agents — they knew pytest and MSW but not boundaries,
decision tables, or the assertion rules. All six now preload `design-test-cases`, as a soft
dependency that resolves to nothing silently when `ceh-testing` is not installed. In the same vein,
`shrink-diff` and `refactor-repo` now point at `verify-behavior-preserved` for anything past a
mechanical transform; the pointer previously ran one way only, and a green existing suite proves
only what it already covered.

`TESTING_WORKFLOW.md` documents what no single plugin can: the routing between them — which of the
three load mechanisms fires when, what a given request triggers end to end, and where two skills
share a trigger and in which order they must run.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-testing` | v1.0.2 (new) |
| `ceh-agent-coding-contract` | v2.8.7 |
| `ceh-python-service` | v3.1.7 |
| `ceh-web-frontend` | v3.2.5 |

### Added

- **`ceh-testing`** — new cross-cutting plugin for stack-agnostic testing technique, with five
  skills and one agent:
  - `test-a-bug-fix` — reproduce-first: the smallest failing test before any source edit, read the
    failure to confirm it fails for the real reason, then revert the fix and prove the test goes red
    again; the reproducer doubles as the `git bisect run` predicate.
  - `design-test-cases` — a nine-rung input-selection ladder (partitions, boundaries, decision
    tables, state transitions including illegal ones, pairwise, properties, metamorphic relations,
    fuzzing, forced dependency failure) with an explicit stopping criterion instead of a coverage
    percentage.
  - `audit-test-suite` — six checks cheapest-first: assertion audit, delete-the-code, mutation
    testing scoped to the diff, flakiness and order dependence, level and speed, branch coverage
    last and never as a headline.
  - `verify-behavior-preserved` — baseline before the edit: characterization tests, golden files,
    and a differential run of old versus new over the same inputs.
  - `close-test-risk-gaps` — a pre-completion triage gate over five classes a functional suite
    structurally misses (concurrency/idempotency, contract drift, performance, authorization,
    migration and rolling deploy); unfired classes are skipped explicitly and the skips reported.
  - `test-suite-auditor` agent — runs the slow, high-output half of the audit out of session,
    read-only, scoped to the diff, and hands back a ranked report.
- **`TESTING_WORKFLOW.md`** — repo guide to the routing between `ceh-testing`, the three stack
  testing skills, and the tester agents: load mechanisms, a trigger table, six scenario
  walkthroughs, the coverage stance, and the known overlaps. Linked from `README.md` and
  `ceh-testing/README.md`.

### Changed

- **`ceh-python-service` / `ceh-web-frontend`** — all six tester agents (`python-unit`,
  `python-integration`, `python-system`, `ts-unit`, `ts-integration`, `ts-system`) preload
  `ceh-testing:design-test-cases` alongside their stack testing skill.
- **`ceh-agent-coding-contract`** — the shared `Behavior preservation` block in `shrink-diff` and
  `refactor-repo` now requires pinning current behavior with `ceh-testing:verify-behavior-preserved`
  before anything past a mechanical transform; `CROSS_REFERENCES.md` updated to match.

### Fixed

- **`ceh-testing` / `close-test-risk-gaps`** — triggers no longer require the user to already know
  the vocabulary; the gate also fires on the unnamed situations (shared stock decrements, a retry
  that could double-charge, a caller-supplied ID that could return someone else's data).
- **`ceh-testing` / `design-test-cases`** — reframed around over-testing, with duplication treated
  as a defect rather than a safety margin.

## [3.26.0] — 2026-07-25

Orienting in an unfamiliar repo had one tool here — the `repo-tree-mapper` agent — and it answers
"what is in this repo", one line per path. It does not answer "what is actually happening in it".
`explain-codebase` fills that: a component-level walk that says what each part is responsible for,
what it connects to, and what will bite you before you change it, plus the end-to-end flows that
turn a list of parts into an explanation.

Two choices shape it. It explains at **component/module level by default** and drops to per-file
entries only when explicitly asked — on a large repo the per-file view multiplies the reading and
orients worse, so it is opt-in rather than the default nobody wanted. And its output is a
**regenerable local artifact**, written to `.agents_workspace/CODEBASE_EXPLAINED.md` and kept
untracked via `.git/info/exclude` rather than a tracked `.gitignore`, so no teammate inherits the
rule and no repo file changes. What replaces per-file coverage is an accounting requirement: every
file lands in an explained component, an explicit group rule, or a named exclusion — anything
unassigned is reported as a gap rather than dropped quietly.

It is the first skill in `ceh-dev-tools`, which drops the "agents only" qualifier it carried in
`README.md` and `CLAUDE.md`. Since it shares onboarding-shaped triggers with `repo-tree-mapper`,
both its description and body disambiguate explicitly against the mapper, against
`ceh-architecture:document-architecture` (diagrams and decisions), and against
`ceh-documentation:user-operator-guide` (docs for people who use the product).

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-dev-tools` | v1.2.0 |

### Added

- **`ceh-dev-tools` / `explain-codebase`** — fires on "go through the repo and explain what is
  happening", "explain this codebase", "document what each module does", or before the first
  change to an inherited repo. Writes `.agents_workspace/CODEBASE_EXPLAINED.md`: what the repo is,
  a Mermaid overview, a section per component using a fixed four-part shape (what it is / what's
  inside / how it connects / before you change it), 1–3 key flows, gaps, and an accounting table.
  Component-level by default; per-file only on an explicit ask. Adds itself to
  `.git/info/exclude`, and untracks the file first if an earlier run committed it.

### Changed

- **`ceh-dev-tools`** — no longer agents-only; plugin description, both README tables, and the
  `CLAUDE.md` plugin table updated to cover the skill alongside `repo-tree-mapper`.
- **`.gitignore`** — Claude-related ignore rules moved out of the repo file into the global
  gitignore.

## [3.25.2] — 2026-07-25

An audit of all 21 plugins against the live Claude Code docs found the plugins were not *broken*
by the Claude 5 model family — no stale model IDs, no dead tool names — but several were written
before frontmatter fields existed that the runtime now provides natively, so behaviour was being
asked for in prose instead of declared.

Dropped `permissionMode: acceptEdits` from the 7 agents that carried it — Claude Code ignores
`permissionMode`, `hooks`, and `mcpServers` on plugin subagents, so it never took effect; the
files are now honest about what actually applies. Added, scoped per field after checking each
skill individually: `paths:` on 6 file-type-triggered skills (not applied broadly, since `paths`
*narrows* auto-loading and would drop non-file triggers like "a uv command is run"); `effort:`
only where it differs from the `high` default; `disallowed-tools: Edit Write` on `code-review`
only, since sibling review skills genuinely write files; `context: fork` + `background: false` on
`summarize-chat` and `lessons-learned`, which act on the conversation itself; `argument-hint` on
12 manual-only skills; and `memory: local` on `ceh-advisor` so it stops re-deriving the same
verdicts across sessions. Fixed a real path bug in `update-changelog`, which told the model to run
a literal placeholder path by hand — now `${CLAUDE_SKILL_DIR}`, which Claude Code substitutes.

Separately, all 83 skill and agent `description` fields — previously split across five competing
YAML styles, two of which had already produced invalid YAML in this repo — were standardized on
the folded block scalar (`>-`), the only style with no escaping burden. `validate.py` now enforces
both fixes: it rejects any `description` not in `>-` form, and it resolves `${CLAUDE_SKILL_DIR}`
so path-bug regressions are caught at validation time rather than at runtime.

### Plugin versions

20 plugins bumped PATCH (content-only frontmatter and description changes; no skills or agents
added or removed).

| Plugin | Version |
|--------|---------|
| `ceh-advisor` | v1.0.4 |
| `ceh-agent-coding-contract` | v2.8.6 |
| `ceh-architecture` | v3.1.3 |
| `ceh-blog` | v1.0.9 |
| `ceh-business-plan` | v1.0.2 |
| `ceh-dev-tools` | v1.1.4 |
| `ceh-documentation` | v1.1.4 |
| `ceh-evaluation` | v1.1.5 |
| `ceh-fabled` | v1.3.3 |
| `ceh-git-workflow` | v3.2.6 |
| `ceh-lessons-learned` | v2.0.7 |
| `ceh-ops` | v3.0.5 |
| `ceh-orchestration` | v1.0.5 |
| `ceh-plan-build-review` | v1.1.2 |
| `ceh-python-library` | v1.2.3 |
| `ceh-python-service` | v3.1.6 |
| `ceh-release-flow` | v1.1.8 |
| `ceh-scaffolding` | v1.0.3 |
| `ceh-seo` | v1.0.1 |
| `ceh-summarize-chat` | v2.0.6 |
| `ceh-web-frontend` | v3.2.4 |

### Changed

- **All plugins** — modernized agent/skill frontmatter to use native Claude Code fields
  (`paths`, `effort`, `disallowed-tools`, `context: fork`, `argument-hint`, `memory: local`)
  instead of prose instructions; dropped the inert `permissionMode: acceptEdits` from 7 agents.
- **`ceh-documentation` / `update-changelog`** — replaced a literal placeholder script path with
  `${CLAUDE_SKILL_DIR}`, which Claude Code substitutes at runtime.
- **All skill and agent `description` fields (83 total)** — standardized on the `>-` folded block
  scalar, the only YAML style with no escaping burden for `:`, `"`, `'`, `\`, and `#`.
- **`tools/validate-plugins/validate.py`** — now enforces `description: >-` on every skill/agent
  and resolves `${CLAUDE_SKILL_DIR}` references during path validation.

### Fixed

- **21 skill/agent files** — unquoted `description:` values containing `: ` were invalid YAML
  under a strict parser (Claude Code's own parser is lenient, so nothing broke at runtime, but the
  files were non-conformant); now quoted or converted to the `>-` block form.

## [3.25.1] — 2026-07-24

The usage-limit guard fired the handoff on the first tool call *after* a 5-hour window reset — the
one moment the quota is most available. The hook read `used_percentage` off the newest statusline
record and checked only its age, so a record written minutes before a reset stayed inside the
15-minute freshness window while describing a window that no longer exists. The reading said ~90%,
the account was actually at 0%, and the session stopped starting new work until an API round-trip
happened to refresh the export.

The age check alone cannot catch this: the record is genuinely recent, it is the *window* that is
gone. `worst_window` now drops any window whose `resets_at` is already in the past, since such a
reading predates the restart by construction. A window carrying no `resets_at`, or an unparseable
one, is still considered — the guard is advisory and fails open, so an unreadable timestamp must
not silently disable it.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.8.4 |

### Fixed

- **`ceh-agent-coding-contract` / `usage-limit-watch.py`** — windows past their `resets_at` are
  excluded from the worst-window scan. Previously the first tool call after a quota reset could
  trigger `usage-limit-handoff` off a pre-reset reading that was recent enough to pass the
  `CEH_USAGE_STALE_MINUTES` check.

## [3.25.0] — 2026-07-24

The plan-build-review loop had no home for a change made *after* a version shipped. A one-line
copy fix or a tightened validation either drifted silently from the frozen `SKELETON`/`ITER` plan
or got over-ceremonied into a full iteration — and "everything post-MVP" sat ambiguous between the
two. `patch-built-version` closes that, and it draws the line at §02: a change touching the data
model or API surface (or adding an entity, route, or screen) is a feature and routes back to
`plan-fullstack-app-iteratively`; anything smaller is recorded as an `ITER_NN.md` carrying
`patch: true` and implemented in scope. The patch marker is the only artifact allowed past the MVP
terminator, and the SemVer PATCH bump is handed to `ceh-git-workflow:release` rather than
duplicated here.

The schema change rippled to three lockstep consumer copies (`implement-from-plan`,
`review-against-plan`, and the new skill's own); `implement-from-plan` learned to exclude patch
ITERs from a default full-sequence run; the duplication is registered in `CROSS_REFERENCES.md`.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-plan-build-review` | v1.1.0 |

### Added

- **`ceh-plan-build-review` / `patch-built-version`** — fires when patching an already-built
  version with a small, non-feature change (bug fix, copy/config tweak, validation change, small
  post-MVP polish). Routing gate: a §02 change (data model / API surface) or a new
  entity/route/screen is a feature and routes to `plan-fullstack-app-iteratively`; anything smaller
  becomes a `patch: true` `ITER_NN.md` implemented in scope, with the PATCH bump handed to
  `ceh-git-workflow:release`.

### Changed

- **Plan document schema** — added the `patch` frontmatter marker; a patch `ITER_NN.md` is the
  only artifact allowed past the `mvp: true` terminator. Propagated to all three lockstep
  `plan-schema.md` consumer copies and registered in `CROSS_REFERENCES.md`.
- **`ceh-plan-build-review` / `implement-from-plan`** — patch ITERs are excluded from the default
  full-sequence run and implemented only when named explicitly.

## [3.24.0] — 2026-07-22

SEO/GEO had no home in the plugin catalog: the technical half (meta tags, structured data,
sitemaps) would have landed in `ceh-web-frontend`, the content half (README pitches, package
descriptions) in `ceh-blog` — while a SaaS marketing site or a published library touches both
with neither plugin loaded. `ceh-seo` closes that as a use-case-workflow plugin for anything
exposed to the internet: public web pages, repo READMEs, package listings, landing copy. Its two
skills split on surface mechanics, where trigger moments and file types are disjoint — the same
rule that keeps `sveltekit` and `react-vite` in one plugin.

The plugin shipped through a behavioral evaluation (`ceh-evaluation:evaluate-skill`, run-001,
gate 4/6 user-accepted with triggering waived): against hermetic no-skill baselines, with-skill
runs cleared every discriminating assertion — verbatim one-liner consistency across
README/pyproject/GitHub 2/2 vs 0/2, title/description length discipline 2/2 vs 0/2 — locating
the plugin's measured value in its limits and prohibitions rather than checklist items models
already know. One eval finding fed straight back into content: the og:image asset-integrity rule
(real 1200×630 PNG/JPG, no SVG, no dangling references).

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-seo` | v1.0.0 |

### Added

- **`ceh-seo` (new plugin)** — SEO/GEO discoverability standards for anything internet-exposed.
- **`ceh-seo` / `web-discoverability`** — fires when shipping a public web page/route: per-page
  head checklist (title/description/canonical/OG with asset-integrity rule), site-level surfaces
  (sitemap, robots, `llms.txt`, real-404 rule), JSON-LD by page type, SSR/prerender requirement,
  GEO citation rules (answer-first sections, extractable facts).
- **`ceh-seo` / `text-discoverability`** — fires when writing public repo/package text: the
  excerpt rule (category noun + audience + differentiator in ~160 chars), the verbatim one-liner
  across surfaces, per-surface checklist (GitHub/PyPI/npm/marketplaces), facts-over-adjectives.
  Boundary drawn against `ceh-documentation:update-readme`: findability vs post-change accuracy.

## [3.23.1] — 2026-07-21

The coding contract could not reach a single subagent. `SessionStart` hooks do not fire for
subagents, and no agent in the repo granted the `Skill` tool — so the two paths that would carry
the contract into a delegated task were both closed, and the contract's own **Multi-Agent
Scenarios** section (treat the caller's instructions as user-level authorization, do not escalate
scope, report stop conditions to the caller since `AskUserQuestion` is unavailable) had no reader.
The fix is the `skills:` frontmatter field, which preloads a skill at dispatch and needs no `Skill`
tool — already in use by the `ceh-git-workflow` agents, just never pointed at the contract.

It is deliberately not preloaded everywhere. The six tester agents are excluded because the
contract's "do not add tests unprompted" rule contradicts an agent whose whole charter is writing
tests; the four `ceh-git-workflow` agents already carry their own procedure; `verifier`,
`repo-tree-mapper` and `ceh-advisor` are read-only or run on haiku. `fabled-voice` is excluded from
every agent — subagent output is consumed by the main agent, never the user, so a response-style
skill there is pure cost.

Auditing the `skills:` field also turned up six entries written as bare skill names while four
others were fully qualified. Both forms point at a skill in the agent's own plugin, so whether the
bare ones ever resolved depends on a same-plugin fallback in the loader that is not documented. The
failure mode is silent — an agent that believes it preloaded its testing standard and did not — so
all entries are now qualified rather than diagnosed, the qualified form being correct either way.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.8.3 |
| `ceh-fabled` | v1.3.1 |
| `ceh-ops` | v3.0.3 |
| `ceh-orchestration` | v1.0.3 |
| `ceh-python-service` | v3.1.4 |
| `ceh-web-frontend` | v3.2.2 |

### Changed

- **`ceh-orchestration` / `executor`, `ceh-ops` / `github-actions`, `gitlab-ci`** — preload
  `ceh-agent-coding-contract:agent-coding-contract` via `skills:`. These three write files with
  broad latitude and no scope discipline of their own; they are also the only agents where a
  cross-plugin preload is justified, the contract being a cross-cutting tier rather than a peer
  use-case plugin.
- **`ceh-python-service` / three tester agents, `ceh-web-frontend` / three tester agents** —
  `skills:` entries qualified: `python-service-testing` →
  `ceh-python-service:python-service-testing`, `frontend-testing` →
  `ceh-web-frontend:frontend-testing`. All 13 `skills:` entries in the repo are now uniformly
  `plugin:skill`.
- **`ceh-agent-coding-contract` / `agent-coding-contract`, `ceh-fabled` / `fabled-voice`** —
  descriptions trimmed (55 → 38 and 85 → 48 words) now that both delivery paths are deterministic
  and the description no longer carries triggering weight. Both now state they load automatically,
  so the main agent does not re-invoke a skill already in context. The manual trigger phrases stay
  as the recovery path for when a hook does not fire.
- **`CLAUDE.md`** — the plugin-agent frontmatter note gains the `skills:` preload rule: no `Skill`
  tool required, `SessionStart` never fires for subagents, always write `plugin:skill`.
- **`README.md`** — records the contract as preloaded into the three implementation subagents.

### Fixed

- **`ceh-orchestration/.claude-plugin/plugin.json`** — normalized from CRLF to LF, the only manifest
  in the repo still using CRLF. Surfaced when a bulk `sed -i` rewrote the whole file; the content
  diff is one version string.

---

## [3.23.0] — 2026-07-20

`fabled-voice` becomes always-on. A SessionStart hook now loads it at the start of every session,
the same mechanism `ceh-agent-coding-contract` uses to load the contract — so the response style
applies without the user asking for it, rather than waiting on a description match.

The mechanism has one non-obvious constraint worth recording. A hook cannot invoke a skill; it can
only inject text, and the model still makes the `Skill` call. Setting
`disable-model-invocation: true` on a hook-loaded skill therefore breaks it — the flag removes the
skill from the model-visible listing, so the hook fires, the directive lands, and the call fails.
`fabled-voice` stays model-invocable for that reason. Cross-plugin hook ordering is likewise not
guaranteed, so the payload resolves precedence in prose instead of relying on sequencing.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-fabled` | v1.3.0 |

### Added

- **`ceh-fabled` / hooks** — a `SessionStart` hook (`startup|resume|clear|compact`) injecting a
  directive to invoke `fabled-voice` before responding. Pure bash, so the plugin gains no `python3`
  dependency. The payload is worded `REQUIRED SETUP ACTION` rather than `MANDATORY FIRST ACTION`
  and defers explicitly to the `ceh-agent-coding-contract` directive when both are pending, so the
  two SessionStart hooks do not contend for the first tool call.

### Changed

- **`ceh-fabled` / `fabled-voice`** — description tightened: the style specifics stay, the
  trigger-phrase list drops to three phrases now that the hook carries the loading. The frontmatter
  does not mention the hook; the READMEs document it.
- **`README.md`, `ceh-fabled/README.md`, `CLAUDE.md`** — record the skill as always-on, add a hooks
  table to the plugin README, and note that this hook needs only `bash` while the `ceh-advisor` and
  `ceh-agent-coding-contract` hooks need `python3`.

### Removed

- **`docs/`** — deleted. It held a stray `DECISION_LOG.md` written to the contract's default
  convention path instead of `.agents_workspace/`, plus a `.gitkeep`. The entry was merged into
  `.agents_workspace/DECISION_LOG.md` as Entry 49 with its original timestamp intact.

---

## [3.22.1] — 2026-07-20

Release commits produced by the release flows were arriving as a bare `chore: release vX.Y.Z`
subject with no body and no attribution footer. The cause was not a single bad instruction but
three specifications that each independently permitted it: the flows' step-7 gate defined the
message *as* the subject line, the subagent delegation note said to pass "only what the diff cannot
show" and then listed only the version number, and `commit-author` treats a caller-supplied subject
as authoritative over its own inference. The attribution footer disappeared as a side effect —
a subject-only message goes out through `git commit -m`, and the footer is only ever assembled on
the multi-line `-F` path.

A release commit is the worst case for inferring intent from a diff: it shows version strings and
changelog prose, but not what shipped or why the bump is that level. In the direct (PR-less) flow
it is the only durable narrative of the release at all. All four specifications now say so.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.2.4 |
| `ceh-release-flow` | v1.1.6 |

### Fixed

- **`ceh-release-flow` / `release-flow`, `direct-release-flow`** — the step-7 gate now requires a
  body and an attribution footer, not just the subject. A new "Step 7 detail" section states that
  `chore: release vX.Y.Z` is the subject rather than the whole message and gives the template:
  one to three sentences on what shipped in the changelog's terms, then `Bump:` with the change
  that forces the level, `Manifests:` with what moved, `Docs:` with what was updated or why it was
  not, then the configured attribution footer — written to a temp file and committed with `-F`.
  The subagent delegation notes now name that body content as something the caller must pass,
  since an agent handed only the subject commits exactly that and cannot recover the rationale
  from a diff of version strings.
- **`ceh-git-workflow` / `release`** — the step-1 version-bump commit template gained body lines
  and now reads "always multi-line" rather than "a footer means a multi-line message".
- **`ceh-git-workflow` / `commit-author`** — a caller-supplied required subject now explicitly
  constrains the subject line only, and is never permission to skip the body or the attribution
  footer.

### Changed

- **`CROSS_REFERENCES.md`** — registers the near-verbatim "Step 7 detail" block shared by the two
  release flows, and records the two `ceh-git-workflow` files that state the same rule in their own
  words so all four stay consistent in intent.

---

## [3.22.0] — 2026-07-20

`ceh-fabled` gains a **style** skill to sit beside its three reasoning skills. `fabled` raises the
quality of the thinking; `fabled-voice` governs only how the result is written — length, structure,
formatting, register — and explicitly changes neither the conclusions nor the work that produced
them.

The rules are derived from paired transcripts rather than impression: 247 messages from a stronger
model against 495 from a weaker one, working the same two repositories, compared on measurable
axes. The largest single discriminator is narration of intent — "let me check X" opens 41% of the
weaker model's mid-task lines and 18% of the stronger one's, which states the finding it just got
instead. The rest follow the same pattern: fewer headings (2% of messages vs 10%), lighter bold
(1.8 vs 2.2 emphases per 1000 characters), an explicit "not validated" clause at roughly four times
the rate, and standing offers in place of permission questions ("Want me to…" 4 occurrences vs 20).

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-fabled` | v1.2.0 |

### Added

- **`ceh-fabled` / `fabled-voice`** — new skill: deliver responses in the stronger model's writing
  style, form only. Defines three message shapes and the rules for each. **Progress lines** lead
  with the finding rather than the intention, stay under three sentences, and take a colon
  terminator when a write follows. **Advisory answers** put the verdict in the first clause, name
  the load-bearing reason as such, argue one counterpoint, and close on a calibration stating
  confidence and the most likely way the answer is wrong. **Closing reports** open verdict-first
  with the numbers in the sentence, use bold inline labels instead of markdown headings, carry an
  explicit validated/not-validated ledger naming the command that was not run, and end on a
  standing offer plus any risk flag. Includes a table of the eight recurring report labels and a
  do/don't table of the weaker model's habits with the replacement for each.

A closing section pins the skill to form: it does not license skipping a tool call to keep a
message short, manufacturing numbers to fill the verdict sentence, or converting a Stop Condition
into an offer. The honest sentence names what was not measured.

## [3.21.2] — 2026-07-19

`ceh-git-workflow`'s commit skill hardcoded an attribution footer. Skill bodies load **after** the
harness Git instructions, so that literal won the conflict and silently overrode whatever the user
had configured as `attribution.commit` — a setting that appeared to be ignored was in fact being
overwritten by the standard meant to describe it.

The three skills that emit an attribution footer now defer to the setting instead of restating it.
Worth noting for anyone who customized the value: a custom `attribution.commit` **replaces** the
default `Co-Authored-By: Claude` git trailer rather than adding to it, and free text like
`Generated with …` is not `Key: Value`, so it is a footer line that `git interpret-trailers` will
not parse. Use trailer syntax if the footer needs to stay machine-readable.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.2.3 |

### Fixed

- **`ceh-git-workflow` / `commit`** — the Attribution rule and the worked example no longer carry a
  literal footer string. Both point at `attribution.commit` from Claude Code settings and forbid
  substituting a literal from the skill or from memory.
- **`ceh-git-workflow` / `open-pr`** — the "Attribution included if AI tooling assisted" checklist
  item now names its source (`attribution.pr`), and the filled-in example ends with the same
  placeholder the commit skill uses, so the pattern is consistent across both skills.
- **`ceh-git-workflow` / `release`** — new Attribution section mapping the version-bump commit to
  `attribution.commit` and the GitHub release notes to `attribution.pr`. The annotated tag message
  is explicitly excluded — a markdown link is noise in `git tag -n` output. Step 1 switches from
  inline `-m` to `-F`, since a single `-m` cannot carry a footer and the instruction would
  otherwise have been unfollowable as written.

Omission is the fallback throughout: when the relevant setting is `false`/empty or no attribution
line is supplied, the footer is dropped rather than invented, so a dangling reference fails closed.

## [3.21.1] — 2026-07-19

The usage-limit guard shipped in 3.21.0 stops **preemptively**. It watched only the 5-hour window
and fired at 95%, which is late enough that the summary competes with the work for the last of the
budget. It now takes whichever window is closest to its cap — the weekly window included — and
fires at 90%, so the handoff is written while everything is still in context rather than
reconstructed afterwards.

Two premises behind the original design turned out to be wrong. The statusline export is not a
weak proxy: it is the **only** local surface carrying live account-wide quota (transcripts record
only the after-the-fact `apiErrorStatus: 429`, never a running percentage), and it refreshes on
every API round-trip, so per-tool-call sampling is fresh enough to act on. Polling an API endpoint
instead was rejected — an API key reports the org API rate limits, a different pool from the
Pro/Max subscription, and the OAuth usage endpoint needs credentials read from a hook, is
undocumented, and the probe consumes the quota it measures.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.8.2 |

### Changed

- **`ceh-agent-coding-contract` / `usage-limit-watch.py`** — the hook now iterates the
  `rate_limits` dict and takes the worst window instead of hardcoding `five_hour`, so the **weekly
  limit triggers the handoff too** and any future window needs no code change. Threshold default
  drops **95% → 90%**.
- **Sensor reliability** — reads the newest record across *all* sessions and projects, so a second
  Claude Code window cannot leave a session acting on a stale number; adds a staleness guard
  (`CEH_USAGE_STALE_MINUTES`, default 15), since a stale low reading reads as safety that is not
  there; and **warns once per session when the statusline export is missing** instead of silently
  no-opping while the user assumes they are protected.
- **`ceh-agent-coding-contract` / `usage-limit-handoff`** — the skill now writes a durable artifact
  to `.agents_workspace/handoff/HANDOFF-<YYYYMMDD-HHMM>-<session-id-prefix>.md` plus one line in a
  global `~/.claude/handoff/index.md`, so work is findable days later without remembering which
  repo it was in. Previously it only reported in chat, which does not survive the session.
- **Subagent routing** — `exit 2` reaches the subagent's own loop, and a subagent's final report is
  never shown to the user, so a subagent that trips the guard now stops and reports **upward**
  rather than writing an artifact it only has partial context for. Only the main session writes the
  handoff. The escalation band stays keyed on `session_id`, which subagents share with the parent,
  so the whole session escalates together.

## [3.21.0] — 2026-07-19

`ceh-agent-coding-contract` gains a **usage-limit handoff**: a guard hook watches the 5-hour
rate-limit percentage and, once it crosses the threshold, tells the agent to stop starting new
work and hand off cleanly rather than getting cut off mid-task.

Alongside it, the three hooks that carry logic — the `ceh-advisor` destructive-command guard and
failure watch, and the new usage-limit watch — move from bash + `jq` to **stdlib Python**. `jq` is
not shipped with Git for Windows, and all three degraded to inert without it, which meant the
advisor's destructive-command protection was silently off on any Windows machine that lacked it.
The six static-payload hooks stay bash deliberately: they are pure `cat` heredocs with no logic,
and a shell is more universally present than Python.

**Requires `python3` on `PATH`** for `ceh-advisor` and `ceh-agent-coding-contract`. The advisor
guard fails closed, so without it destructive commands are blocked rather than waved through.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.8.1 |
| `ceh-advisor` | v1.0.2 |

### Added

- **`ceh-agent-coding-contract` / `usage-limit-handoff`** — new skill plus a `PostToolUse` guard
  hook. The hook reads the 5-hour `used_percentage` relayed by a statusline export to
  `~/.claude/statusline/<project-dir>/<session_id>.jsonl` (Claude Code exposes `rate_limits` only
  to the statusline, not to hooks, hence the relay) and fires at `CEH_USAGE_LIMIT_THRESHOLD`
  (default 95%). The skill then stops new work, reports done vs. open, and ends the turn. Ignored
  warnings escalate every 5 further points instead of repeating on every tool call.
- **Prerequisites section** in the root README covering the new `python3` requirement.

### Changed

- **`ceh-advisor`, `ceh-agent-coding-contract` / hooks** — the three logic hooks are now stdlib
  Python (`ceh-advisor-guard.py`, `ceh-advisor-failure-watch.py`, `usage-limit-watch.py`),
  replacing bash + `jq`. This drops `jq`, GNU `stat -c`, GNU `date -d`, and a hardcoded `/tmp` in
  favour of `json`, `os.stat`, `datetime`, and `tempfile.gettempdir()`, giving identical behaviour
  on Linux, macOS, and Windows. Verified at 21/21 allow/deny parity against the shell originals.
  On Windows the port is also ~5x faster per call, since Git Bash's fork emulation made the old
  multi-`jq` pipeline expensive.
- **`ceh-advisor` / guard failure semantics** — the guard fails **closed**. Deny is signalled the
  documented way (JSON on stdout, exit 0) so it always carries a readable reason, and an
  unparseable payload denies rather than allowing. `hooks.json` appends `|| exit 2` because Claude
  Code treats only exit 2 as blocking — without it a missing interpreter (127) or a crash (1)
  would fail *open* exactly when the guard is most broken. The two advisory `PostToolUse` hooks
  fail **open** instead: one line to stderr and exit 1, never blocking a tool call.
- **`ceh-advisor` / README** — documents explicitly that no code ever writes the ack file (the
  model writes its own permission slip — the intended honest-agent assumption, previously
  understated), and that an ack is a blanket pass for the full TTL rather than scoped to the
  command that was reviewed.

### Fixed

- **`ceh-advisor` / `git push -f` bypass** — the guard never matched a bare
  `git push -f origin main`. The old pattern required whitespace before `-f` that the preceding
  `git push\s` had already consumed, so the flag was only caught in non-first position. Force
  pushes that previously sailed through are now gated. Branch names like `hotfix-f` and
  `feature-force` remain allowed (20/20 targeted cases).
- **`ceh-advisor` / subagent deadlock** — a subagent that tripped the guard was told to "invoke
  the ceh-advisor subagent via the Task tool", which no subagent can do (none have `Task` in their
  tools), leaving it stuck with no path forward. The guard now branches on the `agent_id` hook
  field and tells subagents to stop and report to their caller instead. It still denies rather
  than skipping — skipping would turn delegation into a universal bypass — and a fresh ack written
  by the caller before delegating still unlocks it.

---

## [3.20.0] — 2026-07-18

`ceh-agent-coding-contract` gains **retroactive refactoring**: the write-less-code standard,
which fires at write time inside one session, now has a counterpart for code that accreted across
multiple sessions and commits. `shrink-diff` simplifies a finished feature branch's accumulated
diff against `main` before review; `refactor-repo` runs a propose-then-apply refactor campaign
over a whole codebase or named module, and is user-invocation only.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.7.0 |

### Added

- **`ceh-agent-coding-contract` / `shrink-diff`** — new skill: retroactively apply the
  write-less-code standard to everything a feature branch changed (`git diff main...HEAD`,
  merge-base comparison), across however many commits or sessions produced it. Hunts duplication
  the branch introduced against existing code, dead weight the branch created, over-built
  structure, and retroactive-ladder violations; ranks candidates by payoff over risk. Diff-scoped:
  unchanged code may be edited only for three flagged causes (dedupe, inline a single-caller
  helper, delete newly dead code). Behavior-preservation gate: tests before/after where coverage
  exists, mechanical transforms only where it doesn't, `refactor:` commits separate.
- **`ceh-agent-coding-contract` / `refactor-repo`** — new skill, `disable-model-invocation: true`
  (never auto-fires): whole-codebase or per-module refactor campaign in four phases — read-only
  inventory (with per-area test-coverage status), ranked candidate proposal grouped into
  PR-sized clusters, hard stop for explicit cluster approval, then apply on `refactor/` branches
  under the same behavior-preservation gate with skip-and-report for uncovered areas.
- **`CROSS_REFERENCES.md`** — new entry for the two blocks shared word-for-word between the
  skills (retroactive ladder + behavior preservation), cross-linked to the write-less-code
  ladder entry.

## [3.19.2] — 2026-07-15

The `ceh-web-frontend` `ui-design` skill gains a **finishing recipes** layer, extracted from a
real iterative UI-refresh session so first-pass output lands at post-review quality: a UI that
follows every core rule can still read as a primitive draft (default tables, raw symbols, status
as plain text, buttons floating in space), and these recipes close that gap on the first build.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-web-frontend` | v3.2.1 |

### Changed

- **`ceh-web-frontend` / `ui-design`** — new *Finishing recipes* part: command dock for global
  state and its single action, eyebrow-above-panel section headers, humanized tables (words not
  symbols, lifecycle pills, semantic current-row highlight), lifecycle colors + node-and-rail
  steppers, identity monograms, stat blocks, recessed/auto-grow inputs, app-wide themed
  scrollbars, and a one-motion micro-interaction rule. Core rules gain the surface-ladder depth
  rule (`--bg` chrome / `--surface` command surfaces / `--surface-2` clickable cards). Six new
  "finish tell" anti-patterns and a seventh *finish audit* review-pass item. SKILL.md restructured
  into four parts (design pass / core rules / finishing recipes / quality gates) with a 4-step
  workflow intro; `references/examples.md` gains worked token-compliant markup per recipe;
  description gains polish/primitive trigger phrases.

## [3.19.1] — 2026-07-12

Sixteen task/workflow skills across eight plugins are now **user-invocation only**: each gets
`disable-model-invocation: true` so the model no longer auto-triggers it, and its description is
trimmed of triggering scaffolding (the `Trigger when the user says "…"` phrase lists, `Auto-load`/
`Load when` clauses, keyword stuffing) while keeping the one-line capability statement and the
`Not for X, use Y` disambiguation pointers. These are explicit tasks a user directs — plan an app,
implement/review a plan, write a business plan or blog post, evaluate a skill, summarize the chat,
extract lessons, orchestrate, or run a release flow — not reference standards that should fire on a
code moment.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-blog` | v1.0.8 |
| `ceh-business-plan` | v1.0.1 |
| `ceh-evaluation` | v1.1.4 |
| `ceh-summarize-chat` | v2.0.4 |
| `ceh-lessons-learned` | v2.0.5 |
| `ceh-orchestration` | v1.0.2 |
| `ceh-release-flow` | v1.1.5 |
| `ceh-plan-build-review` | v1.0.6 |

### Changed

- **`ceh-blog`** — `blog-interviewer`, `blog-writer`, `blog-editor`, `blog-repurpose` set to
  user-invocation only (descriptions were already trigger-phrase-free; flag added).
- **`ceh-business-plan` / `develop-business-plan`**, **`ceh-evaluation` / `evaluate-skill`,
  `evaluate-skill-lite`**, **`ceh-summarize-chat` / `summarize-chat`**, **`ceh-orchestration` /
  `orchestrate`**, **`ceh-release-flow` / `release-flow`, `direct-release-flow`** — set to
  user-invocation only; trigger-phrase lists removed from descriptions.
- **`ceh-lessons-learned` / `lessons-learned`** — set to user-invocation only; removed the
  "trigger proactively at the end of a session" clause that contradicted the new flag.
- **`ceh-plan-build-review`** — all four skills (`plan-fullstack-app-iteratively`,
  `plan-fullstack-app-to-mvp`, `implement-from-plan`, `review-against-plan`) set to user-invocation
  only; these are explicit tasks pointed at a specific artifact, not proactive code-moment skills.

## [3.19.0] — 2026-07-12

The `ceh-web-frontend` design-system skill becomes **`ui-design`** — expanded from a theme-picker
into a comprehensive, framework-agnostic frontend UI visual design skill: the design decisions
(layout, hierarchy, navigation, states, density) now come first, with the bundled theme templates
as one layer of the whole.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-web-frontend` | v3.2.0 |

### Changed

- **`ceh-web-frontend` / `ui-design`** — renamed from `design-system` (the old name read as
  backend/DB system design; "design system" remains a trigger phrase in the description) and
  expanded into the full visual layer: a five-question design pass run before any markup, four
  layout archetypes (app shell, top-nav, focused flow, dashboard grid) with content-width and
  spacing-rhythm rules, hierarchy rules (one primary action per view, when a page title appears
  vs. repeats the nav label, "boxes are not structure"), navigation placement (sidebar vs. top bar
  vs. tabs vs. breadcrumbs, frequency ordering, active-state requirement), color/depth discipline,
  designed empty/loading/error/overflow states, density matching, a generic-AI anti-pattern list,
  and a six-point review pass. The original Meridian/Tidewater template workflow is kept,
  condensed into a "Theme layer" section.

### Added

- **`ceh-web-frontend` / `ui-design` / `references/examples.md`** — worked good/bad markup for
  each rule section (layout, spacing, header anatomy, navigation, color, states, density), built
  on the theme token/class contract; kept as a single file because the sections are consumed
  together when building a page.

## [3.18.0] — 2026-07-10

`ceh-fabled` grows from one skill to three: a plan-review skill that raises an existing plan to
frontier-grade planning discipline, and a failure-loop escape skill for repeated failed fixes.
The core `fabled` skill gets an enforcement pass so weaker executor models (Sonnet/Opus) actually
run the protocol instead of reading past it.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-fabled` | v1.1.0 |

### Added

- **`ceh-fabled` / `fabled-plan-review`** — review an existing plan (implementation plan,
  plan-mode output, migration plan, design doc) against a six-dimension rubric — problem fidelity,
  alternatives considered, decomposition quality, pre-mortem risk honesty, verifiability,
  calibrated delivery — delivering a lead verdict (*ready* / *ready after fixes* / *needs rework*),
  findings with concrete fixes, and a plan anti-pattern list.
- **`ceh-fabled` / `fabled-stuck`** — escape a failure loop after two or more failed fixes for the
  same symptom: freeze, inventory the attempts, attack their shared assumption, re-derive the
  diagnosis from raw evidence, widen the hypothesis space across five axes, probe before fixing,
  and exit only when the original failing case passes and the earlier failures are explained.

### Changed

- **`ceh-fabled` / `fabled`** — enforcement edits for weaker executor models: effort triage must
  be written as the first line of reasoning (was "silently"), reference loading is defined as a
  pre-stage-1 Read tool call hooked into triage, the adversarial-review stage now sweeps the draft
  against the anti-patterns list, the discipline is declared session-persistent, and the
  description gains "as fable" / "fable mode" trigger phrases.

## [3.17.3] — 2026-07-10

Full review/audit pass over all nineteen plugins (`ceh-summarize-chat` excluded by request):
verify every registered cross-reference block is in lockstep, syntax-check every shell script,
and fix the defects found. Content-only fixes to existing skills, agents, and scripts — no
skills or agents added.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.6.4 |
| `ceh-blog` | v1.0.7 |
| `ceh-documentation` | v1.1.2 |
| `ceh-git-workflow` | v3.2.2 |
| `ceh-plan-build-review` | v1.0.5 |
| `ceh-python-service` | v3.1.3 |

### Fixed

- **`ceh-documentation` / `scripts/check-semver.py`** — pre-release ordering in `semver_key` was
  inverted (a release ranked below its own pre-release, contradicting semver §11), so a correct
  newest-first changelog containing `1.2.3` above `1.2.3-rc.1` failed validation.
- **`ceh-documentation` / `update-changelog`** — the validate step located the bundled script via
  `${CLAUDE_PLUGIN_ROOT}`, which is only set for hook commands; it now resolves the script
  relative to the plugin root, keeping the manual fallback.
- **`ceh-git-workflow` / `hotfix`** — the command block used a lightweight tag where the release
  skill requires an annotated one, and never showed the PATCH version-bump commit that step 6
  demands; both corrected.
- **`ceh-git-workflow` / `dependency-management`** — `bun.lockb` → `bun.lock`, aligning with
  `ceh-web-frontend:environment` and the Bun 1.2+ text lockfile default.
- **`ceh-python-service` / `fastapi`** — the global exception-handler example returned a flat
  error body while claiming to match the skill's own contract, which nests fields under
  `"error"`; the example now matches.
- **`ceh-python-service` / `python-integration-tester`** — the httpx fixture used
  `AsyncClient(app=...)`, removed in httpx 0.28; replaced with `ASGITransport`.
- **`ceh-agent-coding-contract` / README** — the workflow summary contradicted the contract's
  Validation Policy (quick scoped checks are always allowed, not request-gated).
- **`ceh-plan-build-review`** — propagated drifted canonical §02 wording in `section-specs.md`
  to the iterative copy, and made plan output paths explicit
  (`.agents_workspace/planning/`) to match what the consumer skills glob.

### Changed

- **`ceh-blog`** — `blog-writer` and `blog-editor` now end with the same `blog-repurpose`
  handoff line `blog-interviewer` already had; the three-file duplication is registered in
  `CROSS_REFERENCES.md`.

---

## [3.17.2] — 2026-07-09

Move the multi-line git/gh message convention out of global config and into the git skills that
own each moment, and pin the release-flow subagent-delegation steps to an explicit model and
effort. Both are documentation-only refinements to existing skills — no skills or agents added.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.2.1 |
| `ceh-release-flow` | v1.1.4 |

### Changed

- **`ceh-git-workflow`** — `commit` and `open-pr` build multi-line commit/PR messages via a temp
  file (`git commit -F`, `gh pr create --body-file`) instead of inline heredocs, and `merge` uses
  `--body-file` for multi-line merge bodies. The temp-file path avoids shell quoting and behaves
  identically in PowerShell and Bash.
- **`ceh-release-flow`** — the subagent-delegation sections of `release-flow` and
  `direct-release-flow` now state the model and effort to dispatch each `ceh-git-workflow` agent on
  (Sonnet at medium reasoning effort), sourced from the agents' frontmatter.

---

## [3.17.1] — 2026-07-09

Add a description-length gate to the plugin validator: `tools/validate-plugins/validate.py`
now fails any skill or agent whose frontmatter `description` exceeds 1024 chars, enforced in
CI on every push/PR via the existing `.github/workflows/validate.yml` job. Trimmed the three
descriptions that were already over the limit — `plan-fullstack-app-to-mvp`
(`ceh-plan-build-review`), `evaluate-skill` (`ceh-evaluation`), and `design-system`
(`ceh-web-frontend`) — preserving every trigger phrase and disambiguation rule. No skills or
agents added.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-plan-build-review` | v1.0.4 |
| `ceh-evaluation` | v1.1.3 |
| `ceh-web-frontend` | v3.1.1 |

### Added

- **`tools/validate-plugins/validate.py`** — enforces a 1024-char limit on every skill/agent
  frontmatter `description`, checked in CI on every push and pull request.

### Fixed

- **`ceh-plan-build-review` / `plan-fullstack-app-to-mvp`** — description trimmed from 1245 to
  1019 chars; all trigger phrases and the disambiguation logic against
  `plan-fullstack-app-iteratively` preserved.
- **`ceh-evaluation` / `evaluate-skill`** — description trimmed from 1096 to 995 chars; all
  trigger phrases, the evidence-based battery steps, and both "not for" exclusions preserved.
- **`ceh-web-frontend` / `design-system`** — description trimmed from 1185 to 1021 chars; all
  trigger phrases, the Meridian/Tidewater menu, and all four "not for" redirects preserved.

---

## [3.17.0] — 2026-07-08

Add the `ceh-advisor` plugin — a stronger-model second-opinion subagent, an owned replacement for
the native `/advisor`. The main session consults the advisor at decision points, failure loops,
irreversible actions, and pre-completion gates; the reviewer model is a single `model:` line in
the agent frontmatter (Opus, high effort). Triggering is two-layer: soft description-driven
routing plus deterministic hook backstops that ship with the plugin and load automatically via
`hooks/hooks.json` — a PreToolUse guard that denies destructive bash commands until a fresh
advisor acknowledgement exists, and a PostToolUse watch that interrupts after consecutive failed
commands to force a diagnosis challenge. The advisor enforces an explicit handoff contract
(Situation / Options considered / Leaning toward / Relevant files) since subagents cannot see the
main conversation. Ships as a new plugin at v1.0.0; no other plugin's content changed.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-advisor` | v1.0.0 |

### Added

- **`ceh-advisor` / `ceh-advisor` agent** — verdict-first, read-only senior reviewer: conclusion
  in line 1, justification from files it reads itself, deliberate steelmanning of rejected
  options, and "missing: X, Y" instead of a guessed verdict on insufficient handoff.
- **`ceh-advisor` / destructive-command guard** (PreToolUse, Bash) — denies `rm -rf`,
  `git push --force`, migrations, `terraform apply`, `kubectl delete`, etc. until the advisor's
  one-line verdict is written to `.claude/.ceh-advisor-ack` (TTL-bound, doubles as an audit
  trail); extensible via `.claude/ceh-advisor-patterns.txt`.
- **`ceh-advisor` / consecutive-failure watch** (PostToolUse, Bash) — after N consecutive failed
  bash calls (default 3), feeds back an instruction to stop iterating and have the advisor
  challenge the diagnosis; both hooks degrade to inert when `jq` is absent.

### Changed

- **Plugin READMEs** (`ceh-dev-tools`, `ceh-orchestration`, `ceh-release-flow`) — agent invoke
  syntax updated from the slash form to the `@`-mention form; doc-only, no version bumps.

---

## [3.16.0] — 2026-07-08

Add subagent versions of the four mechanical git moments to `ceh-git-workflow`: `commit-author`,
`pr-opener`, `branch-merger`, and `release-cutter`. Each runs on Sonnet at medium effort in an
isolated context, preloads the skill that owns its moment via the `skills:` frontmatter field
(zero content duplication, no drift), and derives what changed from `git status`/`diff`/`log`
itself — callers pass only context the diff cannot show (the why, issue refs, testing notes, a
target version). The two `ceh-release-flow` skills gain an optional delegation path that
dispatches their mechanical tail steps to these agents while keeping every gate in the
orchestrating flow. The changelog/README updaters deliberately stay skills-only — they need the
live session's intent, which an isolated subagent cannot recover from a diff.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.2.0 |
| `ceh-release-flow` | v1.1.3 |

### Added

- **`ceh-git-workflow` / `commit-author`** — subagent that stages and creates one Conventional
  Commit for work already in the tree; pushes only when the caller says so.
- **`ceh-git-workflow` / `pr-opener`** — subagent that pushes the branch and opens the PR with the
  What/Why/How/Testing template, queueing auto-merge where the repo allows it; never invents
  testing claims.
- **`ceh-git-workflow` / `branch-merger`** — subagent that merges a PR or local branch into `main`
  behind the pre-merge gate (never past red) and runs the post-merge cleanup.
- **`ceh-git-workflow` / `release-cutter`** — subagent that tags `main` and publishes the GitHub
  release, committing the version bump only when it has not already landed ("tag-only" mode for
  the release flow).

### Changed

- **`ceh-release-flow` / `release-flow`** — new "Delegating steps 7–10 to subagents" section:
  commit/PR/merge/release may be dispatched to the matching `ceh-git-workflow` agent when
  installed; gates stay with the flow; skill delegation remains the fallback.
- **`ceh-release-flow` / `direct-release-flow`** — same optional delegation for its commit and
  tag+release steps (7–8).

---

## [3.15.0] — 2026-07-07

Add the `ceh-fabled` plugin — a cross-cutting reasoning-discipline layer for any non-trivial task.
Its single `fabled` skill encodes the process behind high-effort frontier-model output: silent
effort triage, generating genuine alternatives before committing, full-depth decomposition,
adversarial self-review, verification of the checkable, and calibrated, conviction-forward delivery.
Six task-typed reference files (reasoning moves, decision standards, technical rigor, research
epistemics, writing standards, interaction discipline) load on demand. Ships as a new plugin at
v1.0.0; no other plugin changed.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-fabled` | v1.0.0 |

### Added

- **`ceh-fabled` / `fabled`** — new plugin and skill applying frontier-grade reasoning discipline
  (deliberate thinking, alternative generation, adversarial self-review, verification, calibrated
  conviction) to analysis, decisions, debugging, architecture, planning, evaluation, research, and
  substantive writing; scoped with an effort-triage gate so trivial tasks skip the machinery.

---

## [3.14.1] — 2026-07-04

Audit of the `ceh-blog` skills for the personal, series-first voice. Skill descriptions are
shortened for manual invocation (trigger-signal lists dropped in favor of a routing hint),
`blog-repurpose` gains series awareness — adaptations use the post's open thread as enticement
into the serial without spoiling earlier episodes — and the plugin README is reframed to
manual-invocation-first. Content-only — no new skills or agents.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-blog` | v1.0.6 |

### Changed

- **`ceh-blog` / all four skills** — frontmatter descriptions cut to what-it-does plus a one-line
  routing hint between the skills; auto-trigger signal lists removed.
- **`ceh-blog` / `blog-repurpose`** — new Series Awareness block: threads and newsletter blurbs
  point at the series and use the open thread as the hook.
- **`ceh-blog` / README** — manual-invocation-first framing replaces the auto-trigger phrase lists.

---

## [3.14.0] — 2026-07-02

Add a `design-system` skill to `ceh-web-frontend` for giving a frontend its visual look and feel —
picking a theme or brand from bundled templates rather than restating generic design advice. Ships
with two ready-to-use brand templates (`meridian`, `tidewater`), each a `brand.css` plus a
`brand-guide.html` reference.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-web-frontend` | v3.1.0 |

### Added

- **`ceh-web-frontend` / `design-system`** — new skill that fires when giving a frontend its visual
  design (look/feel, theme, or brand), offering a menu of bundled brand templates and applying the
  chosen one; description sharpened for triggering and scoped with named non-goals.

---

## [3.13.4] — 2026-06-29

Close an auto-merge gap in the git workflow: opening a PR now enables GitHub auto-merge on repos
that allow it, so a PR can land itself without invoking the merge skill separately or running a full
release. The merge skill is reframed to cover both PR merges and local no-PR branch merges.
Skill-content only — no new skills or agents.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.1.5 |
| `ceh-release-flow` | v1.1.2 |

### Changed

- **`ceh-git-workflow` / `open-pr`** — after creating the PR, probe `allow_auto_merge` and enable
  auto-merge (`gh pr merge --merge --auto --delete-branch`) on repos that allow it, so the PR lands
  itself when the gate goes green — no separate merge step or release flow required.
- **`ceh-git-workflow` / `merge`** — reframed from PR-only to cover both PR merges (immediate or
  auto-merge) and local no-PR branch merges into `main` (`git merge --no-ff` + branch cleanup).
- **`ceh-release-flow` / `release-flow`** — pipeline steps 8–9 now reflect that `open-pr` queues
  auto-merge at PR-creation time; step 9 confirms it lands or falls back to a direct merge.

---

## [3.13.3] — 2026-06-22

Reconcile the `orchestrate` trigger with measured behavior so it stops over-promising on pure
cost-framed tasks. Skill-content only — no new skills or agents.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-orchestration` | v1.0.1 |

### Changed

- **`ceh-orchestration` / `orchestrate`** — narrowed the trigger to heterogeneous /
  investigation-heavy work and added carve-outs (mechanical single-pass changes → tooling; a
  single one-off subagent dispatch → not this skill). A skill evaluation found the prior
  "minimize token/context cost on any big task" wording over-promised: on mechanical work,
  tooling (sed + typecheck) beats delegation, so the skill produced no behavioral lift there.
  Re-test confirmed the change is non-regressive (positives 6/8, false-fires 0/8).

---

## [3.13.2] — 2026-06-22

Disambiguate the trigger boundary between `plan-fullstack-app-to-mvp` and its iterative counterpart
so version-increment requests stop routing to the all-at-once planner. Skill-content only — no new
skills or agents.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-plan-build-review` | v1.0.3 |

### Changed

- **`ceh-plan-build-review` / `plan-fullstack-app-to-mvp`** — sharpened the description so "plan the
  next version" / "plan v2's scope" routes to `plan-fullstack-app-iteratively`, and only an entire
  major-version-to-MVP request routes here. A skill evaluation found the prior wording over-triggered
  on version-increment prompts (false-positive rate 1/6 → 0/6 after the fix).

---

## [3.13.1] — 2026-06-22

Sharpen the `release-flow` skill's merge step so it prefers GitHub auto-merge instead of hand-polling
CI. Skill-content only — no new skills or agents.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-release-flow` | v1.1.1 |

### Changed

- **`ceh-release-flow` / `release-flow`** — step 9 now explicitly nudges toward `--auto` (queue the
  merge and let GitHub land it when the branch-protection gate goes green; don't poll CI by hand),
  pointing at the `ceh-git-workflow:merge` auto-merge probe rather than duplicating its mechanics.

---

## [3.13.0] — 2026-06-22

Add the **`ceh-evaluation`** plugin — a workflow for evaluating a Claude Code skill or plugin you
just wrote. It derives the skill's own success criteria, then measures four dimensions with evidence
— structural integrity, triggering accuracy, content quality, and behavioral lift — and loops
fix → re-run until a readiness gate passes. It treats `skill-creator` and `plugin-dev` as optional
cross-checks, not authorities, and ships a lite dev-loop variant that skips behavioral lift for a
cheap sanity check during iteration.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-evaluation` | v1.1.2 (new) |

### Added

- **`ceh-evaluation`** — new use-case workflow plugin with two skills. `evaluate-skill` runs the
  full evaluation: it derives criteria from the target skill, scores structure / triggering /
  content / behavioral lift against evidence captured under `.agents_workspace/`, and loops
  fix → re-run until a 6-point readiness gate passes. `evaluate-skill-lite` is a fast dev-loop
  variant — structure + a single triggering pass + content only — that skips behavioral lift and
  reports a partial 4/6 gate for cheap iteration before the full ship verdict. Eval-generated code
  is confined to per-run `iteration-N/generated/` directories, and output is indexed per run so
  re-runs do not overwrite prior evidence. Ships `eval-report-schema.md` and `eval-rubric.md`
  reference templates.

---

## [3.12.0] — 2026-06-21

Add the **`ceh-business-plan`** plugin — an interview-driven workflow that turns a product idea, or
an existing `plan-build-review` app plan, into a validated business plan with a clear product-market
fit. It drafts proactively from whatever already exists, then runs a disciplined interview/revise
loop that attacks the plan's weakest assumption one question at a time until an 8-point PMF
readiness gate passes.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-business-plan` | v1.0.0 (new) |

### Added

- **`ceh-business-plan`** — new use-case workflow plugin with the `develop-business-plan` skill. The
  skill seeds a draft from `plan-build-review` app plans (`SKELETON.md` / `ITER_NN.md`) or any
  PRD/spec/pitch, tags every load-bearing claim `[evidence]` / `[assumption]` /
  `[hypothesis-to-test]`, and loops interview → revise → re-score until the PMF gate reaches 8/8 and
  the user confirms. Ships a `business-plan-schema.md` reference template.

---

## [3.11.3] — 2026-06-20

Add continuous integration that validates the repository's structural integrity on every push to
`main` and every pull request. Repo-tooling only — no plugin behavior changes.

### Plugin versions

No plugin version changes — this release adds repo-level CI tooling only.

### Added

- **CI** — `.github/workflows/validate.yml` runs a new stdlib-only validator
  (`tools/validate-plugins/validate.py`) that checks: `plugin.json`/`marketplace.json` manifests
  (valid JSON, name matches directory, semver, version parity, every plugin listed with an existing
  source), `SKILL.md` and agent frontmatter (`name` + `description`, name matches directory),
  `references/` and `${CLAUDE_PLUGIN_ROOT}/scripts/` file references, `plugin:component` skill
  references, and script syntax (`bash -n` / `shellcheck` / `py_compile`).

---

## [3.11.2] — 2026-06-20

The `merge` skill now uses GitHub auto-merge when the repository allows it, falling back to a direct
merge otherwise — the merge lands automatically once the branch-protection gate (CI + approvals) is
satisfied, instead of waiting on CI by hand.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.1.4 |

### Changed

- **`ceh-git-workflow`** (v3.1.4) — `merge` skill probes `gh api repos/{owner}/{repo} --jq .allow_auto_merge`
  and prefers `gh pr merge --merge --auto` when enabled, falling back to a direct merge; the auto-merge
  and post-merge cleanup steps are consolidated into a single **Merge & Cleanup** section.

---

## [3.11.1] — 2026-06-20

Move the living architecture doc out of the committed `docs/` tree into the gitignored
`.agents_workspace/`. The `user-operator-guide` output stays in `docs/guide/` — those guides are
intended deliverables for other readers and must remain committed.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-architecture` | v3.1.1 |

### Changed

- **`ceh-architecture`** (v3.1.1) — `document-architecture` now writes the living architecture doc to
  `.agents_workspace/ARCHITECTURE.md` (and `.agents_workspace/architecture/` for large systems)
  instead of `docs/`.

---

## [3.11.0] — 2026-06-20

Consolidate architecture decision records into the living architecture doc. The standalone `adr`
skill is replaced by a `document-architecture` skill that captures durable decisions as a **Key
Decisions** section inside `ARCHITECTURE.md` (alongside the Mermaid diagrams), and every other
skill that referenced `docs/adr/DECISIONS.md` now points at `ARCHITECTURE.md` Key Decisions.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-architecture` | v3.1.0 |
| `ceh-git-workflow` | v3.1.3 |
| `ceh-ops` | v3.0.2 |
| `ceh-python-service` | v3.1.2 |

### Added

- **`ceh-architecture`** (v3.1.0) — new `document-architecture` skill: maintains a living
  `ARCHITECTURE.md` with Mermaid diagrams and a **Key Decisions** section that records durable
  architectural decisions inline (replacing separate ADR files).

### Removed

- **`ceh-architecture`** (v3.1.0) — removed the standalone `adr` skill; its responsibility is now
  folded into `document-architecture`.

### Changed

- **`ceh-git-workflow`** (v3.1.3) — `code-review`, `dependency-management`, and `open-pr` skills
  now reference `ARCHITECTURE.md` Key Decisions instead of `docs/adr/DECISIONS.md`.
- **`ceh-ops`** (v3.0.2) — `deploy` skill's breaking-change gate now requires an `ARCHITECTURE.md`
  Key Decisions entry instead of an ADR entry.
- **`ceh-python-service`** (v3.1.2) — `fastapi` skill's API-versioning guidance now records the
  deprecation timeline in `ARCHITECTURE.md` Key Decisions instead of an ADR.

---

## [3.10.3] — 2026-06-19

Redirect all skill *session-artifact* outputs from `docs/` to `.agents_workspace/` so agent-generated
logs and plans no longer land in the committed `docs/` tree. Committed project documentation (ADRs
under `docs/adr/`, user guides under `docs/guide/`) is unchanged.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.6.3 |
| `ceh-lessons-learned` | v2.0.4 |
| `ceh-ops` | v3.0.1 |
| `ceh-plan-build-review` | v1.0.2 |

### Changed

- **`ceh-agent-coding-contract`** (v2.6.3) — Decision Log default path moved from
  `docs/claude_logs/DECISION_LOG.md` to `.agents_workspace/DECISION_LOG.md` (SKILL + README).
- **`ceh-lessons-learned`** (v2.0.4) — `LESSONS_LEARNED.md` output moved from `docs/claude_logs/`
  to `.agents_workspace/` (SKILL + README).
- **`ceh-ops`** (v3.0.1) — `rollback` skill's Decision Log default path updated to
  `.agents_workspace/DECISION_LOG.md`.
- **`ceh-plan-build-review`** (v1.0.2) — plan producers (`plan-fullstack-app-iteratively`,
  `plan-fullstack-app-to-mvp`) now save to `.agents_workspace/planning/`; consumers
  (`implement-from-plan`, `review-against-plan`) now expect plans under `.agents_workspace/planning/`
  or any subfolder within it.
- **Repo** — `.gitignore` now ignores `.agents_workspace/`; root `CLAUDE.md` structure tree updated
  to document the new workspace directory.

---

## [3.10.2] — 2026-06-19

Require Mermaid diagrams (not ASCII art) in plan-build-review's §02 Architecture section, and
require iteration diagrams to visualize what changed rather than just restating the current state.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-plan-build-review` | v1.0.1 |

### Changed

- **`ceh-plan-build-review`** (v1.0.1) — §02 Architecture skeleton diagrams must now be Mermaid
  instead of ASCII art; iteration diagrams must additionally visualize what changed this iteration.
  Propagated across the producer specs (`plan-fullstack-app-iteratively`,
  `plan-fullstack-app-to-mvp`), the consumer schemas (`implement-from-plan`, `review-against-plan`),
  both audit checklists, and `review-against-plan`'s post-implementation check table.
  `CROSS_REFERENCES.md` updated with the new duplication entry.

---

## [3.10.1] — 2026-06-18

Rewrite every plugin hook from Node to pure Bash so hooks run on machines without a Node
runtime (e.g. locked-down hosts where installing Node needs admin approval).

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.6.2 |
| `ceh-architecture` | v3.0.3 |
| `ceh-python-library` | v1.2.1 |
| `ceh-python-service` | v3.1.1 |
| `ceh-web-frontend` | v3.0.4 |

### Changed

- **`ceh-agent-coding-contract`** (v2.6.2), **`ceh-architecture`** (v3.0.3),
  **`ceh-python-library`** (v1.2.1), **`ceh-python-service`** (v3.1.1),
  **`ceh-web-frontend`** (v3.0.4) — all SessionStart/UserPromptSubmit hooks emitted a static
  JSON payload via Node; each `*.js` is replaced by a `*.sh` that prints the identical JSON from a
  single-quoted heredoc, and every `hooks.json` now invokes `bash` instead of `node` (the official
  plugin-hook convention). Removes the Node runtime dependency; each `.sh` output was verified to
  parse to JSON identical to the Node version. Plugin READMEs and `CROSS_REFERENCES.md` updated to
  the new `.sh` paths.

---

## [3.10.0] — 2026-06-18

Add a PR-less variant to `ceh-release-flow`: `direct-release-flow` runs the same release pipeline
straight on `main`, with no branch, PR, or merge.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-release-flow` | v1.1.0 |

### Added

- **`ceh-release-flow`** (v1.1.0) — new `direct-release-flow` skill: the PR-less twin of
  `release-flow`. Same pipeline (semver bump → bump every manifest → changelog → README → CLAUDE.md
  → commit → tag → GitHub release) but committed directly to an up-to-date `main`, dropping the
  branch/open-pr/merge steps. For solo repos and low-risk releases where direct-to-`main` is the
  norm. The plugin README gains a Dependencies section documenting the delegated skills and the
  soft-dependency fallback (a missing plugin makes the flow apply the step's standard inline rather
  than skip it).

---

## [3.9.0] — 2026-06-18

Add the `ceh-release-flow` plugin: a single orchestrator skill that ships a complete release in
one pass by sequencing the skills that already own each step — no standard is duplicated.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-release-flow` | v1.0.0 (new) |

### Added

- **`ceh-release-flow`** (v1.0.0, new plugin) — `release-flow` skill orchestrating the end-to-end
  release pipeline: semver bump → branch → bump every manifest → changelog → README → CLAUDE.md →
  commit → PR → merge → tag → GitHub release. Delegates each step to its owning skill
  (`ceh-git-workflow:branch`/`commit`/`open-pr`/`merge`/`release`,
  `ceh-documentation:update-changelog`/`update-readme`); its only original content is the
  step ordering, the gate between steps, and the rule that the bump lands via a reviewed PR and
  the tag/release are cut on `main` against the merge commit after merge.

---

## [3.8.2] — 2026-06-17

Expand the `ceh-git-workflow` skills with the concrete templates and examples that earlier
token-efficiency passes had stripped, while keeping each skill tight.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.1.2 |

### Changed

- **`ceh-git-workflow`** (v3.1.2) — all eight skills expanded with inline templates and examples:
  - `commit` — scope-selection guidance, `build`/`ci`/`style`/`revert` types, a bad-vs-good
    subject, body formatting, and concrete footers including the AI-attribution line.
  - `merge` — a merge-commit message template and a rebase-based conflict-resolution flow.
  - `open-pr` — per-section how-to guidance and a filled-in example description.
  - `branch` — the branch-from-main rationale and a rebase-to-stay-current flow.
  - `code-review` — review structure, an approve/request-changes/comment verdict, and
    author-response guidance.
  - `dependency-management` — add/remove/upgrade commands plus lockfile and pinning caveats.
  - `hotfix` — post-fix verification and post-mortem follow-up.
  - `release` — pre-release version suffixes; changelog format deferred to its own skill.
  - Cross-skill pointers now use trigger phrases only (no plugin/skill names) so they degrade
    gracefully when a referenced plugin is not installed.

---

## [3.8.1] — 2026-06-17

Fix `check-semver.py` date parsing so it recognizes this repo's em-dash changelog headers.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-documentation` | v1.1.1 |

### Fixed

- **`ceh-documentation`** (v1.1.1) — `scripts/check-semver.py` now accepts either a hyphen (`-`) or
  an em-dash (`—`) as the date separator in version headers. Previously it only matched the hyphen,
  so every em-dash entry (the repo's CHANGELOG convention) was flagged "no date".

---

## [3.8.0] — 2026-06-17

Convert the `ceh-documentation` changelog and README agents into skills, so they run in the main
session and reuse its live context instead of re-deriving it in an isolated agent.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-documentation` | v1.1.0 |
| `ceh-git-workflow` | v3.1.1 |

### Added

- **`ceh-documentation`** (v1.1.0) — two skills converted from the former agents:
  - `update-changelog` — generate or update `CHANGELOG.md` from git history (semver + Keep a
    Changelog), with a no-tag full-history fallback and language-agnostic manifest references.
  - `update-readme` — keep `README.md` accurate after a significant change, gated so
    internal/minor changes are a no-op.

### Changed

- **`ceh-git-workflow`** (v3.1.1) — the `release` skill now prompts to update the changelog before
  bumping the version, referenced by trigger phrase rather than a hard cross-plugin dependency.
- **`ceh-documentation`** — `scripts/check-semver.py` output is now ASCII-only (fixes a Windows
  cp1252 crash on the `→` glyph); fixed a nested-code-fence rendering bug in `user-operator-guide`.

### Removed

- **`ceh-documentation`** — the `changelog-agent` and `readme-updater` agents, superseded by the
  `update-changelog` and `update-readme` skills.

---

## [3.7.1] — 2026-06-15

Simplify `write-less-code` reinforcement in `ceh-agent-coding-contract`: drop the redundant
session-start load that did not fire reliably, leaving the per-turn digest as the primary delivery.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.6.1 |

### Changed

- **`ceh-agent-coding-contract`** (v2.6.1) — the `write-less-code` skill is no longer force-loaded
  at session start.
  - Removed the `SessionStart` hook `load-less-code.js` (and its `hooks.json` entry). It injected a
    deferred "before implementing, invoke the skill" directive that did not fire reliably when a
    session ran a while before writing code.
  - The per-turn `UserPromptSubmit` digest (`less-code-payload.js`) is now the primary delivery — it
    carries the full ladder on every turn from turn one; the full skill loads on demand when
    non-trivial code is written.
  - Cut the "Always-on" plumbing section from the skill body (documentation, not behavior).

---

## [3.7.0] — 2026-06-14

New `write-less-code` skill in `ceh-agent-coding-contract`: the positive half of minimalism
(the contract already owns the negative rules), wired always-on via session-start load plus a
per-turn reinforcement hook.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.6.0 |

### Added

- **`ceh-agent-coding-contract`** (v2.6.0) — new skill `write-less-code`.
  - The minimalism ladder (YAGNI → stdlib → native platform feature → already-installed
    dependency → one line → minimum that works), native-platform-first, and the `// less-code:`
    shortcut convention. Framed as the *positive* delta over the contract's "Universal Non-Goals"
    (no new deps, no speculative abstractions, minimal diffs), not a restatement. Inspired by
    [ponytail](https://github.com/DietrichGebert/ponytail) (MIT, DietrichGebert).
  - Loaded at session start via a new `SessionStart` hook (`load-less-code.js`, firing on
    `startup`/`resume`/`clear`/`compact`) and reinforced every turn via a `UserPromptSubmit` hook
    (`less-code-payload.js`) that re-injects a compact ladder digest, so the reflex survives
    long-session context drift. No configuration or env var required.

---

## [3.6.0] — 2026-06-13

New `ceh-orchestration` plugin: consolidates a thin-orchestrator setup (cost-optimized,
delegate-only main session plus worker subagents) into the marketplace.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-orchestration` | v1.0.0 |

### Added

- **`ceh-orchestration`** (v1.0.0) — new plugin.
  - Skill `orchestrate` — thin-orchestrator mode: the main session restates the goal,
    decomposes into a dependency-ordered plan, dispatches subtasks to workers, and keeps a
    compact result ledger while doing no file I/O itself. Covers the context-isolation cost
    model, model routing (Opus → Sonnet → Haiku), spec discipline, ranked cost levers, and
    why subagents beat Agent Teams for a cost goal.
  - Agents `executor` (Sonnet, scoped implementation) and `verifier` (Haiku, PASS/FAIL
    acceptance check) — the workers the skill dispatches to. Both are scoped to
    thin-orchestrator mode and do not auto-invoke outside it, so installing the plugin does
    not divert ordinary edits into a subagent. Read-only exploration is delegated to Claude
    Code's built-in `Explore` agent (no custom explorer ships), since it skips `CLAUDE.md`
    inheritance and so carries the least context tax.

---

## [3.5.0] — 2026-06-11

Duplicated skill names made unique across plugins: the `python-environment` / `python-testing`
pairs shared by `ceh-python-service` and `ceh-python-library` are renamed to plugin-qualified
names so each skill name maps to exactly one plugin.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-python-service` | v3.1.0 |
| `ceh-python-library` | v1.2.0 |
| `ceh-scaffolding` | v1.0.1 |
| `ceh-web-frontend` | v3.0.3 |

### Changed

- **`ceh-python-service`** (v3.1.0) — skills renamed: `python-environment` →
  `python-service-environment`, `python-testing` → `python-service-testing`. Hook tags, tester
  agents' `skills:` lists, and in-plugin references updated.
- **`ceh-python-library`** (v1.2.0) — skills renamed: `python-environment` →
  `python-library-environment`, `python-testing` → `python-library-testing`. Hook tags and
  in-plugin references updated.
- **`ceh-scaffolding`** (v1.0.1) — scaffold skills' references updated to the new skill names.
- **`ceh-web-frontend`** (v3.0.3) — reference-text updates to the new skill names.
- `CROSS_REFERENCES.md` — new "Same Skill, Different Plugins" map tracking the renamed pairs;
  root and plugin READMEs updated.

Old invocations (`/ceh-python-service:python-environment` etc.) must switch to the new names;
auto-load behavior is unaffected (descriptions unchanged).

---

## [3.4.0] — 2026-06-11

New standalone `skills-sync` tool under `tools/` — copies Claude Code skills from this repo's
plugins into a project's `.claude/skills/`. Repo tooling only; no plugin versions change.

### Added

- **`tools/skills-sync`** — skill-sync tool in three equivalent implementations (`skills-sync.ps1`,
  `skills-sync.sh`, `skills-sync.py`) plus a Tidewater-themed `skills-sync.html` picker page
  (CSS/JS extracted into separate files) and a tools README. Syncs selected skills into
  `.claude/skills/`, ignoring individual skill folders rather than the whole `skills/` directory.
  Cross-implementation bugs from a second audit pass fixed.

---

## [3.3.2] — 2026-06-10

`ceh-agent-coding-contract` contract clarified after a cross-model evaluation (Haiku 4.5,
Sonnet 4.6, Opus 4.8, Fable 5): the blanket no-command-execution rule is replaced by a tiered
Validation Policy, and scope, authority, and sub-agent rules are tightened.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.5.1 |

### Changed

- **`ceh-agent-coding-contract`** (v2.5.1) —
  - **Validation Policy** (replaces the "no validation/command execution unless requested" hard
    rule): read-only inspection (`ls`, `grep`, `git status`/`log`/`diff`) and quick correctness
    checks scoped to the edit (syntax, type-check of changed files, import resolution, throwaway
    sanity snippets) are always allowed; writing tests, running test suites, builds, repo-wide
    lint/format, and any state-changing command require an explicit request. Unrequested heavier
    validation is reported in the summary with the exact command instead of run; delegation to a
    tester sub-agent now applies only to *requested* validation (closes a loophole).
  - **Scope** redefined as what is necessary to fulfill the request — not only files the user
    named; beyond that, no drive-by fixes or opportunistic refactors; unsure remains out-of-scope.
  - **Authority hierarchy**: project `CLAUDE.md` (then user-level) now ranks above the contract.
  - **Five-step workflow**: trivial tasks may compress steps 1, 2, and 5 to one sentence each;
    step 5 summaries must state what was *not* validated.
  - **Sub-agents**: on a Stop Condition, report to the calling agent (`AskUserQuestion` is
    unavailable to sub-agents).
  - **Decision Log**: entry IDs are sequential integers; creating/appending the log is
    pre-authorized. Fixed a duplicate "Entry 3" heading in this repo's log (now Entry 13).

---

## [3.3.1] — 2026-06-10

`ceh-blog` rewritten for a personal, non-influencer voice with series continuity; all four
skills compressed for token efficiency.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-blog` | v1.0.5 |

### Changed

- **`ceh-blog`** (v1.0.5) —
  - **Voice**: new Voice section (word-for-word identical in `blog-writer` and `blog-interviewer`)
    — first-person, reflective, the reader overhears the reasoning; banned influencer tells
    (standalone one-liner paragraphs, aphoristic closers, imperative lessons, "If you're building
    X, then Y", bold pseudo-headers, meta-takeaway sign-offs, CTA endings); a never-invent rule
    (every beat from the material or the author's words — flag missing beats, don't fabricate);
    and a `CLAUDE.md` blog-voice override.
  - **Endings**: all six post-type templates end on "The Open Thread" (honest current state —
    what's unresolved, what comes next; a reserved verdict is valid; closure only for a finished
    series' final post) instead of Takeaway/CTA/conviction conclusions. Ending lines are
    byte-identical across writer, interviewer, and editor.
  - **Series continuity**: the blog is treated as serials — each project a series, each post an
    episode. `blog-writer` gains a Series Awareness step (read prior posts, pick up the previous
    episode's thread, cross-link, check continuity facts); `blog-interviewer` reads the blog (not
    just the repo) in Phase 0, asks whether the new post answers the last post's open thread, and
    pins chronology relative to the previous episode.
  - **Interviewing**: four required story beats for story-voice posts (the turn, the moment, the
    verdict, the thread — the thread becomes the ending); hypothesis-option questions permitted;
    answer-drift handling (keep the answer, re-ask once at most); verbatim quote capture (the
    user's phrasing is the voice).
  - **`blog-editor`** aligned so it diagnoses influencer tells and series-continuity slips instead
    of "fixing" open endings into conviction closers. `blog-repurpose` voice rules unchanged —
    its CTA conventions are platform-native to social formats.
  - **Token efficiency**: all four skill bodies compressed (−23% chars, 56.4k → 43.7k) with no
    rule, trigger phrase, or template line dropped; the duplicated Voice and template blocks are
    registered in `CROSS_REFERENCES.md`.

---

## [3.3.0] — 2026-06-09

New `ceh-plan-build-review` plugin: the full plan-driven development loop (plan → implement →
review) in one plugin; the implement/review skills moved out of `ceh-agent-coding-contract`.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-plan-build-review` | v1.0.0 |
| `ceh-agent-coding-contract` | v2.5.0 |

### Added

- **`ceh-plan-build-review`** (v1.0.0) — new use-case plugin bundling four skills:
  - `plan-fullstack-app-iteratively` (new) — plans one release at a time; each session produces a
    single `SKELETON.md` / `ITER_NN.md` artifact scoped to the next build.
  - `plan-fullstack-app-to-mvp` (new) — plans the complete build to a working MVP in one session;
    a complexity gate hands off to the iterative planner when upfront planning is unsafe.
  - `implement-from-plan` (moved from `ceh-agent-coding-contract`) — implements a plan
    document section by section, including the `plan-schema.md` reference.
  - `review-against-plan` (moved from `ceh-agent-coding-contract`) — audits the
    codebase against a plan document and fixes gaps/deviations/errors.
- **`CROSS_REFERENCES.md`** — new "Plan document schema" entry registering the duplication between
  the consumer-side `plan-schema.md` copies and the two planners' `section-specs.md` (producer
  side). The duplication is intentional — the skills are also used standalone outside the plugin —
  and is the repo's only sanctioned exception to the no-duplicated-references rule.

### Changed

- **`ceh-plan-build-review`** — `plan-schema.md` reconciled to the planner skills' schema (the
  golden standard): `mvp: true` and `mvp_target` live on the terminator iteration only, non-terminal
  iterations omit the `mvp` key, and the SKELETON carries no MVP fields; the `## Out of MVP scope`
  block moved from the SKELETON to the terminator. `review-against-plan` now carries its own copy
  of `plan-schema.md` instead of reaching into `implement-from-plan/` by relative path, so every
  skill folder is self-contained for standalone use.

### Removed

- **`ceh-agent-coding-contract`** (v2.5.0, MINOR per the v2.3.0 skill-removal precedent) —
  `implement-from-plan` and `review-against-plan` moved to `ceh-plan-build-review`. The contract
  plugin is now contract-only (skill + SessionStart hook); README updated with a pointer to the
  new plugin.

---

## [3.2.0] — 2026-06-07

New `merge` skill, and the `open-pr` skill triggers more reliably.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.1.0 |

### Added

- **`ceh-git-workflow`** — new `merge` skill owning the merge-and-cleanup moment: pre-merge gate
  (CI green, approvals, rebased, clean history), merge-commit strategy (no squash/rebase-merge),
  and post-merge cleanup (delete remote + local branch, return to `main`, prune). Triggers on
  "merge it", "merge and delete the branch", "clean up the branch", and the merge half of compound
  requests like "create a PR, merge it, delete the branch".

### Changed

- **`ceh-git-workflow`** — the `open-pr` skill under-triggered on compound requests (e.g. "create
  pr, merge and delete branch") because its description named only "opening a pull request".
  Rewrote it to match any phrasing (create/open/raise/make/submit/send a PR, pull request, or merge
  request) and to scope the PR-creation half of compound requests, deferring merge/cleanup to the
  new `merge` skill. Moved the merge-commit policy out of `open-pr` (now a one-line pointer) so the
  `merge` skill owns it with no duplication.

---

## [3.1.4] — 2026-06-06

The `release` skill triggers more reliably and is no longer stack-specific.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-git-workflow` | v3.0.1 |

### Changed

- **`ceh-git-workflow`** — the `release` skill under-triggered: its description named only
  `pyproject.toml`/`package.json` for version bumps (missing `plugin.json`/`marketplace.json` and
  other ecosystems), carried no literal user-phrasings, and stopped at the git tag without covering
  GitHub releases. Rewrote the description with quoted trigger phrases ("cut a release", "create a
  release", "bump the version(s)", etc.) and a manifest-agnostic file list (examples, not a closed
  set). Updated the command sequence to use an annotated tag (`git tag -a -m`, avoiding the "no tag
  message" failure on repos that enforce it) and to include the optional `gh release create` step.

---

## [3.1.3] — 2026-06-06

SessionStart hooks now surface a user-visible note when they fire.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.6 |
| `ceh-architecture` | v3.0.2 |
| `ceh-python-service` | v3.0.1 |
| `ceh-python-library` | v1.1.1 |
| `ceh-web-frontend` | v3.0.2 |

### Changed

- **`ceh-agent-coding-contract`, `ceh-architecture`, `ceh-python-service`, `ceh-python-library`,
  `ceh-web-frontend`** — each plugin's SessionStart hook injected its directive/invariants only via
  `additionalContext`, which reaches Claude but is never shown to the user, so there was no signal
  in the conversation UI that the hook had fired. Added a `systemMessage` field to each hook so the
  user sees a short note (e.g. "ceh-python-service: loading Python service invariants for this
  session.") on session start, `/clear`, and compaction. The `additionalContext` payloads are
  unchanged.

---

## [3.1.2] — 2026-06-06

Plan skills now auto-trigger on version-tagged phrasing.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.5 |

### Changed

- **`ceh-agent-coding-contract`** — `implement-from-plan` and `review-against-plan` handled
  version-tagged plans in their bodies (v3.1.1) but their `description` frontmatter carried no
  version phrasing, so prompts like "implement v2 iter plans" never auto-triggered. Added
  version-tagged trigger phrases and noted `SKELETON_v2.md` / `v2_ITER_03.md` variants and
  `depends_on`-chain resolution in both descriptions. No body changes.

---

## [3.1.1] — 2026-06-05

Plan skills support version-tagged plan files and `depends_on`-based resolution.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.4 |

### Changed

- **`ceh-agent-coding-contract`** — `implement-from-plan` and `review-against-plan` were hardcoded
  to `SKELETON.md` / `ITER_NN.md`. Generalized discovery to match optional version tags (prefix or
  suffix, e.g. `SKELETON_v2.md`, `v2_ITER_03.md`) and grouped files into plan families. Resolution
  now follows the `depends_on` chain backward (never forward), crossing into a base version where a
  later version builds on it.
- **`plan-schema.md`** — aligned to the canonical section spec: added `mvp_target` (SKELETON) and
  the `mvp` terminator + `depends_on` (ITER, artifact stems); documented the SKELETON
  `## Out of MVP scope` block. Clarified that `mvp` / `mvp_target` are optional (no terminator
  inferred when absent), that skeletons carry no `depends_on`, and the same-sequence vs
  cross-version `depends_on` chain forms.

---

## [3.1.0] — 2026-06-05

SessionStart hook audit: added one missing invariants hook and fixed two that were silently failing.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-architecture` | v3.0.1 |
| `ceh-python-library` | v1.1.0 |
| `ceh-web-frontend` | v3.0.1 |

### Added

- **`ceh-python-library`** — SessionStart invariants hook (`hooks/hooks.json` → `hooks/load-invariants.js`)
  injecting the passive `python-environment` style/type and minimal-dependency rules, mirroring
  `ceh-python-service`. Closes a shared-standards gap: the library carried the same invariant skill
  but no hook to enforce it. Added a parallel `## Hooks` section to the plugin README.

### Fixed

- **`ceh-architecture`**, **`ceh-web-frontend`** — the SessionStart hook scripts had an escaped
  closing backtick (`\``) that left the template literal unterminated, so `node` threw a
  `SyntaxError` and the hook injected nothing. Both invariants blocks were silently never reaching
  sessions. Both now emit valid JSON.

---

## [3.0.0] — 2026-06-05

Use-case-based plugin reorganization (see `.agents_workspace/PLUGIN_REORG_PLAN.md`). **Breaking:** four plugins
were renamed; there are no alias shims. Net 11 → 13 plugins.

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.3 |
| `ceh-architecture` | v3.0.0 |
| `ceh-blog` | v1.0.4 |
| `ceh-dev-tools` | v1.1.2 |
| `ceh-documentation` | v1.0.1 |
| `ceh-git-workflow` | v3.0.0 |
| `ceh-lessons-learned` | v2.0.3 |
| `ceh-ops` | v3.0.0 |
| `ceh-python-library` | v1.0.0 |
| `ceh-python-service` | v3.0.0 |
| `ceh-scaffolding` | v1.0.0 |
| `ceh-summarize-chat` | v2.0.3 |
| `ceh-web-frontend` | v3.0.0 |

### Renamed (breaking)

- `ceh-release-ops` → **`ceh-ops`**; `ceh-python-backend` → **`ceh-python-service`**;
  `ceh-typescript-frontend` → **`ceh-web-frontend`**; `ceh-architecture-design` → **`ceh-architecture`**.

### Added

- **`ceh-python-library`** (NEW) — packaging/publishing, public-API surface, semver, plus uv environment
  and pytest testing duplicated-and-trimmed from `ceh-python-service` (no web deps).
- **`ceh-scaffolding`** (NEW) — per-project-type setup (service, library, web frontend, fullstack); folds
  in the former `gitignore` skill's entries.
- **`ceh-web-frontend`** — new `react-vite` skill; now covers Svelte and React in one plugin.

### Changed

- **`ceh-ops`** — deduped: security/observability/database-migrations merged into `ceh-python-service`,
  definition-of-done merged into `ceh-git-workflow:open-pr`, versioning split (semver → git-workflow,
  deploy pipeline → new `deploy` skill). Keeps incidents, rollback, deploy + CI agents.
- **`ceh-python-service`** — `fastapi` absorbs rest-api design; `asyncpg` absorbs postgresql driver rules;
  `postgresql` moved in (schema design); observability/security adopt the richer ops content.
- **`ceh-web-frontend`** — consolidated `coding-style` + `linting` into `environment`; generalized
  `accessibility`/`frontend-testing` to `.svelte` and `.tsx`.
- **`ceh-architecture`** — trimmed to `adr` + `domain-modeling`; hook invariants trimmed accordingly.
- **`ceh-git-workflow`** — `open-pr` absorbed the definition-of-done quality gate.
- **`ceh-agent-coding-contract`** (PATCH) — Decision Log section now states the log is the required
  channel and is not satisfied by a commit message/PR/summary; log at the moment of the decision.

### Removed

- `event-sourcing` and `llm-integration` skills (app-specific, not reusable standards).
- standalone `rest-api`, `postgresql` (moved), `repository-structure` (folded into scaffolding),
  and `gitignore` (folded into scaffolding) skills.
- dead `scripts/sync-stubs.ps1`.

---

## [2.8.0] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.2 |
| `ceh-architecture-design` | v2.2.2 |
| `ceh-blog` | v1.0.4 |
| `ceh-dev-tools` | v1.1.2 |
| `ceh-documentation` | v1.0.1 |
| `ceh-git-workflow` | v2.5.3 |
| `ceh-lessons-learned` | v2.0.3 |
| `ceh-python-backend` | v2.3.1 |
| `ceh-release-ops` | v2.2.5 |
| `ceh-summarize-chat` | v2.0.3 |
| `ceh-typescript-frontend` | v2.3.0 |

### Added

- **`ceh-architecture-design`**, **`ceh-python-backend`**, **`ceh-typescript-frontend`** (MINOR) — each ships a `SessionStart` invariants hook that injects always-on domain invariants (the rules that under-trigger as auto-load skills because they fire on implicit mid-turn decisions). Skills remain the on-demand depth reference, routed via `<plugin>:<skill>` tags. Process plugins (release-ops, git-workflow) intentionally keep discrete-event skills with no hook.

### Changed

- **`ceh-architecture-design`** (MINOR) — scoped to backend: removed the asyncpg transaction/pool code (now sole-owned by `ceh-python-backend:asyncpg`) and the frontend structure (now in `ceh-typescript-frontend:sveltekit`); added an `adr` storage convention; standardized PostgreSQL on `entity_*` vocabulary.
- **`ceh-typescript-frontend`** (MINOR) — modernized all skill examples to Svelte 5 runes (`$props`, `$state`, `$derived`, `onclick`); `bun.lockb` → `bun.lock`.
- **`ceh-agent-coding-contract`** (PATCH) — clarified the authority hierarchy (an in-session user instruction overrides the contract) and the authorization rule; made the Decision Log path overridable; added the `compact` hook event.
- **`ceh-python-backend`** (PATCH) — fastapi error handler now includes `correlation_id`; lifespan pool uses the standard sizing; synced the pip-audit command and coverage labels to the release-ops canonical.
- **`ceh-release-ops`** (PATCH) — rollback Decision Log path made overridable.
- **`ceh-git-workflow`** (PATCH) — synced open-pr's two checklist blocks and standardized the `docs/adr/DECISIONS.md` path.

---

## [2.7.2] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.1 |
| `ceh-architecture-design` | v2.1.2 |
| `ceh-blog` | v1.0.4 |
| `ceh-dev-tools` | v1.1.2 |
| `ceh-documentation` | v1.0.1 |
| `ceh-git-workflow` | v2.5.2 |
| `ceh-lessons-learned` | v2.0.3 |
| `ceh-python-backend` | v2.2.3 |
| `ceh-release-ops` | v2.2.4 |
| `ceh-summarize-chat` | v2.0.3 |
| `ceh-typescript-frontend` | v2.2.3 |

### Changed

- **All plugins** (PATCH) — standardized author metadata across every `plugin.json` and the marketplace manifest. Author is now `{ "name": "cheneeheng", "email": "eeheng.chen@gmail.com" }` (six manifests previously read `"Chen"` with no email); the marketplace `owner` gained the same email.

---

## [2.7.1] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-documentation` | v1.0.0 |
| `ceh-git-workflow` | v2.5.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.3 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Changed

- **`ceh-git-workflow`** (v2.5.1) — switched the PR merge policy from squash-merge to merge-commit. `main` now preserves every commit per PR (intentionally, as source material for write-ups/blog posts) via `gh pr merge --merge`; squash and rebase-merge are prohibited. Updated `open-pr` (Merge Strategy + PR-title note), `hotfix`, and the plugin README accordingly. Conventional Commits now applies per-commit, with a pre-merge branch-cleanup note.
- **`ceh-release-ops`** (v2.2.3) — mirrored the hotfix merge step in `incidents` (squash → merge commit) to stay consistent with the cross-referenced `ceh-git-workflow/hotfix` skill.

---

## [2.7.0] — 2026-06-04

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.4.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-documentation` | v1.0.0 |
| `ceh-git-workflow` | v2.5.0 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Added

- **`ceh-agent-coding-contract`** (v2.4.0) — the plugin now ships its own `SessionStart` hook (`hooks/hooks.json` → `hooks/load-contract.js`) that injects the mandatory directive to load the `agent-coding-contract` skill on the `startup` and `clear` events. Previously this lived in the user's global `~/.claude/settings.json`; bundling it makes contract auto-loading opt-in per project by simply enabling the plugin — no global hook configuration required.

---

## [2.6.0] — 2026-06-01

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.3.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-documentation` | v1.0.0 |
| `ceh-git-workflow` | v2.5.0 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Added

- **`ceh-documentation`** (v1.0.0) — new plugin for end-user and operator-facing documentation. Ships the `user-operator-guide` skill: task-oriented user guides and operator runbooks with strict audience separation, a no-invention/`[VERIFY]` rule, document-type selection, and single- or multi-file output rooted at `docs/guide/` with `index.md` as the entry point.

### Changed

- **`ceh-git-workflow`** (v2.5.0) — moved the `changelog-agent` and `readme-updater` agents (and the `check-semver.py` helper) into the new `ceh-documentation` plugin. Their invoke paths change from `/ceh-git-workflow:*` to `/ceh-documentation:*`.

---

## [2.5.1] — 2026-05-30

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.3.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.2 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.2 |

### Changed

- **`ceh-python-backend`** (v2.2.2) — wired the `python-testing` skill into all three tester agents via `skills:` frontmatter, and sharpened their descriptions to clarify when to delegate to an agent (many tests / broad coverage / isolated run) versus handle one or two tests inline. Dropped the duplicated Test Structure block from `python-unit-tester` now that the skill carries it.
- **`ceh-typescript-frontend`** (v2.2.2) — wired the `frontend-testing` skill into all three tester agents via `skills:` frontmatter and sharpened their delegation descriptions to match. Added a Vitest/Jest/Mocha runner-detection note to the `frontend-testing` skill.
- **Repo docs** — documented the plugin-agent frontmatter limitation (`permissionMode`, `hooks`, `mcpServers` ignored on plugin subagents) in `CLAUDE.md` and `README.md`, and re-synced `CROSS_REFERENCES.md` for definition-of-done checklist and coverage-target label drift.

---

## [2.5.0] — 2026-05-29

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.3.0 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Removed

- **`ceh-agent-coding-contract`** (v2.3.0) — deleted the `execution-modes` skill. Sessions are always autonomous in practice, making the separate interactive/autonomous mode switch redundant.

### Changed

- **`ceh-agent-coding-contract`** (v2.3.0) — folded autonomous-by-default behavior and the authority hierarchy into the `agent-coding-contract` skill: new Execution Mode section, "Ask, don't guess" reframed as "Decide, don't guess silently", and the Interactive/Autonomous parentheticals removed from the task workflow and decomposition rules. READMEs and plugin description updated accordingly.

---

## [2.4.3] — 2026-05-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.3 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.3 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Changed

- **`ceh-blog`** (v1.0.3) — sharpened all four skill `description` fields for reliable, disambiguated triggering: each now leads with what the skill does, states the discriminating input state (topic/repo → interviewer, raw notes → writer, written prose → editor, finished post → repurpose), keeps high-signal trigger phrases, and preserves inter-skill routing — while trimming redundant framing (~95 → ~75 words each) for tighter always-loaded token use.

---

## [2.4.2] — 2026-05-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.3 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.2 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Changed

- **`ceh-blog`** (v1.0.2) — rewrote all four skill `description` fields to use the directive "Trigger when…" pattern with explicit trigger phrases and "Do NOT trigger" exclusions; matches the `ceh-agent-coding-contract` style for unambiguous skill dispatch.

---

## [2.4.1] — 2026-05-25

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.3 |
| `ceh-architecture-design` | v2.1.1 |
| `ceh-blog` | v1.0.1 |
| `ceh-dev-tools` | v1.1.1 |
| `ceh-git-workflow` | v2.4.1 |
| `ceh-lessons-learned` | v2.0.2 |
| `ceh-python-backend` | v2.2.1 |
| `ceh-release-ops` | v2.2.2 |
| `ceh-summarize-chat` | v2.0.2 |
| `ceh-typescript-frontend` | v2.2.1 |

### Fixed

- **All plugins** — collapsed multiline `description` block scalars (`>`, `|`) to single-line inline strings in skill and agent frontmatter (56 files across all 10 plugins).
- **`ceh-blog`** — removed redundant `ceh-` prefix from skill `name` fields (`ceh-blog-editor` → `blog-editor`, etc.); the prefix is already carried by the plugin namespace.

---

## [2.4.0] — 2026-05-25

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.2 |
| `ceh-architecture-design` | v2.1.0 |
| `ceh-blog` | v1.0.0 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.4.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.2.0 |
| `ceh-release-ops` | v2.2.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.2.0 |

### Added

- **`ceh-blog` plugin (new, v1.0.0)** — interview-driven blog writing end-to-end:
  - `blog-interviewer`: structured interview skill to extract ideas, audience, and key points from the user.
  - `blog-writer`: drafts a full publication-ready blog post from interview output.
  - `blog-editor`: iterative editing pass — tone, clarity, and structure review.
  - `blog-repurpose`: repurposes a finished post for Twitter/X, LinkedIn, TL;DR, and newsletter formats.

### Changed

- **`ceh-agent-coding-contract`** (v2.2.2): Karpathy-derived rules added to the coding contract — opinionated heuristics on scope discipline, implementation order, and change minimalism.

---

## [2.3.0] — 2026-05-16

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.2.1 |
| `ceh-architecture-design` | v2.1.0 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.4.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.2.0 |
| `ceh-release-ops` | v2.2.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.2.0 |

### Added

- **`ceh-agent-coding-contract`** (v2.2.1): New `execution-modes` micro-skill extracted from references — covers interactive vs. autonomous mode rules and stop conditions.
- **`ceh-python-backend`** (v2.2.0): Four new micro-skills promoted from the former `python-backend` bundle:
  - `alembic`: Alembic migration setup, autogenerate, upgrade/downgrade workflow.
  - `asyncpg`: asyncpg query patterns, connection pool, and database reference (replaces `references/database.md`).
  - `python-environment`: uv environment setup, dependency management, and linting (ruff, mypy).
  - `python-observability`: structured logging, metrics, and health-check patterns.
  - `python-security`: secrets handling, CORS, rate limiting, and input validation.
- **`ceh-typescript-frontend`** (v2.2.0): New `environment` micro-skill covering Bun/Node setup, Vite config, and toolchain commands — extracted from the former `typescript-frontend` bundle.
- **Repo**: `scripts/sync-stubs.ps1` added — synchronises cross-plugin stub reference files in one pass.
- **Repo**: `CROSS_REFERENCES.md` added — tracks content duplicated across skills with canonical source and all copy locations.

### Changed

- **`ceh-agent-coding-contract`** (v2.2.1): All reference files (`core-rules.md`, `decision-log.md`, `execution-modes.md`, `non-goals.md`, `stop-conditions.md`, `task-workflow.md`) inlined into `agent-coding-contract/SKILL.md`; reference files removed. `implement-from-plan` and `review-against-plan` skills updated to inline their reference content.
- **`ceh-architecture-design`** (v2.1.0): Former `architecture-design` bundle skill and all its `references/` files removed. Content inlined into the existing micro-skills: `adr`, `domain-modeling`, `event-sourcing`, `llm-integration`, `postgresql`, `repository-structure`, `rest-api`.
- **`ceh-git-workflow`** (v2.4.0): Former `git-workflow` bundle skill and all its `references/` files removed. Content inlined into the existing micro-skills: `branch`, `code-review`, `commit`, `dependency-management`, `gitignore`, `hotfix`, `open-pr`, `release`. `merge` skill removed; merge strategy content consolidated into `open-pr`.
- **`ceh-python-backend`** (v2.2.0): Former `python-backend` bundle skill and all its `references/` files removed. Content distributed into `fastapi`, `python-testing`, and the four new micro-skills above. Agent descriptions trimmed (`python-integration-tester`, `python-system-tester`).
- **`ceh-release-ops`** (v2.2.1): Former `release-ops` bundle skill and all its `references/` files removed. Content inlined into existing micro-skills: `database-migrations`, `definition-of-done`, `incidents`, `observability`, `rollback`, `security`, `versioning`. Lifecycle phase labels added to micro-skill descriptions.
- **`ceh-typescript-frontend`** (v2.2.0): Former `typescript-frontend` bundle skill and all its `references/` files removed. Content inlined into existing micro-skills: `accessibility`, `coding-style`, `frontend-testing`, `linting`, `sveltekit`, plus new `environment`.
- **`ceh-git-workflow`** (v2.4.0): `readme-updater` agent — `maxTurns` tuned; `effort` field removed.
- **Repo**: `CLAUDE.md` updated — bundle/micro-skill distinction removed; versioning and plugin table updated to reflect new structure.
- **Repo**: All plugin `README.md` files updated to reflect bundle removal and current skill lists.
- **Repo**: `ceh-dev-tools/CHANGELOG.md` removed (stale, not maintained).

---

## [2.2.3] — 2026-05-14

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.1.2 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.3 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Added

- **`ceh-git-workflow`** (v2.2.3): Attribution footer guidance added to commit (`commits.md`) and PR (`pull-requests.md`) standards. Test-run delegation rule added to `task-workflow.md` — test execution should be handed off to background subagents (auto-triggered tester agents take precedence; `Agent(run_in_background=True)` as fallback).
- **Repo**: `LICENSE.md` added.

### Changed

- **`ceh-git-workflow`** (v2.2.3): `branch` skill inlines start-new-work commands, dropping the `workflows.md` pointer (~135 lines/invocation saved).
- **`ceh-agent-coding-contract`** (v2.1.2): `agent-coding-contract` skill trigger narrowed to explicit phrases only, removing broad auto-load on refactors and multi-file changes. `review-against-plan` skill drops §01/§03 audit rows and tightens wording (~10 lines/run saved).
- **Repo**: `CLAUDE.md` updated — "Adding an Agent" section added parallel to "Adding a Skill"; `ceh-dev-tools` flagged as agents-only in the Plugins table; cross-bundle stub check command narrowed to `skills/python-backend` path; versioning rules clarified (PATCH for updates, MINOR for new skills/agents).

---

## [2.2.2] — 2026-05-02

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.1.0 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.1 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Added

- **`ceh-agent-coding-contract`** (v2.1.0): Two new bundle skills for plan-driven development:
  - `implement-from-plan`: implements a SKELETON.md or ITER_NN.md planning document section by section, resolving iteration pointers and respecting scope boundaries.
  - `review-against-plan`: audits the codebase against a planning document, categorizes findings as Gap / Deviation / Error, fixes them in-line, and produces a Plan Compliance Report.
  - `plan-schema.md` reference: defines SKELETON and ITER frontmatter, section table (§01–§06), pointer rules, and resolution order.

---

## [2.2.1] — 2026-04-29

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.2 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.1 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.2 |
| `ceh-release-ops` | v2.1.2 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.2 |

### Changed

- **`ceh-agent-coding-contract`** (v2.0.2): Added built-in tool guidance across reference files — `AskUserQuestion` in `core-rules.md` (ask-don't-guess rule), `execution-modes.md` (Interactive Mode stop), and `stop-conditions.md`; `TaskCreate`/`TaskUpdate` and `Agent` tool in `task-workflow.md` for subtask tracking and parallel execution.

- **`ceh-git-workflow`** (v2.2.1): Added tool guidance — `Read`/`Grep`/`Bash` for code inspection in `code-review.md`; `Bash` with `git diff main...HEAD` in `pull-requests.md` author self-review checklist; `Bash` for audit commands in `dependencies.md`.

- **`ceh-python-backend`** (v2.1.2): Added `Bash` tool notes to `environment.md` (command table), `linting.md` (pre-PR checks), `migrations.md` (alembic workflow), `testing.md` (coverage run), and `security.md` (`pip-audit`).

- **`ceh-typescript-frontend`** (v2.1.2): Added `Bash` tool notes to `environment.md` (command table) and `linting.md` (pre-PR checks).

- **`ceh-release-ops`** (v2.1.2): Added `Bash` tool notes to `migrations.md` (alembic commands), `versioning.md` (release checklist), `security.md` (audit commands), and `rollback.md` (rollback procedure).

### Fixed

- Removed stale `docs/claude_logs/LESSONS_LEARNED.md` session log.

---

## [2.2.0] — 2026-04-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.1 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.1.0 |
| `ceh-git-workflow` | v2.2.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.1 |
| `ceh-release-ops` | v2.1.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.1 |

### Changed

- **`ceh-dev-tools`** (v1.1.0):
  - `repo-tree-mapper` agent: defaults to running in background.

- **`ceh-git-workflow`** (v2.2.0):
  - `changelog-agent` agent: defaults to running in background.
  - `readme-updater` agent: defaults to running in background.

---

## [2.1.1] — 2026-04-26

### Fixed

- Added full list of agents to the readme.

---

## [2.1.0] — 2026-04-26

### Plugin versions

| Plugin | Version |
|--------|---------|
| `ceh-agent-coding-contract` | v2.0.1 |
| `ceh-architecture-design` | v2.0.1 |
| `ceh-dev-tools` | v1.0.1 |
| `ceh-git-workflow` | v2.1.0 |
| `ceh-lessons-learned` | v2.0.1 |
| `ceh-python-backend` | v2.1.1 |
| `ceh-release-ops` | v2.1.1 |
| `ceh-summarize-chat` | v2.0.1 |
| `ceh-typescript-frontend` | v2.1.1 |

### Added

- **`ceh-dev-tools` plugin (new, v1.0.1)** — developer productivity agents:
  - `repo-tree-mapper` agent: walks a repo and produces an annotated `REPO_MAP.md`; trimmed description ~50%, `maxTurns` 25 → 8.
  - `walk-repo.sh` script: git-aware directory walker (fixed non-portable `$skip && continue` → `[[ $skip == true ]] && continue`).
  - Registered in top-level `README.md`, `CLAUDE.md`, and `marketplace.json`.

- **`ceh-git-workflow`** (v2.1.0) — new agents and scripts:
  - `changelog-agent`: generates or updates `CHANGELOG.md` (Keep a Changelog + semver).
  - `readme-updater`: applies surgical README edits after feature changes.
  - `check-semver.py` script: validates all version headers in a changelog file.

- **`ceh-python-backend`** (v2.1.1) — new agents, scripts, and references:
  - `python-unit-tester`, `python-integration-tester`, `python-system-tester` agents.
  - `run-unit-tests.sh`, `run-integration-tests.sh`, `run-system-tests.sh` scripts (use `uv run pytest`).
  - `references/migrations.md`: Alembic setup, autogenerate, upgrade/downgrade, test DB management.

- **`ceh-typescript-frontend`** (v2.1.1) — new agents, scripts, and micro-skills:
  - `ts-unit-tester`, `ts-integration-tester`, `ts-system-tester` agents.
  - `detect-test-framework.sh`, `run-unit-tests.sh`, `run-integration-tests.sh`, `check-coverage.sh`, `run-e2e.sh` scripts.
  - `skills/linting/SKILL.md`: new micro-skill for ESLint/Prettier/svelte-check/tsc.
  - `skills/coding-style/SKILL.md`: new micro-skill for TypeScript type conventions and naming.
  - `references/accessibility.md`: expanded with ARIA patterns, focus management, keyboard nav, form labelling, and color contrast rules.

- **`ceh-release-ops`** (v2.1.1) — new agents, scripts, and micro-skills:
  - `github-actions`, `gitlab-ci` agents for creating, reviewing, and debugging CI pipelines.
  - `gh-detect-stack.sh`, `gh-scaffold.sh`, `gh-validate.sh`, `gh-analyze-failure.sh` scripts.
  - `gl-detect-stack.sh`, `gl-scaffold.sh`, `gl-validate.sh`, `gl-analyze-failure.sh` scripts.
  - `skills/versioning/SKILL.md`: micro-skill for version bumps and release tagging.
  - `skills/rollback/SKILL.md`: micro-skill for deployment health-check failures.

- **READMEs and CHANGELOGs** added to all plugins that were missing them (`ceh-agent-coding-contract`, `ceh-architecture-design`, `ceh-git-workflow`, `ceh-python-backend`, `ceh-release-ops`, `ceh-lessons-learned`, `ceh-summarize-chat`, `ceh-typescript-frontend`, `ceh-dev-tools`).

### Fixed

- **`ceh-agent-coding-contract`** (v2.0.1): merged `agent-role.md` into `core-rules.md`; updated `SKILL.md` to load all references (full contract, not selective).
- **`ceh-python-backend`**: `references/exceptions.md` — removed contradictory rule about route handlers converting domain exceptions; `references/coding-style.md` — replaced deprecated `asyncio.get_event_loop()` with `asyncio.get_running_loop()`; `references/security.md` — `uv run pip-audit` → `uvx pip-audit`; `references/testing.md` — added `system/` to test structure tree.
- **`ceh-typescript-frontend`**: `references/error-handling.md` — component example now uses `onSuccess` callback instead of writing `sessionStore` directly; removed `scripts/setup-test-db.sh` (Postgres setup does not belong in a frontend plugin).
- **`ceh-release-ops`**: `references/definition-of-done.md` — corrected core domain services coverage target from 90% → 95%, matching `ceh-python-backend/references/testing.md` and `ceh-git-workflow/references/ci.md`; trimmed `references/observability.md` (removed redundant bad-example block); synced `skills/python-backend/references/observability.md` stub.
- **`ceh-git-workflow`**: `references/workflows.md` — added `git push origin --delete <branch-name>` to the "After PR is merged" sequence.

### Changed

- Token optimizations across reference files (no content removed): `ceh-summarize-chat/SKILL.md`, `ceh-lessons-learned/SKILL.md`, `ceh-architecture-design/references/domain-modeling.md`, `ceh-architecture-design/references/postgresql.md`, `ceh-python-backend/references/database.md`, `ceh-release-ops/references/observability.md`, `ceh-python-backend/references/coding-style.md`, `ceh-python-backend/references/testing.md`; both database stubs kept in sync.

---

## [2.0.0] — 2026-04-08 (all plugins)

### Changed

- **Breaking**: split the monolithic `ceh` plugin into 8 standalone plugins, one per domain:
  `ceh-agent-coding-contract`, `ceh-architecture-design`, `ceh-python-backend`,
  `ceh-typescript-frontend`, `ceh-git-workflow`, `ceh-release-ops`,
  `ceh-summarize-chat`, `ceh-lessons-learned`.
- Each bundle skill and its associated micro-skills now live in the same plugin. Skill invoke
  prefixes changed from `ceh:*` to `ceh-<plugin>:*` (e.g. `ceh:commit` → `ceh-git-workflow:commit`).
- Cross-bundle micro-skills (`postgresql`, `observability`, `security`) retain identical relative
  reference paths; foreign reference files are duplicated into the host plugin where needed.
- `marketplace.json` updated to list all 8 plugins; old `ceh` entry removed.

---

## [1.0.5] — 2026-04-06

### Fixed

- `lessons-learned` skill: clarified append instruction to always add new entries at the very end of `LESSONS_LEARNED.md`, never before the last existing entry.

---

## [1.0.4] — 2026-04-05

### Changed

- Standardised all Claude-generated log file paths to `docs/claude_logs/`: `LESSONS_LEARNED.md`, `DECISION_LOG.md` (referenced across `lessons-learned`, `agent-coding-contract`, `git-workflow`, and `release-ops` skills).
- Moved `ARCHITECTURE_DECISIONS.md` references out of `docs/claude_logs/` to `docs/adr/DECISIONS.md` — this file is shared developer documentation, not a Claude session artifact (`git-workflow/references/code-review.md`, `architecture-design/references/rest-api.md`).

---

## [1.0.3] — 2026-04-03

### Added

7 micro-skills extracted from `git-workflow` for fine-grained auto-triggering on individual
git operations.

| Micro-skill | Sources | Auto-triggers when |
|---|---|---|
| `branch` | git-workflow/branching + workflows | Creating or naming a branch |
| `commit` | git-workflow/commits + workflows | Writing a commit message or staging changes |
| `open-pr` | git-workflow/pull-requests + workflows | Opening a pull request or writing a PR description |
| `merge` | git-workflow/merging | Merging a branch or choosing a merge strategy |
| `hotfix` | git-workflow/workflows + releases | Executing a critical production fix |
| `release` | git-workflow/releases + workflows | Tagging a release or bumping a version |
| `gitignore` | git-workflow/gitignore | Creating or editing a `.gitignore` file |

---

## [1.0.2] — 2026-04-01

### Added

18 micro-skills for precise auto-triggering. Each is a thin skill that points to the relevant
reference file(s) already defined in the bundle skills — no content duplication.

| Micro-skill | Sources | Auto-triggers when |
|---|---|---|
| `adr` | architecture-design/adrs | Making significant design decisions |
| `domain-modeling` | architecture-design/domain-modeling | Designing entities, IDs, status fields |
| `event-sourcing` | architecture-design/event-sourcing | Working with event log or state snapshots |
| `rest-api` | architecture-design/rest-api | Building endpoints, choosing HTTP codes |
| `postgresql` | architecture-design/postgresql + python-backend/database | Writing SQL, asyncpg queries, schema changes |
| `llm-integration` | architecture-design/llm-integration | Integrating LLM calls or handling output |
| `fastapi` | python-backend/fastapi + python-backend/exceptions | Writing route handlers, DI, exception hierarchy |
| `python-testing` | python-backend/testing | Writing Python tests |
| `sveltekit` | typescript-frontend/sveltekit + typescript-frontend/error-handling | Routes, stores, components, API client |
| `frontend-testing` | typescript-frontend/testing | Writing frontend tests |
| `accessibility` | typescript-frontend/accessibility | Writing Svelte component markup |
| `observability` | python-backend/observability + release-ops/observability | Logging, metrics, health checks |
| `database-migrations` | release-ops/migrations | Writing or running Alembic migrations |
| `incidents` | release-ops/incidents + release-ops/hotfix | Production incidents, post-mortems |
| `definition-of-done` | release-ops/definition-of-done | Preparing to open a PR |
| `security` | python-backend/security + release-ops/security | Secrets, CORS, rate limiting, input validation |
| `code-review` | git-workflow/code-review | Reviewing PRs, leaving review comments |
| `dependency-management` | git-workflow/dependencies | Adding or upgrading packages |

---

## [1.0.1] — 2026-04-01

### Changed

- Refactored `agent-coding-contract`, `architecture-design`, `python-backend`, `typescript-frontend`, and `release-ops` skills: replaced long, keyword-stuffed `SKILL.md` titles with a short title and a summary paragraph, and moved all detailed content into topic-specific files under a `references/` folder — matching the pattern established by `git-workflow`.
- Updated `summarize-chat` skill: replaced the verbose title with a short title and summary paragraph (no reference files needed).

### Reference files added

| Skill | New reference files |
|-------|-------------------|
| `agent-coding-contract` | agent-role, core-rules, decision-log, execution-modes, non-goals, stop-conditions, task-workflow |
| `architecture-design` | adrs, domain-modeling, event-sourcing, llm-integration, postgresql, repository-structure, rest-api |
| `python-backend` | coding-style, database, environment, exceptions, fastapi, linting, observability, security, testing |
| `release-ops` | definition-of-done, hotfix, incidents, migrations, observability, rollback, security, versioning |
| `typescript-frontend` | accessibility, coding-style, environment, error-handling, linting, sveltekit, testing |

---

## [1.0.0] — 2026-03-31

### Added

- Initial release of the `ceh` plugin.
- Skills: `agent-coding-contract`, `architecture-design`, `git-workflow`, `lessons-learned`, `python-backend`, `release-ops`, `summarize-chat`, `typescript-frontend`.
- `git-workflow` ships with reference files: branching, ci, code-review, commits, dependencies, gitignore, merging, pull-requests, releases, workflows.
- `LESSONS_LEARNED.md` for capturing session retrospectives.
- `marketplace.json` for plugin discovery.
