# ceh-workflow-builder

Turn a repetitive multi-step task into something an agent runs, instead of
something you drive by hand every time.

The hard part is not writing a `SKILL.md` — three other tools do that. The hard
parts are deciding whether the task is one skill or a multi-step workflow, and
making the handoffs between steps explicit. A workflow whose steps pass data
with no declared shape fails the same way every time: a later step infers a
shape from whatever artifact it finds, infers it wrong, and the run keeps
producing garbage past a green gate.

Target runtime is **Claude Code**. The emitted artifact lands in the target
repo's `.claude/skills/`, so there is no install step.

## Skill

### `build-agentic-workflow`

Interviews the task, applies the one-skill-vs-workflow gate, decides per step
whether it becomes an existing skill, a script, inline prose, or its own step
skill, then emits the set leaf-first so every reference resolves as it is
written.

**Invoke:** `/ceh-workflow-builder:build-agentic-workflow`

**Auto-triggers on:** "turn this into a skill", "turn this into a workflow",
"build an agentic workflow", "automate this process", "make this repeatable",
"I do this by hand every time", or "I need a skill that calls other skills".

Covers the assumed-capability contract, the six-condition workflow gate, the
step-earns-a-skill test, data-contract schemas for non-adjacent handoffs
(step N to step N+m), the falsifiable-gate rule, and the two run directories.

## Directories

| | Variable | Default | Holds |
|---|---|---|---|
| Build time | `$CEH_WORKFLOW_BUILD_DIR` | `.agents_workspace/` | the interview spec while authoring |
| Run time | `$CEH_WORKFLOW_RUN_DIR` | `.agents_workspace/` | a generated workflow's step artifacts and run state |

Two variables on purpose. Building one workflow must not collide with running
another. Each run gets its own `<run-dir>/<name>/<run-id>/`, so a second run
never reads the first one's artifacts, and that directory is expected to be
git-ignored.

## Not this plugin

- Evaluating a skill that already exists — `ceh-evaluation:evaluate-skill`.
- Delegating one big task to subagents right now, without producing a reusable
  artifact — `ceh-orchestration:orchestrate`.
