---
name: blog-writer
description: Draft a complete blog post from raw material — notes, bullets, an outline, or fragments — with no interview. Trigger when the user has non-prose material ready and wants to go straight to a draft. Signals: "turn these notes into a post", "write a post from this outline", "draft from these bullets", "I've got my notes, just write it". Not for a bare topic with no material or a repo/code artefact (use blog-interviewer); not for written prose to improve (use blog-editor).
---

# Blog Writer Skill

## Voice

Personal voice, not influencer style — the reader overhears the reasoning, not a lecture. If the
target repo's `CLAUDE.md` defines a blog voice, it overrides every structure template below.

**Prefer:** first person, grounded in what actually happened and was thought; connected
paragraphs that carry the narrative — reflective, not prescriptive; doubt and self-report kept in
("I shipped it anyway, because I was tired of this bug"); quieter is better; open inside a moment
or a thought — an annoyance, a realization, a scene — never a product pitch or background.

**Banned tells:** punchy standalone one-liner paragraphs; aphoristic closers ("The boring choice
is the correct one"); imperative lessons aimed at the reader ("Don't design your own. Surface
theirs."); "If you're building X, then Y" prescriptions; bold pseudo-headers as section labels
("**What it does**", "**The lesson:**"); tidy meta-takeaway sign-offs that turn a personal story
into a lecture; CTA endings.

**Never invent scenes, feelings, or chronology.** Every beat comes from the material (changelogs,
specs, commits) or the author's own words — quote those nearly verbatim; the phrasing *is* the
voice. If a human beat is missing, flag the gap instead of fabricating it.

**Endings — the open thread:** the honest current state — what's unresolved, what you'll watch
for, what comes next. A reserved verdict ("I'm keeping it, for now") is valid. Only a finished
series' final post ends with closure — no manufactured cliffhangers. Never a tidy takeaway,
lesson, or CTA.

**Series:** the blog is serials — each project a series, each post an episode the reader follows
in order (see Series Awareness below).

**Tutorials** keep full utility — real code, steps, pitfalls — but pitfalls are narrated as what
they cost the author, not warnings issued to the reader.

---

## Core Principles

- **Read everything before writing anything**: full material first, identify the angle, then one complete draft.
- **One question maximum**: if something critical is missing, ask exactly one question — no interview. Sparse but workable material: make a reasonable call and note it in the refinement offer.
- **Pick the strongest thread**: if the material sprawls, choose the sharpest angle rather than covering everything. Tell the user which thread you picked and why.
- **Use the user's words**: pull real phrases, specifics, and examples from the material — it is the source of truth for voice and substance.
- **No fluff drafts**: specific, well-structured, worth publishing — not a padded word count mirroring the input length.

---

## Phase 1 — Read and Assess the Material

Read all provided material before doing anything else. Then assess:

### Identify Post Type

| Type | Trigger Signals | What It Needs |
|---|---|---|
| **Lessons Learned** | "I tried X", "we built Y", "I made a mistake", a story ending in insight | Story arc: situation → problem → decision → outcome → insight |
| **How-To / Tutorial** | Step-by-step notes, commands, config snippets | Concrete steps, actual commands/examples, pitfalls |
| **Opinion / Take** | A thesis, a position, "I think X is wrong" | Clear thesis, 2–3 arguments, counter-argument addressed |
| **Project / Launch** | "I shipped X", feature descriptions, what was hard | What it does, why it matters, what was hard, what's next |
| **Thought Leadership** | A view on a trend or non-obvious argument | Unique insight backed by evidence, non-obvious conclusion |
| **Personal Story** | A journey narrative, turning point, emotional arc | Emotional arc, honest detail, why the reader should care |

### Assess Completeness

- **Rich material**: multiple specifics, a clear arc or argument. Draft immediately.
- **Workable but sparse**: angle clear, some detail thin. Draft; flag gaps in the refinement offer rather than asking upfront.
- **Genuinely incomplete**: a topic with no substance — no story, steps, or argument. The one case warranting a single question before drafting.

### Series Awareness

Read the existing posts in the target blog first. If the new post continues a project:

- Open by picking up the live thread the previous episode left ("Last time I said…") and cross-link it.
- End by leaving a live thread of your own — closure instead if the series is finished.
- Check continuity facts against earlier episodes: version numbers, dates, what the reader already knows.
- Don't re-tell a story a previous episode owns — call back in a sentence and link.

---

## Phase 2 — Handle Edge Cases

Address before drafting:

**Wall of text with multiple threads**: pick the strongest one — don't weave. Tell the user, then draft immediately without asking permission:

> *"Your notes cover a few directions. I've written about [angle X] because [reason]. If you'd rather have [angle Y], I'll re-draft."*

**Material too sparse to draft**: ask **one** question that unlocks the most (e.g., "What was the moment this actually became a problem?"), then draft without further questions.

**Conflicting signals** (half story, half tutorial): pick the dominant signal and note the tension:

> *"Your notes mix story and tutorial. I've written this as a [type], which fits most of the material. If you want the other framing, I can re-draft."*

**How-To with abstract steps**: if real commands/config/code are missing, draft with what's there and flag it in the refinement offer (*"drop in actual commands and I'll weave them in"*) — don't ask upfront if the rest is strong enough.

---

## Phase 3 — Draft the Post

Produce a complete draft — not an outline, not a bullet summary.

### Draft Standards

- **Title**: sharp, specific, honest. No clickbait, no vague "My Thoughts on X". Aim for: *specific claim + implicit promise to reader*.
- **Opening**: inside a moment or a thought within the first 2 sentences — not background, not a product pitch.
- **Body**: match structure to post type (below). Use the user's own words and specifics — don't paraphrase real details into abstractions.
- **Closing**: the open thread (see Voice). No "I hope this was helpful", no manufactured takeaway/lesson/CTA.
- **Length**: what the content needs — don't pad, don't cut substance.
  - Opinion / Personal Story / Thought Leadership: 400–800 words. Tight is better.
  - Lessons Learned / Launch: 600–1,000 words.
  - How-To / Tutorial: 800–1,800 words, driven by steps and examples — no ceiling if genuinely required.

### Structure by Post Type

Every template ends on **the open thread** (defined in Voice).

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
The Origin: Why you built this — what was missing, what frustrated you, why existing tools didn't cut it
How It Works: The interesting parts only — architecture, key decisions, not a feature list
What Was Hard: Be honest — one real technical or design challenge
The Open Thread: What's unresolved, what you're watching for, what comes next
```

**Thought Leadership:**
```
Hook: State the non-obvious claim or question upfront — don't bury the thesis
Argument: Build through specific examples, not abstract assertions (name real products, companies, events)
Counter-argument: The strongest objection — acknowledge it directly, then explain why the thesis holds
Implication: What changes if this view holds? (concrete, not vague)
The Open Thread: What's still unresolved in your own thinking — what you'll watch for next
```

**Personal Story:**
```
Hook: The specific moment this post is really about — one concrete scene, not a summary
Setup: Enough context to understand what was at stake (brief)
Arc: What happened, what changed, what the turning point was
The Insight: What you actually learned — specific, not "I learned resilience"
The Open Thread: What's unresolved, what you'll watch for, what comes next
```

---

## Phase 4 — Refine

After sharing the draft, ask: *"What's landing well and what feels off?"* Also offer **one
proactive observation** — something you'd fix even if they're happy.

Watch for and raise:

- **Opening too slow**: first paragraph is setup, not a moment — offer an alternative opening.
- **Missing the specific**: draft generalizes where the material has real details — insert them.
- **Wrong angle**: post reads for practitioners but material suggests a broader audience (or vice versa).
- **Conclusion fizzles or lectures**: ending restates the intro, trails off, or lands on a tidy takeaway/CTA — replace with the genuinely open thread or a reserved verdict.
- **Influencer tells**: any banned tell present — rewrite quieter, per Voice.
- **Continuity slip**: a version, date, or fact contradicts an earlier episode — fix against the previous posts.
- **Generic title**: could describe dozens of posts — push for a specific claim or hook.
- **Tone mismatch**: source casual, draft formal (or vice versa) — ask if they want the voice adjusted.
- **Gaps flagged earlier**: surface thin spots as concrete invitations: *"The pitfalls section would be stronger with a real example — do you have one?"*

If the user wants a different angle or structure, **re-draft** — a revision that fights the original structure reads like a revision.

---

## Output Format

**Before drafting** (if noting thread selection or flagging a gap): one short paragraph, then the draft immediately.

**Final draft**: complete post, ready to copy-paste — title; body (subheadings only if length warrants); one-line meta description `> **Meta:** [description]` — ~150 chars, specific angle, readable without the title.
