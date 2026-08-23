---
name: explain-until-understood
description: >-
  Explain a subsystem, design, diff, or unfamiliar tool to someone in the session until they can
  answer questions about it unaided — assuming they know nothing about the subject and stating the
  floor it builds from. Reads the real thing rather than a doc or changelog, defines the
  foundations before using them, verifies claims by running, draws structure and time in ASCII,
  shows the tempting-but-wrong alternative, closes on a transferable rule plus a self-test. Carries
  the escalation ladder for an explanation that missed — prose, steps, pictures, foundations — on
  the rule that you change the representation rather than restate it louder. Writes no files by
  default. Not for implementing, fixing, or reviewing code, a repo-wide orientation file
  (ceh-coding-agent:explain-codebase), or user-facing documentation (ceh-documentation).
argument-hint: '[what to explain]'
---

# Explain Until Understood

The target is a reader who can answer questions about the system **without the explanation in
front of them** — not a reader who followed along. Following along is the failure mode that feels
like success, on both sides.

The output is the conversation. By default this skill writes no files; the two exceptions are in
*Persisting* below.

## Who you are explaining to

**Assume the reader knows nothing about the subject.** Not that they are inexperienced — that they
have never seen this system, this tool, or this codebase, and do not know the words it uses. The
cost is asymmetric and that is the whole argument: explaining above someone burns a full round trip
and they may not say they are lost, while explaining below someone costs one paragraph they skim in
three seconds.

State the floor you are building from in one line before you start — "assuming you have written
Python but never used asyncio" — so the reader can raise it. Then build strictly upward from it.
The stated floor scales like everything else (see *Scale to the ask*): it belongs on anything
running the full procedure, and a one-sentence answer carries its floor implicitly. Spending half a
short answer on a preamble about what you assume is its own way of explaining badly.
Raise the floor only on evidence: they say so, or they ask a question that uses the vocabulary
correctly. Their job title is not evidence, that they are in a terminal is not evidence, and a term
they pasted from an error message is not evidence they know it.

**Scale to the ask.** "What does this regex do" earns a sentence, and at most the wrong-conclusion
framing from step 5. Step 1 is the one step that never scales away — the one-sentence answer is
only right because you opened the file. Everything else does: the full seven-step procedure is for
something the reader has to hold in their head afterwards — a subsystem, a design, a release's
worth of change. Running all seven on a one-line question is its own way of failing to explain.
The other end has a limit too: when the subject is larger than one explanation can carry, name the
slices, explain one, and say what the others are. A compressed tour of all of it leaves the reader
able to answer nothing.

## Not the same as

| Want | Use |
|------|-----|
| A repo-wide orientation file, component by component | `ceh-coding-agent:explain-codebase` |
| One line per path, fast structure map | `ceh-coding-agent:repo-tree-mapper` agent |
| Diagrams and decision records that live in the repo | `ceh-architecture:document-architecture` |
| Docs for people who *use* or *operate* the product | `ceh-documentation:user-operator-guide` |
| Someone in this session needs to understand something now | **this skill** |

## Procedure

Step 1 is what *you* do; steps 2 and 4–7 are what the *reply* contains, in that order. Step 3 is
both — you run the command, and its output goes in the reply next to the claim it supports. Do not
narrate the doing: "I read the modules and ran the validator" is process, and the reader asked for
an explanation. Pasted output is evidence, not narration.

1. **Read the real thing first.** Never explain from memory, from a design doc, or from a summary —
   including a design doc you wrote yourself earlier in the session. What "the real thing" is
   follows the ask: for repo code, open the modules, read the docstrings, follow the call sites;
   for "what changed since `<tag>`", the diff — commit messages after it and labelled as claimed
   intent, never the changelog; for an unfamiliar tool, its own `--help` plus one run against a
   real fixture — read-only, per step 3. A tool with no read-only run is read, not run: say so, and
   mark its behavior unverified. A design doc says what the author decided; the source says what is
   true today.
   The ban covers the *subject* only: a step 2 foundation may come from your own knowledge — say
   plainly that it does. If the subject itself has no artifact you can reach, say so before
   explaining anything, and mark every claim that follows as unverified. A subject that has no
   artifact to reach in the first place — a protocol, a general technique — is a different case:
   say once that it comes from knowledge, and do not label every line.

2. **Establish foundations before the specific case.** Name the two to four ideas the whole
   explanation rests on, and state each one plainly before you use it. Choose them for the reader's
   floor, not for the subject: the foundation you owe them usually sits one layer *below* where the
   subject's own documentation begins, because that documentation was written for someone who had
   already chosen to use the thing. The test for any term is whether a sharp person outside this
   field would know it — if not, it is either a foundation to state here or a word to replace.
   Writing "as you know", or reusing a term introduced earlier in the session, is the tell that a
   definition is missing. Needing more than four foundations means the subject is too big for one
   explanation: name the slices and explain one (see *Scale to the ask*).
   Everything after this step stands on these, so a foundation that missed makes the rest
   unreadable rather than partly readable — which is the single most common cause of an explanation
   that has to be repeated. You do not stop mid-reply to check: aim step 7's first self-test
   question at a foundation, which is where a missed one surfaces cheapest.

3. **Verify by running.** Run the tool, the command, the throwaway script, and paste the real
   output. "semgrep found 2 hits, lines 22 and 23–27" beats "semgrep would flag the network call."
   Read-only runs only — a command that changes state is not an illustration, and the contract
   requires it be requested first. Cheap, too: a throwaway snippet or one targeted command needs no
   permission, while a full test suite, a build, or a repo-wide lint stays contract-gated even
   though it changes nothing — ask for it, or cite output that already exists. Where you cannot or
   may not run it, say so in the same breath as the claim.

