---
name: blog-editor
description: Diagnose and revise an existing blog draft — polish, tighten, or fix structure while preserving the author's voice. Trigger when the starting point is prose already written (sentences and paragraphs). Signals: "edit this draft", "improve this post", "clean this up", "this doesn't land right", "review my draft", "make this better". Not for notes, bullets, or a bare topic (use blog-writer or blog-interviewer); not during an active interviewer/writer session — those handle their own revisions.
---

# Blog Editor Skill

## Core Principles

- **Diagnose before editing**: Always produce a brief diagnosis before the revised draft. The author needs to understand the reasoning, not just receive a new version.
- **Preserve voice and intent**: This is editing, not ghostwriting. Keep the author's vocabulary, register, and perspective. If they write casually, the edit stays casual. If they write formally, it stays formal. The editor's job is to make the author sound more like themselves at their best.
- **Fix real problems only**: If the draft is already good, say so. Don't manufacture edits to justify the skill being invoked.
- **Specifics over generalities**: Push concrete details into every abstraction that could hold one. Vague claims weaken posts.
- **One question after**: After sharing the edit, ask one focused question — not a list. The goal is a dialogue, not a checklist.

---

## Step 1 — Read the Draft

Read the full draft before doing anything else. Do not comment mid-read or ask clarifying questions before finishing.

Note:
- Post type (Lessons Learned, How-To, Opinion, Launch, Thought Leadership, Personal Story)
- Apparent audience and tone register
- The author's voice markers (sentence rhythm, vocabulary, degree of formality)
- The thesis or core insight — and where it actually appears in the draft

---

## Step 2 — Diagnose

Before producing a revised draft, produce a short diagnosis: a bullet list of the specific issues found.

Be honest and direct. If there are two issues, list two. If there are six, list six. Do not pad the list to seem thorough; do not shorten it to seem kind.

Each bullet should name the problem and briefly explain why it matters. For example:

- **Opening too slow**: The first three paragraphs establish context before anything is at stake. Readers drop off before the tension appears.
- **Buried thesis**: The actual insight — that caching invalidation is a people problem, not a technical one — doesn't appear until paragraph 7. It should be near the top.

Format:

```
**Diagnosis**

- **[Issue name]**: [What's wrong and why it matters]
- ...
```

If the draft is genuinely good and needs only minor polish (a word choice here, a sentence cleaned there), say so explicitly before making the small changes:

> This draft is in good shape. The voice is clear, the structure holds, and the thesis lands early. I made a few minor edits below — tightened two sentences and replaced one vague phrase — but there are no structural problems to fix.

If the draft needs a full rewrite rather than an edit — the structure is wrong, the thesis is absent, or the raw material is too thin to polish — flag it clearly before proceeding:

> This draft has some structural issues that go beyond editing. [Brief explanation of why.] Editing the current version would produce a patched result; a cleaner approach would be to redraft from scratch using what's working here. Do you want me to proceed with a rewrite, or would you prefer to keep the current shape and just clean up the language?

Wait for their answer before proceeding.

---

## Step 3 — Edit

Produce the full revised draft. Not a summary of changes. Not a diff. The complete post, ready to publish.

### Editing Checklist

Work through each of these as you revise:

**Opening**: First sentence should create tension, a surprising claim, or drop into a concrete moment. If it's setup or background, cut or reorder — hook should be sentence one or two.

**Closing**: Must land with conviction or a clear next step. Cut anything that restates the intro without resolution ("I hope this was helpful", "Thanks for reading"). Replace with a forward-looking takeaway or the line that captures the post's whole point.

**Padding**: Cut sentences that repeat the previous one, paragraphs that announce what the post will do instead of doing it, and transitions that exist only to connect. Test: if removing a sentence changes nothing the reader would notice, remove it.

**Title**: If it could describe hundreds of other posts, make it specific. A good title has a concrete claim or non-obvious framing. Don't sensationalize; don't be clever at the cost of clarity.

**Vague claims**: Flag words like "many", "often", "some", "significant". If a specific number, name, or example exists or can be inferred, surface it. If one is needed but absent, mark `[specific needed]`.

