# ceh-agent-coding-contract

A behavioral contract for coding agents: the rules that govern how an agent operates during a
session — what it may change, when it must stop, and how it logs decisions. The plugin loads the
contract automatically at session start, alongside the `write-less-code` minimalism skill.

> The plan-driven workflow skills (`implement-from-plan`, `review-against-plan`) moved to the
> `ceh-plan-build-review` plugin, which bundles them with the planning skills.

## Skills

| Skill | When it loads | What it does |
|-------|---------------|--------------|
| `agent-coding-contract` | Every coding session (auto, via hook) | The full behavioral contract — role, core rules, five-step workflow, stop conditions, decision logging. |
| `write-less-code` | Every coding session (auto, via hook) | The minimalism reflex — the ladder (YAGNI → stdlib → native → installed dep → one line), native-platform-first, the `// less-code:` shortcut convention. The positive half of the contract's minimal-change rules. |
| `shrink-diff` | On demand — when a feature branch is functionally done and its diff should get smaller before review | Retroactive minimalism — applies the write-less-code standard to the accumulated diff vs `main`, across all the commits and sessions that produced it: dedupe against existing code, delete dead weight, collapse over-built structure. Diff-scoped, with three narrow causes for touching unchanged code. |
| `refactor-repo` | Manual only (`/refactor-repo`) — never auto-fires | Whole-codebase (or per-module) refactor campaign: read-only inventory, ranked proposal with payoff/risk/diff-size estimates, then apply only user-approved clusters on `refactor/` branches under a behavior-preservation gate. |
| `usage-limit-handoff` | When the usage-limit guard hook fires (5h or weekly window past threshold) | Stop-and-summarize protocol: close the current atomic step, start nothing new, write a durable handoff artifact to `.agents_workspace/handoff/` plus a line in the global `~/.claude/handoff/index.md`, end the turn. Subagents report upward instead of writing the artifact. |
| `explain-until-understood` | Manual only (`/explain-until-understood`) — never auto-fires | How an explanation is built and what to do when it misses: assume the reader knows nothing about the subject and say what floor you are building from, read the real code (never a design doc), foundations before the specific case, plain language (concept before name, every term of art defined at first use), verified output over described output, ASCII for structure and time, close on a transferable rule plus a self-test. Ships the escalation ladder — prose → steps → pictures → foundations — with the rule that a miss at pictures means a skipped foundation, not a missing detail; a reader lost on a *word* is not on the ladder at all. Writes no files by default — `.agents_workspace/` scratch notes on request, and one narrow repo path for a subsystem explainer no other skill owns. |

**Manual triggers**

- `agent-coding-contract` — `/agent-coding-contract`, or say `"load the contract"` / `"agent contract"` / `"coding contract"`.
- `write-less-code` — `/write-less-code`, or say `"write less code"` / `"be lazy"` / `"simplest solution"` / `"yagni"`.
- `shrink-diff` — `/shrink-diff`, or say `"shrink the diff"` / `"consolidate the branch"` / `"can this diff be smaller"`.
- `refactor-repo` — `/refactor-repo` only (model auto-invocation is disabled by design).
- `usage-limit-handoff` — `/usage-limit-handoff`, or say `"wrap up the session"` / `"usage limit handoff"` / `"stop and summarize"`.
- `explain-until-understood` — `/explain-until-understood [what to explain]` only (model auto-invocation is disabled by design).

## How the skills auto-load

The plugin ships hooks (`hooks/hooks.json`) that activate automatically when the plugin is enabled —
no global `settings.json` change or env var required.

**At session start** — a `SessionStart` hook (`hooks/load-contract.sh`) injects a **mandatory**
directive to load `agent-coding-contract` before any other action, firing on `startup`, `resume`,
`clear`, and `compact` (so a fresh, resumed, or reset session has it loaded, and it is re-injected
after compaction).

**Every turn** — a `UserPromptSubmit` hook (`hooks/less-code-payload.sh`) re-injects a compact digest
of the `write-less-code` ladder before each prompt. This carries the minimalism reflex on every turn,
reliably from turn one; the full `write-less-code` skill loads on demand when non-trivial code is
actually being written.

**Every tool call** — a `PostToolUse` hook (`hooks/usage-limit-watch.py`) samples the account-wide
rate-limit percentage, taking whichever window is closest to its cap (the 5-hour and weekly windows
both count). When it crosses `CEH_USAGE_LIMIT_THRESHOLD` (default 90%), the hook tells the agent to
stop starting new work and run `usage-limit-handoff`; if ignored, it re-fires every 5 further
points of usage.

The reading is account-wide — claude.ai web, desktop, mobile and Claude Code draw from one pool —
and refreshes on every API round-trip, so sampling per tool call is fresh enough to stop
preemptively rather than after a 429. The hook reads the newest record across *all* sessions and
projects, so a second Claude Code window does not leave a session acting on a stale number. Inside
a subagent it tells the subagent to stop and report upward instead of writing an artifact, since a
subagent sees only its own slice of the work.

> **Prerequisite for the usage-limit guard:** the hook reads the rate-limit data that a statusline
> export writes to `~/.claude/statusline/<project-dir>/<session_id>.jsonl` — a statusline script
> that appends its stdin JSON there (each line `{"session_id", "ts", "data": <payload>}`, with
> `:` and path separators in the project dir name replaced by `-`). Claude Code itself provides
> `rate_limits` only to the statusline, not to hooks, hence the relay. Without the export the guard
> warns once per session that it is inactive, rather than failing silently — everything else in the
> plugin works unchanged. Readings older than `CEH_USAGE_STALE_MINUTES` (default 15) are treated as
> unknown for the same reason: a stale low number reads as safety that is not there. A window whose
> `resets_at` has already passed is skipped regardless of the record's age — the reading predates
> the reset, so a high number there describes a window that no longer exists.
>
> The hook needs `python3` on PATH (stdlib only, no packages), which is what makes it behave the
> same on Linux, macOS, and Windows; it replaced a bash+`jq` version that needed a POSIX shell and
> a `jq` binary Windows does not ship. It is advisory, so it fails open: on error it prints one
> line to stderr and exits 1 (visible warning, nothing blocked).

## What the contract enforces

The `agent-coding-contract` skill is the single source of truth. In short, it requires the agent to:

- **Run Autonomous Mode** — on routine ambiguity, decide the conservative option, log it, and
  continue; stop only for the hard cases (unresolvable conflicts, repo state contradicting
  instructions, risk of data loss, inconsistent partial failure).
- **Follow the five-step workflow** — Understand → Confirm scope → Apply changes → Validate →
  Summarize. Quick checks scoped to the edit are always allowed; test suites, builds, and
  state-changing commands run only when explicitly requested.
- **Make minimal, authorized changes** — localized diffs, no unsolicited refactors, touch only what
  is in scope, never claim work was done that wasn't.
- **Log decisions made under ambiguity** to `.agents_workspace/DECISION_LOG.md` (default path;
  override it via your project `CLAUDE.md`). See the skill for the entry format and when to log.

Refer to the skill for the authoritative wording — this section is a summary and is not the contract
itself.
