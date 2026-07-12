---
name: blog-editor
disable-model-invocation: true
description: Diagnose and revise an existing blog draft — polish, tighten, or fix structure while preserving the author's voice. For notes or a bare topic use blog-writer or blog-interviewer instead.
---

# Blog Editor Skill

## Core Principles

- **Diagnose before editing**: a brief diagnosis always precedes the revised draft — the author needs the reasoning, not just a new version.
- **Preserve voice and intent**: editing, not ghostwriting. Keep the author's vocabulary, register, and perspective — casual stays casual, formal stays formal. The job is to make the author sound more like themselves at their best.
- **Personal voice, not influencer style**: the house voice is first-person, reflective, and quiet — the reader overhears reasoning rather than being taught. Never edit *toward* influencer tells: punchy standalone one-liner paragraphs, aphoristic closers, imperative lessons aimed at the reader, "If you're building X, then Y" prescriptions, bold pseudo-headers as section labels, tidy meta-takeaway sign-offs, CTA endings. Diagnose these when present; never introduce them. An open or reserved ending is valid — don't "fix" it into a conviction closer. If the target repo's `CLAUDE.md` defines a blog voice, it overrides the structures below.
- **Fix real problems only**: if the draft is already good, say so. Don't manufacture edits to justify the skill being invoked.
- **Specifics over generalities**: push concrete details into every abstraction that could hold one.
- **One question after**: after sharing the edit, ask one focused question — a dialogue, not a checklist.

---

## Step 1 — Read the Draft

Read the full draft before doing anything else — no mid-read comments or questions. Note: post type (Lessons Learned, How-To, Opinion, Launch, Thought Leadership, Personal Story); apparent audience and register; the author's voice markers (rhythm, vocabulary, formality); the thesis — and where it actually appears.

---

## Step 2 — Diagnose

Produce a short, honest bullet list of the specific issues — two if there are two, six if there are six. Each bullet names the problem and why it matters:

```
**Diagnosis**

- **[Issue name]**: [What's wrong and why it matters]
- ...
```

If the draft is genuinely good and needs only minor polish, say so explicitly before the small changes:

> This draft is in good shape — the voice is clear, the structure holds, the thesis lands early. I made a few minor edits below, but there are no structural problems to fix.

If it needs a full rewrite (wrong structure, absent thesis, material too thin to polish), flag it and **wait for their answer**:

> This draft has structural issues that go beyond editing. [Why.] Editing would produce a patched result; a cleaner approach is to redraft using what's working. Proceed with a rewrite, or keep the shape and just clean up the language?

---

## Step 3 — Edit

Produce the full revised draft — not a summary of changes, not a diff. Work through this checklist:

**Opening**: first sentence should create tension, a surprising claim, or a concrete moment. Setup or background: cut or reorder — the hook is sentence one or two.

