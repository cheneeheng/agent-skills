---
name: blog-writer
description: Trigger when the user has raw material — notes, bullets, an outline, or fragments — and wants to go straight to a draft without an interview. Trigger when user says "turn these notes into a blog post", "write a post from this outline", "draft from these bullets", "I've got my notes, just write it", "here's my outline, write the post", or provides non-prose material and asks to draft or write. Do NOT trigger when the user only has a topic but no material — use blog-interviewer. Do NOT trigger when the user provides a repo or code artefact — use blog-interviewer Phase 0. Do NOT trigger when the user has written prose to improve — use blog-editor.
---

# Blog Writer Skill

## Core Principles

- **Read everything before writing anything**: Don't skim and draft. Read the full material, identify the angle, then produce a single complete draft.
- **One question maximum**: If something critical is genuinely missing, ask exactly one question. Do not run an interview. If the material is sparse but workable, make a reasonable call and note it in the refinement offer.
- **Pick the strongest thread**: If the material is sprawling or multi-directional, choose the sharpest angle rather than trying to cover everything. Tell the user which thread you picked and why.
- **Use the user's words**: Pull real phrases, specifics, and examples from the material rather than paraphrasing into generic prose. The material is the source of truth for voice and substance.
- **No fluff drafts**: The output should be punchy, well-structured, and worth publishing — not a padded word count that mirrors the input length.

---

## Phase 1 — Read and Assess the Material

Read all provided material before doing anything else. Then assess:

### Identify Post Type

Match the material to the most fitting post type from the taxonomy below:

| Type | Trigger Signals | What It Needs |
|---|---|---|
| **Lessons Learned** | "I tried X", "we built Y", "I made a mistake", a story that ends with insight | A real story arc: situation → problem → decision → outcome → insight |
| **How-To / Tutorial** | Step-by-step notes, commands, config snippets, a process to teach | Concrete steps, actual commands/examples, common pitfalls |
| **Opinion / Take** | A thesis, a position, arguments for and against, "I think X is wrong" | A clear thesis, 2–3 supporting arguments, counter-argument addressed |
| **Project / Launch Announcement** | "I shipped X", feature descriptions, what it does and why, what was hard | What it does, why it matters, what was hard, what's next |
| **Thought Leadership** | A view on a trend, industry claim, or non-obvious argument | Unique insight, backed by evidence or experience, non-obvious conclusion |
| **Personal Story** | A journey narrative, turning point, emotional arc | Emotional arc, honest detail, why the reader should care |

### Assess Completeness

Before drafting, judge whether the material is sufficient:

- **Rich material**: Multiple specifics, a clear arc or argument, enough texture to write from. Draft immediately.
- **Workable but sparse**: The angle is clear but some detail is thin. Draft with what's there; flag the gaps in the refinement offer rather than asking upfront.
- **Genuinely incomplete**: The material names a topic but has no substance — no story, no steps, no argument, just keywords. This is the one case where a single question is warranted before drafting.

---

## Phase 2 — Handle Edge Cases

Address these before drafting:

### Wall of Text with Multiple Threads

If the material covers more than one coherent story or argument, **pick the strongest one** — don't try to weave them together. Tell the user:

> *"Your notes cover a few different directions. I've chosen to write about [angle X] because [brief reason — e.g., it has the clearest arc / the most specific detail / the most useful takeaway]. If you'd rather I write about [angle Y], let me know and I'll re-draft."*

Then draft immediately — don't ask permission before proceeding.

### Material Too Sparse to Draft

If the material is genuinely too thin (topic named, no substance), ask **one** question that unlocks the most:

> *"Your notes give me the topic but I need one more thing before I can write this well: [single most important question — e.g., 'What was the moment this actually became a problem?' / 'What's the step most people get wrong?' / 'What's the argument you're making against the conventional view?']"*

After receiving the answer, draft without further questions.

### Conflicting Signals

If the material sends mixed signals about post type, audience, or angle (e.g., half the notes are story-mode, half are tutorial-mode), pick the dominant signal and note the tension:

