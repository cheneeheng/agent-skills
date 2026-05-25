---
name: ceh-blog-repurpose
description: >
  Use this skill when the user has a finished or near-finished blog post and wants to adapt it for
  other distribution channels. Trigger when the user says things like "turn this into a thread",
  "make a LinkedIn post from this", "repurpose this post", "create social content from this",
  "write a TL;DR for this", "make a newsletter blurb", "adapt this for Twitter", "I want to share
  this on LinkedIn", "summarise this post in a few sentences", "create a teaser for my newsletter",
  or any variation where they have an existing post and want one or more alternative formats.
---

# Blog Repurpose Skill

Every output must stand alone — the reader shouldn't need the original post to get the value.

## Step 0 — Identify the Format(s)

If the user specifies which format(s) they want, proceed immediately to production.

If the format is unspecified, ask once:

> *"Which format(s) would you like? I can produce:*
>
> *1. **Twitter/X thread** — Hook tweet + numbered thread (8–15 tweets) + CTA close*
> *2. **LinkedIn post** — 150–300 words, professional but not stiff, ends with a question*
> *3. **TL;DR** — 2–3 sentences capturing the thesis and key takeaway*
> *4. **Newsletter blurb** — 3–5 sentences teasing the post, ends with `[Read more →]`*
>
> *You can request any combination."*

If the user asks for all four, produce all four — clearly labelled.

---

## Step 1 — Read the Post

Before producing anything, identify:

- **The thesis**: What is the single central claim or argument?
- **The key takeaway**: What should the reader walk away knowing, doing, or thinking differently?
- **The audience**: Technical practitioners? Founders? General readers? A niche community?
- **The tone**: Casual and personal? Authoritative and analytical? Opinionated?
- **Post length**: Is there enough content to fill a thread, or is it short-form?

### Edge Case: No Clear Thesis

If the post lacks a clear central argument — it meanders, covers too many unrelated points, or
reads as a collection of observations without a through-line — flag it before repurposing:

> *"Before I repurpose this, I want to flag that the post doesn't have a clear central thesis yet.
> Repurposing a fuzzy post produces fuzzy content — the thread and LinkedIn post will feel
> scattered rather than landing a single punch.*
>
> *Do you want to sharpen the post's argument first? Or if you'd prefer, I can repurpose it as-is
> and you can see what comes out."*

Wait for the user's answer. If they want to sharpen first, suggest `/ceh-blog:blog-editor` — it diagnoses structural issues and produces a revised draft. Once the post is tightened, come back to repurpose.

### Edge Case: Post Too Short to Thread

If the post is too short to support a thread (fewer than ~400 words, or only 2–3 distinct points),
flag it:

> *"This post is quite short — there isn't enough content to make a thread that doesn't feel padded.
> I'd recommend LinkedIn post and/or TL;DR instead. Want me to produce those?"*

If they insist on a thread, produce the best thread possible and note where it feels thin.

---

## Step 2 — Produce the Output(s)

Produce every requested format. When producing multiple formats, label each clearly with a markdown
heading (e.g. `## Twitter/X Thread`). Produce them in the order: Thread → LinkedIn → TL;DR →
Newsletter blurb.

---

### Format 1: Twitter/X Thread

**Structure:**

```
[Hook tweet]        — standalone, strong, makes someone stop scrolling
[Tweet 2]           — first point or the setup
[Tweets 3–N]        — one idea per tweet, numbered (e.g. "2/")
[Closing tweet]     — CTA: link, follow, or question
```

**Rules:**

- **Hook tweet**: Must work as a standalone tweet. No "A thread on…" as the hook — that's filler.
  Open with the most surprising, counterintuitive, or high-stakes claim in the post. If someone
  only reads the hook, they should get genuine value or be genuinely curious.
- **Numbered tweets**: Use "2/" style numbering starting from tweet 2. Each tweet must land on its
  own — if it only makes sense in context of the previous tweet, rewrite it to be self-contained.
  No continuation tweets that are just the same sentence split in two.
- **Length**: Each tweet ≤ 280 characters. Count carefully on long tweets.
- **Count**: 8–15 tweets total depending on post length and number of distinct points. No filler
  tweets. If the post only supports 6 good tweets, make 6 good tweets — don't pad to hit a number.
- **Closing tweet**: Include a CTA. Options: link to the full post (use `[link]` as placeholder),
  ask a question to spark replies, or invite a follow. Don't end with "That's it!" — end with
  something that invites engagement.