**Closing**: must land on something honest — the open thread (what's unresolved, what the author is watching for, what comes next) or a reserved verdict. Cut "I hope this was helpful" / "Thanks for reading" — but don't replace with a tidy takeaway, lesson, or CTA; that turns a personal story into a lecture. A genuinely open ending is valid. Only a finished series' final post ends with closure.

**Padding**: cut sentences that repeat the previous one, paragraphs that announce instead of doing, connective-only transitions. Test: if removing it changes nothing the reader would notice, remove it.

**Title**: if it could describe hundreds of posts, make it specific — a concrete claim or non-obvious framing. Don't sensationalize; don't be clever at the cost of clarity.

**Vague claims**: flag "many", "often", "some", "significant". Surface a number, name, or example if one exists or can be inferred; otherwise mark `[specific needed]`.

**Tone consistency**: match the author's most natural register. Watch for corporate hedging, passive voice avoiding first person, formality spikes in casual prose.

**Influencer tells**: quiet down any banned tell (see Core Principles) — fold them back into connected, first-person paragraphs. Never introduce them.

**Series continuity**: if the draft is an episode in a series, check against earlier posts — versions, dates, what the reader already knows. It should pick up the previous episode's open thread (cross-linked) rather than re-telling a story an earlier post owns.

**Structural fit**: does the post follow its type's natural shape (below)? Scattered steps or a buried story need reordering, not rewording.

**Buried thesis**: core insight past paragraph 3 in a sub-1,000-word post — surface it earlier. Test: does the first paragraph tell the reader what this post is actually about?

### Post Type Structures

Target shapes for reordering or restructuring. Every template ends on **the open thread**: the honest current state — what's unresolved, what the author will watch for, what comes next. A reserved verdict ("I'm keeping it, for now") is valid. A finished series' final post ends with closure instead — no manufactured cliffhangers.

**Lessons Learned:**
```
Hook: The moment it went wrong (or right)
Setup: Context — what were you trying to do?
The Story: What happened, in order
The Turn: When/where things changed
The Insight: What you actually learned (be specific)
The Open Thread: What's unresolved, what you'll watch for, what comes next
```

**How-To:**
```
Hook: The moment this became a problem for you / what it cost you
Overview: What we're doing and why this approach
Steps: Numbered, concrete, with real examples
Pitfalls: What they cost you — narrated as your experience, not warnings issued to the reader
The Open Thread: Where this leaves you — what's still rough, what you're watching for
```

**Opinion / Take:**
```
Hook: State the controversial or non-obvious thesis upfront
Argument 1: [strongest point]
Argument 2: [second point]
Counter-argument: What the other side would say — and why you're still right
The Open Thread: Where you actually land — a reserved verdict is valid; what would change your mind
```

**Project / Launch:**
```
Hook: What it does and who it's for (one sentence)
The Origin: Why you built this — what was missing, what frustrated you
How It Works: The interesting parts only — key decisions, not a feature list
What Was Hard: One real technical or design challenge
The Open Thread: What's unresolved, what you're watching for, what comes next
```

**Thought Leadership:**
```
Hook: State the non-obvious claim or question upfront
Argument: Build through specific examples, not abstract assertions
Counter-argument: The strongest objection — acknowledge it, then explain why the thesis holds
Implication: What changes if this view holds?
The Open Thread: What's still unresolved in your own thinking — what you'll watch for next
```

**Personal Story:**
```
Hook: The specific moment this post is really about — one concrete scene
Setup: Enough context to understand what was at stake (brief)
Arc: What happened, what changed, what the turning point was
The Insight: What you actually learned — specific, not "I learned resilience"
The Open Thread: What's unresolved, what you'll watch for, what comes next
```

---

## Output Format

**Diagnosis** first (format above), then the revised draft immediately after:

```
[Title]

[Body]

> **Meta:** [~150-character description — the post's specific angle, not just the broad topic; readable without the title]
```

---

## Step 4 — Invite Feedback

After sharing the edited draft, ask exactly this — one question, no menu of revision directions:

> What's working and what still feels off?

Wait for their answer, then address what they raise specifically.

Once the user is satisfied, mention: *"When you're ready to share this, `/ceh-blog:blog-repurpose` can adapt it into a Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb."*

---

## Edge Cases

**Draft is already good**: say so clearly, make only minor polish edits. Don't manufacture issues.

**Draft needs a full rewrite**: flag it before doing anything; ask before producing one.

**Draft in another language**: edit in that language, same framework. Don't translate unless asked.

**Very long draft (3,000+ words)**: same process; be especially aggressive about padding. Flag if it would be stronger as two pieces.

**No identifiable thesis**: name it in the diagnosis, offer your best inference, and confirm before editing — editing toward the wrong thesis polishes the wrong post.

**Already published**: treat the same as unpublished — updating a live post or learning for the next one is the same editing work.

**Bullet notes instead of prose**: offer to route:

> "These look like notes rather than a draft. For turning notes into a post from scratch, `/ceh-blog:blog-writer` is a better fit. Want me to switch, or did you have a draft in mind?"