> *"Your notes mix story and tutorial. I've written this as a [Lessons Learned / How-To], which fits the majority of the material. If you want the other framing, I can re-draft."*

### How-To with Abstract Steps

If the material describes a process conceptually but lacks real commands, config examples, or code snippets, draft with what's there and flag it explicitly in the refinement offer:

> *"The steps section is based on your description — if you have actual commands or config to add, drop them in and I'll weave them in."*

Don't ask for them upfront if the rest of the material is strong enough to proceed.

---

## Phase 3 — Draft the Post

Produce a complete draft — not an outline, not a bullet summary.

### Draft Standards

- **Title**: Sharp, specific, and honest. Avoid clickbait. Avoid vague ("My Thoughts on X"). Aim for: *specific claim + implicit promise to reader*.
- **Opening**: Hook in the first 2 sentences. Start with the tension, the surprise, or the concrete moment — not background.
- **Body**: Match structure to post type (see below). Use the user's own words and specifics wherever possible — don't paraphrase real details into abstractions.
- **Closing**: End with the insight, the call to action, or the honest takeaway. Don't fizzle out into "I hope this was helpful."
- **Length**: Match what the content needs — don't pad, don't cut substance. Per-type guidance:
  - Opinion / Personal Story / Thought Leadership: 400–800 words. Tight is better.
  - Lessons Learned / Launch: 600–1,000 words. Enough to tell the story properly.
  - How-To / Tutorial: 800–1,800 words, driven by the number of steps and examples needed. Don't impose a ceiling if the content genuinely requires more.

### Structure by Post Type

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
The Origin: Why you built this — what was missing, what frustrated you, why existing tools didn't cut it
How It Works: The interesting parts only — architecture, key decisions, not a feature list
What Was Hard: Be honest — one real technical or design challenge
What's Next: Where this is going
CTA: Try it / read the docs / follow for updates
```

**Thought Leadership:**
```
Hook: State the non-obvious claim or question upfront — don't bury the thesis
Argument: Build through specific examples, not abstract assertions (name real products, companies, events)
Counter-argument: The strongest objection — acknowledge it directly, then explain why the thesis holds
Implication: What changes if the reader accepts this view? (concrete, not vague)
Close: A challenge, a question, or a line that reframes how the reader sees the topic
```

**Personal Story:**
```
Hook: The specific moment this post is really about — one concrete scene, not a summary
Setup: Enough context to understand what was at stake (brief)
Arc: What happened, what changed, what the turning point was
The Insight: What you actually learned — specific, not "I learned resilience"
Takeaway: What the reader should do or notice as a result — make it actionable
```

---

## Phase 4 — Refine

After sharing the draft, ask: *"What's landing well and what feels off?"*

Also offer **one proactive observation** — something you'd fix even if they're happy. Don't just ask and wait.

### Common issues to watch for and raise:

- **Opening too slow**: First paragraph is setup, not tension — flag and offer an alternative opening.
- **Missing the specific**: Draft generalizes where source material has real details — insert them.
- **Wrong angle**: Post reads for practitioners but material suggests a broader audience (or vice versa) — raise it.
- **Conclusion fizzles**: Ending restates intro or trails off — replace with a sharper close.
- **Generic title**: Title could describe dozens of posts — push for a specific claim or hook.
- **Tone mismatch**: Source is casual but draft is formal (or vice versa) — ask if they want the voice adjusted.
- **Gaps flagged earlier**: Surface thin spots as concrete invitations: *"The pitfalls section would be stronger with a real example — do you have one?"*

If the user wants a different angle or structure entirely, **re-draft** — don't just patch. A revision that fights the original structure will read like a revision.

---

## Output Format

**Before drafting (if noting thread selection or flagging a gap):** One short paragraph — direct, no preamble. Then the draft immediately after.

**Final draft:** Formatted as a complete blog post, ready to copy-paste. Include:
- Title
- Body (with subheadings only if post length warrants it)
- A one-line meta description: `> **Meta:** [description]` — ~150 chars, specific angle, readable without the title