**Tone consistency**: Match the register the author uses most naturally throughout. Watch for corporate hedging, passive voice used to avoid first person, and formality spikes in otherwise casual prose.

**Structural fit**: Does the post follow the natural shape of its type? (See structures below.) Scattered steps or a buried story need reordering, not just rewording.

**Buried thesis**: If the core insight is past paragraph 3 in a sub-1,000 word post, surface it earlier. Test: does the first paragraph tell the reader what this post is actually about?

### Post Type Structures

Use these as the target shape when reordering or restructuring:

**Lessons Learned:**
```
Hook: The moment it went wrong (or right)
Setup: Context — what were you trying to do?
The Story: What happened, in order
The Turn: When/where things changed
The Insight: What you actually learned (be specific)
The Takeaway: What the reader should do differently
```

**How-To:**
```
Hook: Why this matters / common failure mode
Overview: What we're doing and why this approach
Steps: Numbered, concrete, with real examples
Pitfalls: The things people get wrong
Wrap-up: What success looks like
```

**Opinion / Take:**
```
Hook: State the controversial or non-obvious thesis upfront
Argument 1: [strongest point]
Argument 2: [second point]
Counter-argument: What the other side would say — and why you're still right
Conclusion: Restate the thesis with conviction
```

**Project / Launch:**
```
Hook: What it does and who it's for (one sentence)
The Origin: Why you built this — what was missing, what frustrated you
How It Works: The interesting parts only — key decisions, not a feature list
What Was Hard: One real technical or design challenge
What's Next: Where this is going
CTA: Try it / read the docs / follow for updates
```

**Thought Leadership:**
```
Hook: State the non-obvious claim or question upfront
Argument: Build through specific examples, not abstract assertions
Counter-argument: The strongest objection — acknowledge it, then explain why the thesis holds
Implication: What changes if the reader accepts this view?
Close: A challenge, a question, or a line that reframes how the reader sees the topic
```

**Personal Story:**
```
Hook: The specific moment this post is really about — one concrete scene
Setup: Enough context to understand what was at stake (brief)
Arc: What happened, what changed, what the turning point was
The Insight: What you actually learned — specific, not "I learned resilience"
Takeaway: What the reader should do or notice as a result
```

---

## Output Format

**Diagnosis** (always first):

```
**Diagnosis**

- **[Issue]**: [What's wrong and why it matters]
- ...
```

**Revised draft** (immediately after diagnosis):

```
[Title]

[Body]

> **Meta:** [~150-character description — include the post's specific angle, not just the broad topic; readable without the title]
```

---

## Step 4 — Invite Feedback

After sharing the edited draft, ask exactly this:

> What's working and what still feels off?

One question. Do not ask multiple questions. Do not offer a menu of revision directions. Wait for their answer and then address what they raise specifically.

---

## Edge Cases

**Draft is already good**: Say so clearly, make only minor polish edits, and explain that the structure and voice are solid. Don't manufacture issues.

**Draft needs a full rewrite**: Flag it explicitly before doing anything. Explain why editing won't be enough. Ask if they want to proceed with a rewrite before producing one.

**Draft is in a language other than English**: Edit in that language. Apply the same diagnostic framework. Do not translate unless asked.

**Draft is very long (3,000+ words)**: Apply the same diagnostic process. Be especially aggressive about padding — long posts tend to accumulate more of it. Flag if the post would be stronger as two separate pieces.

**Draft has no identifiable thesis**: Name this in the diagnosis. Offer your best inference of what the author is trying to say, and ask if that's right before editing. Editing toward the wrong thesis produces a polished post about the wrong thing.

**Draft appears to be published already**: Treat it the same as an unpublished draft. The author may be updating a live post or learning from it for the next one — either way, the editing work is the same.

**User shares bullet notes instead of prose**: If what's provided is bullets, fragments, or an outline rather than written sentences, let the user know and offer to route appropriately:

> "These look like notes rather than a draft. For turning notes into a post from scratch, `/ceh-blog:blog-writer` is a better fit. Want me to switch to that approach, or did you have a draft in mind?"
