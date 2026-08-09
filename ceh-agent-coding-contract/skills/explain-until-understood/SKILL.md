---
name: explain-until-understood
disable-model-invocation: true
description: >-
  Explain a subsystem, a design, or a set of changes to the person in the session until they can
  answer questions about it unaided: read the real code rather than a design doc, state the two to
  four primitives the explanation rests on before using them, verify claims by running them, draw
  structure and time in ASCII, show the tempting-but-wrong alternative, and close on a transferable
  rule plus a short self-test. Carries the escalation ladder for an explanation that missed — prose,
  then numbered steps, then pictures, then back to the primitives — on the rule that you change the
  representation rather than restate it louder. Writes no files. Not for implementing, fixing, or
  reviewing code, not for a repo-wide orientation file (use ceh-dev-tools:explain-codebase), and
  not for user-facing documentation (ceh-documentation).
argument-hint: '[what to explain]'
---

# Explain Until Understood

The target is a reader who can answer questions about the system **without the explanation in
front of them** — not a reader who followed along. Following along is the failure mode that feels
like success, on both sides.

The output is the conversation. This skill writes no files (see *Persisting* below).

## Not the same as

| Want | Use |
|------|-----|
| A repo-wide orientation file, component by component | `ceh-dev-tools:explain-codebase` |
| One line per path, fast structure map | `ceh-dev-tools:repo-tree-mapper` agent |
| Diagrams and decision records that live in the repo | `ceh-architecture:document-architecture` |
| Docs for people who *use* or *operate* the product | `ceh-documentation:user-operator-guide` |
| Someone in this session needs to understand something now | **this skill** |

## Procedure

1. **Read the real code first.** Never explain from memory, from a design doc, or from a summary —
   including a design doc you wrote yourself earlier in the session. Open the modules, read the
   docstrings, follow the call sites. A design doc says what the author decided; the code says
   what is true today.

2. **Establish foundations before the specific case.** Name the two to four primitives the whole
   explanation rests on, and state them plainly before using them. Writing "as you know", or
   reusing a term introduced earlier in the session, is the tell that a definition is missing.
   Skipping this step is the single most common cause of an explanation that has to be repeated.

3. **Verify by running.** Run the tool, the command, the throwaway script, and paste the real
   output. "semgrep found 2 hits, lines 22 and 23–27" beats "semgrep would flag the network call."
   Where you cannot run it, say so in the same breath as the claim.

4. **Draw structure and time; write everything else.** Prose is bad at nesting, ordering,
   before/after, and data flow — use a picture for those, a table or list for the rest. A diagram
   of a list is noise. In the conversation, draw in ASCII: it renders in a terminal, Mermaid does
   not. Mermaid is for a file that will be viewed rendered.

5. **Frame failure as "what you would wrongly conclude".** Not "this is a bug" but "you would read
   that as reconcile routing to verdict, and go debug the rule ladder — and the rule ladder is
   fine." The wrong conclusion is what makes a subtle failure memorable.

6. **Show the tempting-but-wrong alternative.** For any non-obvious design, name the simpler thing
   a reader would reach for and show precisely where it breaks. This is what turns "the code does
   X" into "the code *must* do X".

7. **Close with the transferable rule, then a self-test.** One sentence the reader can apply to
   the next case — "pass context explicitly wherever someone else's scheduler owns the task" beats
   re-listing the three call sites where it is passed. Follow it with two to five questions they
   should now be able to answer unaided. Their answers, or their silence, tell you whether step 2
   held.

## When it did not land

Do not restate the same explanation with more words. Drop a level and change the representation:

| Attempt | Representation | If it still misses |
|---|---|---|
| 1 | prose with code references | go to step-by-step |
| 2 | numbered steps, one idea each | go to pictures |
| 3 | one ASCII diagram per step | stop escalating — you skipped step 2 |
| 4 | define the primitives, then rebuild the explanation on them | ask which sentence broke |

A miss at attempt 3 is almost never a missing detail. It is a foundation the first three attempts
all assumed. Go back to step 2 rather than adding more pictures.

## Persisting the explanation

Explaining slides naturally into writing it down. Keep the boundary explicit:

- **Default: nothing is written.** The explanation is the reply.
- **Scratch notes** under `.agents_workspace/` are in scope when the user asks for something to
  re-read later.
- **Anything that lands in the repo** — `docs/`, README, architecture notes — is a different job.
  Hand off to the skill that owns it (see *Not the same as*) rather than writing it here.

## Honesty

The contract's honesty rules apply unchanged. One addition specific to explaining:

**"Not documented" and "I did not check" are different answers.** Grep before giving either, and
report which one you are giving. The same holds for "this path was never verified end to end" —
often the single most valuable line in the whole explanation.

## Rules

- **Evidence over inference.** Unclear purpose is written as "purpose unclear — checked imports and
  call sites, no references found", never guessed at. Never invent a responsibility.
- **Don't paste code.** A signature or a three-line snippet is the ceiling.
- **Describe what exists today**, not what was planned or is half-built.

## Anti-patterns

- Explaining from a design doc because it is well written. If the reader had understood the doc,
  they would not be asking.
- Reusing a term introduced earlier in the session as though it is now known.
- A diagram where a table would do; Mermaid where the reader has a terminal.
- Answering "is this documented?" with yes or no instead of a grep result per file.
- Ending on the mechanism instead of the rule of thumb.
- Restating attempt N as attempt N+1 with more words.