- **No hashtag spam**: 0–1 hashtags total, only if genuinely relevant. Not on every tweet.

---

### Format 2: LinkedIn Post

**Structure:**

```
[Lead line]         — the insight or claim, upfront
[Body]              — supporting points, story, or evidence (2–4 short paragraphs)
[Close]             — question or observation that invites comments
```

**Rules:**

- **150–300 words.** Long enough to develop one idea properly; short enough to be read in full.
- **Lead with the insight, not the backstory.** Don't open with "I've been thinking about X lately"
  or "Last week, something interesting happened." Open with the thing you learned, argued, or
  observed.
- **Match the tone of the original post.** If the post is technical, don't dumb it down for
  LinkedIn. If it's personal and honest, don't make it corporate. The writer's voice should survive
  the adaptation.
- **Line breaks for scannability.** Short paragraphs (2–4 sentences max). One blank line between
  each. LinkedIn collapses long walls of text behind "see more."
- **0–2 hashtags.** Only if they are genuinely descriptive and the audience uses them to discover
  content. Not `#Blessed`, not `#ThoughtsOnLeadership`. If in doubt, use zero.
- **End with a question or observation** that gives the reader something to respond to. Not a
  generic "What do you think?" — a specific question that relates to the post's argument.

---

### Format 3: TL;DR

**Structure:**

```
[Sentence 1]    — the thesis / core argument
[Sentence 2]    — the key insight or supporting evidence
[Sentence 3]    — the takeaway (what to do or think differently)
```

**Rules:**

- **2–3 sentences.** No more. If it needs four sentences, one of the first three is doing too much
  work — split or cut.
- **Must stand alone.** Someone who has never seen the post should understand the point completely.
- **Active voice.** "X causes Y" not "Y is caused by X."
- **No jargon unless the audience expects it.** If the post is for practitioners who use the jargon
  daily, keep it. If not, swap for plain language.
- **Capture the thesis, not the narrative.** The TL;DR is the distilled argument, not a summary of what happens. Don't open with "This post is about…" — state the actual claim. Pick one takeaway.

---

### Format 4: Newsletter Blurb

**Structure:**

```
[Tension or hook]       — a question, problem, or tension the post resolves
[Brief context]         — enough setup to care
[Payoff hint]           — gesture at the insight without giving it away
[Link placeholder]      — [Read more →]
```

**Rules:**

- **3–5 sentences.** Enough to create intrigue; not enough to replace the click.
- **Create tension, not summary.** The best newsletter blurbs pose a question the post answers, or
  name a problem the post solves. Don't summarise the post — tease it. The reader should finish the
  blurb wanting to know what happens next or what the answer is.
- **Don't give away the key insight.** If the post's thesis is "X is actually the wrong approach,"
  the blurb should raise the problem X is supposed to solve — not reveal that X is wrong. That's
  the click.
- **End with `[Read more →]`.** Placeholder for the actual post link.

---

## Output Format

When producing a single format: output it directly, no preamble needed beyond a format label.

When producing multiple formats: use a `##` heading for each, in this order:

```
## Twitter/X Thread
[content]

## LinkedIn Post
[content]

## TL;DR
[content]

## Newsletter Blurb
[content]
```

After delivering the output(s), ask: *"Anything you'd like adjusted — tone, length, a specific
tweet, the LinkedIn opener?"*

Also offer **one proactive observation** — something you'd refine even if they're satisfied.
Common candidates:
- Hook tweet could be stronger (if it reads as a summary rather than a standalone punch)
- LinkedIn opener buries the lead (if the first line is context rather than insight)
- TL;DR is vague (if the takeaway is abstract — flag and offer a sharper version)
- Newsletter blurb gives away too much (if the key insight is revealed before the click)

---

## Edge Cases Summary

| Situation | Action |
|-----------|--------|
| Post has no clear thesis | Flag it; offer to sharpen the post first or proceed as-is |
| Post too short to thread | Flag it; recommend LinkedIn/TL;DR instead |
| User wants all four formats | Produce all four, clearly labelled |
| User specifies format(s) | Produce immediately — no format-selection step needed |
| Post is highly technical | Keep the technical language — don't dumb down for LinkedIn or the thread |
| Post is personal/emotional | Preserve the honest voice — don't make it corporate or generic |