4. **Draw structure and time; write everything else.** Prose is bad at nesting, ordering,
   before/after, and data flow — use a picture for those, a table or list for the rest. A diagram
   of a list is noise. In the conversation, draw in ASCII: it renders on every surface, while
   Mermaid renders only where the reader's client draws it — a terminal does not. Mermaid is for a
   file that will be viewed rendered.

5. **Frame failure as "what you would wrongly conclude".** Not "this is a bug" but "you would read
   that as reconcile routing to verdict, and go debug the rule ladder — and the rule ladder is
   fine." The wrong conclusion is what makes a subtle failure memorable. The step frames a failure
   the code actually has — if reading it turned up none, say the path is straightforward and move
   on. An invented failure mode breaks the evidence rule.

6. **Show the tempting-but-wrong alternative.** For any non-obvious design, name the simpler thing
   a reader would reach for and show precisely where it breaks. This is what turns "the code does
   X" into "the code *must* do X".

7. **Close with the transferable rule, then a self-test.** One sentence the reader can apply to
   the next case — "pass context explicitly wherever someone else's scheduler owns the task" beats
   re-listing the three call sites where it is passed. Follow it with two to five questions they
   should now be able to answer unaided. A wrong answer is the miss signal — go to the ladder
   below, but re-explain only the idea that answer got wrong rather than the whole subject, and a
   wrong answer about a step 2 foundation goes straight to attempt 4. Silence is not a signal: it
   reads as "understood" as often as "lost", so end the turn rather than re-explain unprompted.

## Plain language

The register of the explanation is a choice, and the default drifts technical because the source
material is technical. Steer it deliberately.

- **Concept first, name second.** Say what the thing does, then attach its name: "the call hands
  the work off and returns before it finishes — that is what `async` means here." The reverse order
  lets the name stand in for the idea, and the reader nods at a word.
- **Define every term of art at first use, in the same sentence.** Not a glossary at the end, not a
  link. If the definition needs more than a clause, it was a step 2 foundation and belongs there.
- **Prefer the shorter, older word** — "use" over "leverage", "start" over "instantiate", "check"
  over "validate". The exception is where the precise word *is* the mechanism (a `422`, `SIGTERM`,
  the actual function name); those stay verbatim, like the literals in *Rules*.
- **One new idea per sentence.** A sentence carrying two unfamiliar things fails on both, and the
  reader cannot tell you which one broke.
- **An analogy is a bridge, not a claim.** Give one, then say where it stops being true. An
  unbounded analogy becomes a wrong mental model that outlives the explanation.

## When it did not land

First ask *what kind* of miss it was, because two of the three are not ladder moves:

- **A word you never defined.** Define it and say the same thing again at the same level. This is
  not an attempt on the ladder — you owed them the definition and the explanation was otherwise
  fine.
- **A foundation you did state, that did not take.** Go to attempt 4 directly, per step 7. The
  words were on the page and still did not land, so restating them is what already failed.
- **They have the words and cannot assemble them.** This is what the ladder below is for.

Do not restate the same explanation with more words. Drop a level and change the representation.
Only the representation changes: a re-explanation still closes on step 7's rule and self-test at
the scale the first attempt was pitched at — one question is enough for a small ask — because the
self-test is how you find out whether the new form landed.

Locate yourself on the ladder by the **form of the last attempt**, not by how many messages have
passed — invoked cold after a miss, look at what the previous explanation actually was and take the
next row down. A table is attempt 1, not attempt 3: it lays out facts side by side but carries no
structure, ordering, or flow, so a reader stuck on *how the parts connect* gains nothing from one.
A prose explanation carrying one diagram is attempt 1 too — that is step 4 done right, not the
ladder skipped ahead. Attempt 3 is the explanation rebuilt so that every step has its own picture.

| Attempt | Representation | If it still misses |
|---|---|---|
| 1 | prose, tables, and code references | go to step-by-step |
| 2 | numbered steps, one idea each | go to pictures |
| 3 | one ASCII diagram per step | stop adding pictures — go to attempt 4 |
| 4 | define the foundations, then rebuild the explanation on them | ask which sentence broke |

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

**"Not documented" and "I did not check" are different answers.** "Not documented" is a claim, and
only a grep earns it; with no grep the honest answer is "I did not check". Report which of the two
you are giving. The same holds for "this path was never verified end to end" — often the single
most valuable line in the whole explanation.

## Rules

- **Evidence over inference.** Unclear purpose is written as "purpose unclear — checked imports and
  call sites, no references found", never guessed at. Never invent a responsibility.
- **Don't paste code.** A signature or a three-line snippet is the ceiling. A literal that *is* the
  behavior — a constant, a threshold, a regex, a status string — is quoted verbatim and does not
  count against that ceiling; paraphrasing a value loses the mechanism.
- **Describe what exists today**, not what was planned or is half-built.

## Anti-patterns

- Explaining from a design doc because it is well written. If the reader had understood the doc,
  they would not be asking.
- Opening at the level the subject's own documentation is pitched at, which already assumes the
  reader chose to use the thing.
- Treating a term as known because the reader typed it, when they may have copied it out of an
  error message.
- Reusing a term introduced earlier in the session as though it is now known.
- A diagram where a table would do; Mermaid where the reader has a terminal.
- Answering "is this documented?" with yes or no instead of a grep result per file.
- Ending on the mechanism instead of the rule of thumb.
- Restating attempt N as attempt N+1 with more words.
