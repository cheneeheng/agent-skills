---
name: build-agentic-workflow
description: >-
  Load this skill to turn a repetitive multi-step task into something an agent runs instead of
  something a human drives by hand: interview the task, decide whether it is one skill or a gated
  multi-step workflow, and emit the artifact into the target repo's `.claude/skills/`. Trigger on
  "turn this into a skill", "turn this into a workflow", "build an agentic workflow", "automate this
  process", "make this repeatable", "I do this by hand every time", "wrap these steps into something
  the agent can run", or "I need a skill that calls other skills". Covers the one-skill-vs-workflow
  gate, the pipeline + gate table, per-step data-contract schemas for handoffs, and leaf-first
  emission. Not for evaluating a skill that already exists (use ceh-evaluation:evaluate-skill), not
  for adding a component to this plugin repo, and not for running a workflow that has already been
  built.
---

# Build an Agentic Workflow

Interview a fuzzy, repetitive task into a runnable artifact. Two possible outputs, and choosing
between them is the main decision this skill makes:

- **One skill** — the default. A single `SKILL.md` the agent loads and follows.
- **A workflow** — a flow skill that owns *ordering and gates only*, plus the step skills, scripts,
  and handoff schemas it delegates to.

Target runtime is **Claude Code**. Other agent runtimes are out of scope; do not water the output
down for portability.

## Assumed capabilities

The emitted artifact may rely on these and nothing else. State in the artifact which ones it uses.

| Capability | Tool | Watch out |
|---|---|---|
| Read, write, edit files | `Read` / `Write` / `Edit` | — |
| Run commands | `Bash` | Any CLI a step invokes belongs in the artifact's `compatibility` |
| Search | `Glob` / `Grep` | — |
| Call another skill | `Skill` | Target must exist and be model-invocable |
| Give a step its own context window | `Agent` | A subagent cannot see the caller's transcript |
| Ask the user | `AskUserQuestion` | Stripped from every subagent — a delegated step can never ask |

## Directories

Two directories, two variables, two lifetimes. Do not conflate them.

| | Variable | Default | Holds |
|---|---|---|---|
| Build time | `$CEH_WORKFLOW_BUILD_DIR` | `.agents_workspace/` | this skill's interview spec and notes |
| Run time | `$CEH_WORKFLOW_RUN_DIR` | `.agents_workspace/` | the generated workflow's step artifacts and run state |

Both default to the same place, so both namespace by name: the interview spec is
`<build-dir>/<name>-workflow-spec.md` and run-time paths are `<run-dir>/<flow-name>/`. Use a
provisional slug for the spec until the name is settled, then rename it — otherwise building a second
workflow overwrites the first one's spec.

The generated flow **names the run-time variable and its default in its own body** — the agent that
runs it is not the agent that built it and has none of this context.

Run artifacts are never committed. Before finishing, check the target repo actually ignores the run
directory and append it to `.gitignore` if it does not; stating the requirement in prose is not the
same as meeting it.

## Phase 1 — Interview

Write the answers to `<build-dir>/<name>-workflow-spec.md` as you go. Batch enumerable choices
through `AskUserQuestion`; ask the open-ended ones plainly. Do not start designing until every
question has an answer.

1. **The moment.** What happens right before you would want this to run? This becomes the trigger,
   and it must be a verb. If the answer is a topic rather than a moment, the artifact will never
   auto-fire and the interview is not done.
2. **The manual procedure.** Walk it step by step in the order you actually do it.
3. **Preconditions and proof.** Per step: what has to be true before it starts, and how do you know
   it worked? An answer you cannot check is not a gate.
4. **Data flow.** Per step: what does it read, what does it leave behind, and which *later* step
   reads that? Name the producing step, not just the artifact.
5. **Tooling.** Which CLIs, credentials, services, or network access does each step need?
6. **Done.** What is true at the end that was not true at the start?
7. **Interruption.** Does this run in one sitting, or can it stop partway and need resuming?

## Phase 2 — One skill or a workflow

**Default to one skill.** Emit a workflow only if at least one of these holds:

1. A step has a gate that can fail and must block the next step.
2. Steps need different tools or permissions.
3. A step is big enough to deserve its own context window.
4. The run must survive interruption and resume.
5. A step is already owned by an existing skill worth delegating to.
6. One step's output is another step's input — the handoff needs a declared contract.

"It has several paragraphs" is not a reason. If none hold, write one skill and stop here.

## Phase 3 — What each step becomes

Decide per step, in this order — stop at the first that fits:

| Becomes | When |
|---|---|
| An existing skill | Something already owns this step. Delegate to it |
| A script | The step is mechanical and deterministic |
| Its own step skill | The step is independently triggerable, or needs its own context window |
| Inline prose in the flow | Nothing above fits — the default |

**A step earns its own skill only on the third row.** A step that only ever runs inside one flow,
and fits in the flow's own context, is inline prose or a script. Three skills beat six: every skill
added to `.claude/skills/` competes for auto-triggering in the target repo, and `.claude/skills/` is
flat, so a generated set is grouped only by naming — flow `<name>-flow`, steps `<name>-<step>`.

**Nesting is capped at one level.** A workflow's steps may be skills; a step skill may not itself be
a workflow.

**A step skill cannot be hidden.** `disable-model-invocation: true` would block the flow's own call
to it. Instead, its `description` must name the owning flow and route away from direct use.

## Phase 4 — Data contracts

The failure this prevents: a later step gets no declared shape, infers one from whatever artifact it
finds, infers it wrong, and the run keeps producing garbage past a green gate.

