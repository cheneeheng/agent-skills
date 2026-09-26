---
name: explain-in-chunks
description: >-
  Load this skill when the user asks to have a topic explained and the answer should come from
  what is in the workspace, one part at a time rather than all at once: "explain X to me step by
  step", "walk me through how X works here", "teach me X in parts", "explain this in chunks",
  "don't dump it all at once", "explain X using only what's in the repo/docs/notes". Grounds every
  claim in a file from the accessible workspace(s) and cites it, refuses to fill gaps from general
  knowledge, plans the topic as an ordered series of parts, delivers exactly one part per turn,
  and makes each part standalone or explicitly linked to the earlier part it builds on. Also load
  when the user says "next", "continue", "go on", or "back to part N" during such a series. Not for
  a whole-repo orientation file (ceh-coding-agent:explain-codebase), not for writing user-facing
  documentation (ceh-documentation), and not for implementing, fixing, or reviewing code.
argument-hint: '[topic to explain]'
---

# Explain in Chunks

Two promises to the user, and everything below exists to keep them:

1. **Grounded** — every claim about the topic comes from a file in a workspace this session can
   read, and says which file.
2. **Paced** — the user gets one part, understands it, then asks for the next. Never the whole
   thing at once.

## Where information may come from

**Allowed sources:** files in the primary working directory and in any additional workspace
directory this session has access to — code, docs, notes, configs, specs, ADRs, git history of
those repos. Nothing else counts as a source.

**Not a source:** your general knowledge, the web, the name of a library, what a file "probably"
does from its name. General knowledge may supply only ordinary language to connect sourced facts —
"a function", "a list", "calls" — never a fact about the topic.

When a part needs a fact the workspace does not contain, say so in place and keep going:

> The workspace does not say how retries are scheduled. `queue/worker.py:40` calls `retry()`, but
> its definition is not in any directory I can read.

Never paper over the gap with a plausible guess. If the user explicitly asks for outside knowledge
on a point, give it only in a separate block labelled **Outside the workspace:** so it can never
be mistaken for a sourced claim.

## Step 1 — Check coverage before promising anything

1. List the workspaces you can read (primary working directory plus any added directories).
2. Search them for the topic: its name, synonyms, identifiers, file names, headings. For a large
   workspace, delegate the search to a read-only subagent and ask for `path:line` anchors back —
   then read the anchored lines yourself before citing them.
3. Decide:

| Found | Do |
|---|---|
| Nothing relevant | Stop. Say the topic is not covered, list where you searched and the terms you used, and ask whether it lives somewhere you cannot see. Explain nothing. |
| Fragments only | Say which aspects are covered and which are not, then offer a plan over the covered aspects only. |
| Enough | Go to Step 2. |

Read the sources themselves, not summaries of them. Where two sources disagree (a doc says one
thing, the code another), keep both — the conflict is part of the explanation, and you cite both
sides rather than silently picking one.

## Step 2 — Plan the parts

Split the topic into an ordered series of parts. Each part:

- answers **one question** the user could ask in a sentence ("What enters the pipeline?", "Who
  decides when a job fails?");
- fits in roughly **150–300 words** plus at most one small code excerpt or ASCII diagram;
- comes **after** every part it depends on. Foundations first, then mechanisms, then edge cases.
  A part must never lean on something a later part introduces.

Aim for 3–7 parts. Fewer than 3 means the topic is small enough to answer directly — say so and
answer in one go. More than 7 means the topic is really two topics — offer to split it and ask
which half comes first.

Mark each part in the plan as **standalone** (readable with no earlier part) or **builds on Part
N** (names the specific earlier part it needs). Prefer standalone when the cost is one recap
sentence.

## Step 3 — Deliver one part per turn

The first reply holds the plan and Part 1, nothing more:

```
Explaining <topic> in <N> parts, from <which workspace(s)>:

1. <title> — <the one question it answers>  (standalone)
2. <title> — <question>  (builds on 1)
3. ...

## Part 1 of N — <title>

<body>

Sources: `path/to/file.py:12-30`, `docs/design.md:4`

Next: Part 2 — <title>. Say "next", ask about anything above, or jump to a part by number.
```

Every later part uses the same shape, with a link line directly under the heading:

```
## Part 3 of 5 — <title>
Builds on Part 2: <the one fact from Part 2 this part needs, restated in one sentence>.

<body>

Sources: ...

Next: Part 4 — <title>. ...
```

A standalone part says `Standalone — no earlier part needed.` in that line instead.

Rules for the body:

- **Cite as you go.** Every factual sentence about the topic is traceable to a `path:line` in the
  Sources line; quote short excerpts inline when the exact wording matters. Re-open the lines
  before citing — a line number from memory drifts.
- **Restate, don't point.** "Builds on" restates the needed fact in one sentence so the user never
  has to scroll back. Refer only to earlier parts by number; never to "what we'll see later".
- **Define on first use.** A term the workspace uses gets defined — from the workspace — the first
  time it appears. If the workspace uses it without defining it, say that.
- **One idea deep.** If a part starts needing a second idea, that idea is the next part.

Then **end the turn.** Do not deliver the next part until the user asks, even if the part feels
short. "Give me the rest" or "all at once" is the only override, and even then keep the part
headings so the structure survives.

## Step 4 — Handle what the user does between parts

| User says | Do |
|---|---|
| "next", "continue", "go on" | Deliver the next undelivered part. |
| "back to part N", "repeat N" | Re-explain part N, differently this time: a concrete walk-through of one real case from the workspace, or a small diagram, instead of the same prose again. |
| A question about the current part | Answer it from the workspace with citations, briefly, then restate the Next line. |
| A question that reveals a missing foundation | Insert a new part before the current point, show the updated plan (numbers shift), and deliver the inserted part. |
| A question the plan already covers later | Say which part covers it and offer to jump; do not answer it half-way now. |
| "skip", "jump to N" | Deliver part N, turning its link line into a one-sentence recap of whatever skipped parts it needs. |
| "I get it", "stop" | Stop. Offer a three-line recap of the parts delivered, each with its main source. |

After the last part, close with a short recap — one line per part — and list any gaps found along
the way (facts the workspace does not contain), so the user knows where the explanation ends
because the sources end.

## Keeping the series alive across a long session

The plan lives in the conversation by default. When the plan has more than 5 parts, or the user
says they will come back later, also write it to `.agents_workspace/explanations/<topic-slug>.md`:
the plan, which parts are delivered, and the sources per part. Tell the user the path, and do not add the file to version control. On "continue
the explanation of X" in a later session, read that file, re-check that the cited lines still say
what the plan claims, and resume at the first undelivered part.

## Anti-patterns

| Don't | Because |
|---|---|
| Fill a gap with what the library or pattern "usually" does | The user asked for this workspace's truth; a confident guess is indistinguishable from a sourced fact |
| Deliver Part 1 and Part 2 because Part 1 was short | Pacing is the product; the user chooses when to move on |
| "As mentioned earlier…" with no restatement | The user has to scroll and reconstruct; restate the fact in one sentence |
| Forward references ("we'll see why in Part 4") | The current part is then not understandable on its own terms |
| Citing a file you only saw in a subagent's summary | You have not read it; the line may not say that |
| One giant Sources list at the end of the series | Each part must stand on its own evidence |
