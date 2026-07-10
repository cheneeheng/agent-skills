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

**Manual triggers**

- `agent-coding-contract` — `/agent-coding-contract`, or say `"load the contract"` / `"agent contract"` / `"coding contract"`.
- `write-less-code` — `/write-less-code`, or say `"write less code"` / `"be lazy"` / `"simplest solution"` / `"yagni"`.

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
