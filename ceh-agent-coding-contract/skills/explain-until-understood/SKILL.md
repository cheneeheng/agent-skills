---
name: explain-until-understood
disable-model-invocation: true
description: >-
  Explain a subsystem, a design, a set of changes, or an unfamiliar tool to the person in the
  session until they can answer questions about it unaided: read the real thing rather than a
  design doc or a changelog, state the two to four primitives the explanation rests on before using
  them, verify claims with read-only runs, draw structure and time in ASCII, show the
  tempting-but-wrong alternative, and close on a transferable rule plus a short self-test. Carries
  the escalation ladder for an explanation that missed — prose, then numbered steps, then pictures,
  then back to the primitives — on the rule that you change the representation rather than restate
  it louder. Writes no files by default. Not for implementing, fixing, or reviewing code, not for a
  repo-wide orientation file (use ceh-dev-tools:explain-codebase), and not for user-facing
  documentation (ceh-documentation).
argument-hint: '[what to explain]'
---

# Explain Until Understood

The target is a reader who can answer questions about the system **without the explanation in
front of them** — not a reader who followed along. Following along is the failure mode that feels
like success, on both sides.

The output is the conversation. By default this skill writes no files; the two exceptions are in
*Persisting* below.

**Scale to the ask.** "What does this regex do" earns a sentence, and at most the wrong-conclusion
framing from step 5. Step 1 is the one step that never scales away — the one-sentence answer is
only right because you opened the file. Everything else does: the full seven-step procedure is for
something the reader has to hold in their head afterwards — a subsystem, a design, a release's
worth of change. Running all seven on a one-line question is its own way of failing to explain.

## Not the same as

| Want | Use |
|------|-----|
| A repo-wide orientation file, component by component | `ceh-dev-tools:explain-codebase` |
| One line per path, fast structure map | `ceh-dev-tools:repo-tree-mapper` agent |
| Diagrams and decision records that live in the repo | `ceh-architecture:document-architecture` |
| Docs for people who *use* or *operate* the product | `ceh-documentation:user-operator-guide` |
| Someone in this session needs to understand something now | **this skill** |

## Procedure

Steps 1 and 3 are what *you* do. Steps 2 and 4–7 are what the *reply* contains, in that order. Do
not narrate the doing: "I read the modules and ran the validator" is process, and the reader asked
for an explanation.

1. **Read the real thing first.** Never explain from memory, from a design doc, or from a summary —
   including a design doc you wrote yourself earlier in the session. What "the real thing" is
   follows the ask: for repo code, open the modules, read the docstrings, follow the call sites;
   for "what changed since `<tag>`", the diff — commit messages after it and labelled as claimed
   intent, never the changelog; for an unfamiliar tool, its own `--help` plus one run against a
   real fixture. A design doc says what the author decided; the source says what is true today.

2. **Establish foundations before the specific case.** Name the two to four primitives the whole
   explanation rests on, and state them plainly before using them. Writing "as you know", or
   reusing a term introduced earlier in the session, is the tell that a definition is missing.
   Skipping this step is the single most common cause of an explanation that has to be repeated.

3. **Verify by running.** Run the tool, the command, the throwaway script, and paste the real
   output. "semgrep found 2 hits, lines 22 and 23–27" beats "semgrep would flag the network call."
   Read-only runs only — a command that changes state is not an illustration, and the contract
   requires it be requested first. Where you cannot or may not run it, say so in the same breath as
   the claim.

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

Do not restate the same explanation with more words. Drop a level and change the representation.
Only the representation changes: a re-explanation still closes on step 7's rule and self-test,
because the self-test is how you find out whether the new form landed.

Locate yourself on the ladder by the **form of the last attempt**, not by how many messages have
passed — invoked cold after a miss, look at what the previous explanation actually was and take the
next row down. A table is attempt 1, not attempt 3: it lays out facts side by side but carries no
structure, ordering, or flow, so a reader stuck on *how the parts connect* gains nothing from one.

| Attempt | Representation | If it still misses |
|---|---|---|
| 1 | prose, tables, and code references | go to step-by-step |
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
- **One case has no owner:** a developer-facing explainer of a single subsystem, written into
  `docs/`. It is neither a whole-repo orientation file, nor product documentation, nor a decision
  record. Say that plainly instead of forcing a fit — `ceh-architecture:document-architecture` is
  the nearest, and it will reshape the material into diagrams plus Key Decisions rather than
  preserve the explanation you just gave. Having named the gap, write the file yourself if the user
  still wants it, keeping the explanation's shape. This is the one repo path this skill may write.

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