**When a schema is required.** Whenever a step's output is read by *any* later step — N+m, not just
N+1 — and one artifact may have several consumers. A step that produces nothing, or a terminal
artifact nobody downstream reads, gets no schema.

- **Handoff is always a file.** Never conversation state: a delegated step cannot see the caller's
  transcript, and compaction drops anything held only in context.
- **Artifacts live for the whole run.** Nothing is cleaned up at a step boundary; the consumer may be
  four steps away.
- **One writer, many readers.** The schema belongs to the producing step. Every consumer points at
  the one schema file rather than restating its fields, or the contract drifts between them.
- **Preconditions are checked twice.** The producer's gate proves the artifact was valid when
  written; each consumer re-asserts it exists before reading, since intervening steps can fail.

**Where it lives.** `.claude/skills/<name>-flow/references/<artifact>-schema.md`. Form is a Markdown
doc: required fields, optional fields, one complete worked example, and the list of consuming steps.
Reach for JSON Schema and a validator only when the artifact is genuinely JSON and that step already
runs a script — never add a dependency for this.

**Schemas make gates falsifiable.** Replace "the plan is complete" with "`<run-dir>/<flow>/plan.md`
exists and carries every required field in `plan-schema.md`". Phrase gates that way wherever a schema
exists.

## Phase 5 — Emit

Leaf-first, so every reference resolves the moment it is written:

1. Schema docs → `references/`
2. Scripts → `scripts/`
3. Step skills → `.claude/skills/<name>-<step>/SKILL.md`
4. The flow skill → `.claude/skills/<name>-flow/SKILL.md`

Then run both checks:

- **Resolution.** A generated step skill must have a directory that now exists under
  `.claude/skills/`. A pre-existing skill delegated to is a different check: it must be installed in
  the session and model-invocable, since a call to a skill with `disable-model-invocation: true`
  fails silently.
- **Dependency.** Every `Reads` entry names an artifact some *earlier* step `Writes`. This is the
  likeliest generation bug once handoffs stop being adjacent.

Default destination is `.claude/skills/` in the target repo — no install step, picked up immediately.
Offer plugin packaging only when the user says the workflow is shared across repos.

## The flow skill template

```markdown
---
name: <name>-flow
description: >-
  <The moment, as a verb.> Trigger on "<phrase>", "<phrase>". This skill owns only the ordering and
  the gates; each step is delegated to the skill or script that owns it. Not for <nearest
  neighbour>, use <that> instead.
compatibility: >-
  <Only if a step needs a CLI, service, credential, or network. Name the tool, its minimum version,
  and what fails without it.>
---

# <Name> Flow

<One paragraph: the pipeline as an arrow chain, and what this adds over running the steps ad hoc.>

Run state and step artifacts live in `$CEH_WORKFLOW_RUN_DIR/<name>/`, defaulting to
`.agents_workspace/<name>/`. That directory is git-ignored.

## Pipeline

Run top to bottom. Each step gates the next — do not proceed past a red gate.

| # | Step | Delegate to | Gate before next step |
|---|------|-------------|-----------------------|
| 1 | <what happens> | the Skill tool with `skill="<step-skill>"`, or `scripts/<x>.sh`, or "— inline" | <falsifiable condition> |

## Data contracts

| Step | Reads (from step) | Writes | Schema |
|---|---|---|---|
| 2 | `plan.md` (step 1) | `report.md` | `references/<artifact>-schema.md` |

<Omit this section entirely when no step reads another step's output.>
```

In the emitted flow, spell the delegation out as a literal instruction to invoke the Skill tool with
that skill name, and give the schema its real filename. The template above keeps the call in
backticks and the schema path as an angle-bracket placeholder on purpose: *this* repo's
`validate.py` resolves every literal skill invocation and every literal `references/…` path it
finds, so a concrete example here would fail the repo's own gate. Do not "fix" either one.

## The step skill template

```markdown
---
name: <name>-<step>
description: >-
  <The moment.> Called by `<name>-flow` as step N; not for direct use outside that flow.
---

# <Name>: <Step>

Reads `<artifact>` at `$CEH_WORKFLOW_RUN_DIR/<name>/<file>` per `<schema>`; writes `<artifact>` to
`<path>`. <Omit whichever half does not apply.>

<The step's actual instructions.>

## Done when

<The falsifiable condition the flow's gate checks.>
```

## Frontmatter rules for everything emitted

`description` is always a folded block scalar (`>-`), with a uniform 2-space indent and no blank
lines — it is the only style with no escaping burden for colons, quotes, or backslashes. The
description carries the trigger moment *and* negative routing to the nearest neighbour. Any other key
containing `: ` gets single quotes.

If `skill-creator` is installed in the session, use it for the mechanical `SKILL.md` authoring. It is
optional and this skill does not depend on it.

## Final checklist

- [ ] Trigger is a moment, not a topic.
- [ ] Workflow emitted only because a Phase 2 condition holds — otherwise one skill.
- [ ] Every step's gate is falsifiable, stated against a schema where one exists.
- [ ] Every cross-step handoff is a file under the run directory, with a schema.
- [ ] Every `Reads` has an earlier `Writes`.
- [ ] Every delegated skill exists and is model-invocable.
- [ ] No step skill survives that only ever runs inside the flow and needed no own context.
- [ ] `compatibility` present if and only if a step needs software the machine may lack.
- [ ] Run directory declared, defaulted, and actually present in the target repo's `.gitignore`.
