---
name: blog-interviewer
description: Interview the user to shape a blog post, then draft it. Trigger when the starting point is only a topic, idea, project, repo, or experience — nothing written yet. Signals: "help me write a blog post", "interview me for a post", "I want to blog about X", "write a post about this repo", "I have an idea for an article", or a GitHub link/repo/README to turn into a post. Not for ready-made notes or an outline (use blog-writer); not for an existing draft to improve (use blog-editor).
---

# Blog Interviewer Skill

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

- **Infer first, ask second**: extract everything the user has already said; only ask what you genuinely can't infer.
- **One question at a time**: never dump a list. Ask the single most important thing you don't yet know.
- **Shape as you listen**: form the structure as answers come in — don't wait until the end.
- **Concrete over abstract**: push for specifics — real numbers, actual events, named people, exact moments.
- **Capture quotes verbatim**: the user's phrasing *is* the voice. A usable line ("first impression is a lot cleaner and smooth") goes into the draft nearly word-for-word — store it, don't paraphrase it.
- **No fluff drafts**: specific, well-structured, worth publishing — not a padded word count.

---

## Phase 0 — Repo / Code Source Handling (when user provides a repo)

If the user provides a GitHub URL, pasted README, file contents, or any code artefact, **read it before asking anything**.

- **GitHub URL**: `web_fetch` the URL, then `https://raw.githubusercontent.com/{owner}/{repo}/main/README.md` (`master` if `main` fails). Browse key files if needed (`package.json`, `pyproject.toml`, main entry point).
- **Local path**: explore with bash — `ls -la`, `cat README.md` (or `.rst`/`.txt`), then key manifests/entry points for stack and structure. No README: `find . -maxdepth 2 -type f`.
- **Pasted content**: read it directly.

### Step 1: Extract what the repo already tells you

Infer without asking: **what it does** (README, module names, entry points); **who it's for** (docs, example usage); **stack and key design decisions** (structure, dependencies); **current state** (finished tool, experiment, WIP?).

### Step 1.5: Read the blog, not just the repo (Series Awareness)

If the post is going into an existing blog, read the previous posts before asking anything — especially the latest episode in the same series. Then:

- **Pick up the thread**: if the last post ended on a live thread, ask *"the last post ended on X — is this the post that answers it?"* If yes, that thread is the new post's opening.
- **Pin chronology**: ask *"When did this happen, relative to the last post?"* — one timestamp question prevents continuity bugs (wrong versions, events out of order).
- **Check continuity facts** against earlier episodes: versions, dates, what the reader already knows. Don't re-tell a story a previous episode owns — call back in a sentence and link.
- **Leave a thread**: plan what this episode leaves open; closure instead if the series is finished.

Applies in the no-repo flow too — if the user has an existing blog, read it before interviewing.

### Step 2: Identify viable post angles

A repo usually supports multiple post types. Surface only the angles that actually fit:

> *"I've read through the repo. There are a few directions this post could go:*
> *- **Launch/showcase** — what it is, why you built it, how to use it*
> *- **Tutorial/How-To** — walk readers through building something similar*
> *- **Lessons Learned** — what you discovered, what surprised you, what you'd do differently*
>
> *Which resonates, or is there a different angle you have in mind?"*

### Step 3: Interview for what the repo can't tell you

The repo gives you the *what*; interview for the **human story** — one at a time, only what the repo hasn't answered:

- Why build this instead of using an existing tool?
- Hardest decision while building it?
- What are you most proud of that nobody will notice?
- What would you do differently starting over?
- A specific user, problem, or moment that sparked it?

2–3 of these usually suffice. Stop when there's enough texture for a voice.

### Series of Posts

If the repo can support multiple posts (complex system, long build journey, multiple use patterns), flag it:

> *"This project has enough depth for a short series — e.g. an intro post now, a deep-dive into [key decision] later, a retrospective once it's been out a while. One post to start, or plan a series?"*

If a series: plan the arc first (which post covers what), then one post at a time.

---

## Phase 1 — Understand the Intent

> **Skip to Phase 2 if you went through Phase 0** — type and angle are decided. Phase 1 is for a verbal prompt with no repo or artefact.

Infer: **topic**; **post type** (taxonomy below); **audience**; **goal** (credibility, lesson, traffic, entertainment, announcement); **length/tone**. If genuinely uninferable, ask **one** question that unlocks the most — usually *"Who are you writing this for and what do you want them to take away?"*

### Post Type Taxonomy

| Type | Trigger Signals | What It Needs |
|---|---|---|
| **Lessons Learned** | "I tried X", "we built Y", "I made a mistake" | Story arc: situation → problem → decision → outcome → insight |
| **How-To / Tutorial** | "how to do X", "step-by-step" | Concrete steps, actual commands/examples, pitfalls |
| **Opinion / Take** | "I think X is wrong", "here's my hot take" | Clear thesis, 2–3 arguments, counter-argument addressed |
| **Project / Launch** | "I shipped X", "we launched" | What it does, why it matters, what was hard, what's next |
| **Thought Leadership** | "my view on [trend/industry]" | Unique insight backed by evidence, non-obvious conclusion |
| **Personal Story** | "something happened to me", "my journey" | Emotional arc, honest detail, why the reader should care |

Questions and final structure should match the identified type.

---

## Phase 2 — The Interview

Extract the **specific raw material** that makes the post real: stories, data points, moments, opinions, decisions. Only ask what you haven't inferred; adapt to the post type.

**For any post:**
- The single most important thing the reader should walk away knowing or feeling?
- The most surprising or counterintuitive thing about this topic?
- A specific moment, decision, or event this post is really about?

### The Four Story Beats (required for story-voice posts)

For personal-voice posts (Lessons Learned, Personal Story, most Launch and Opinion), facts are not enough — interview for these four beats, one at a time, skipping any the user already gave:

1. **The turn** — what happened between not-knowing and knowing? How did the realization arrive?
2. **The moment** — your reaction when it happened?
3. **The verdict** — the honest current state; allowed to be unresolved or reserved.
4. **The thread** — what question is still open? (This becomes the post's ending.)

**For Lessons Learned / Story posts:** what actually happened, in order; the mistake/turning point/key decision; what you got wrong at first and what changed your mind; what you'd do differently.

**For How-To posts:** the most common mistake; the step most tutorials leave out; the thing you wish someone had told you. **Ask for real commands, config, or file contents** — if a step is described abstractly, ask *"What does that actually look like in code / config / command?"*

**For Opinion / Thought Leadership posts:** the view you're arguing against (named explicitly); the evidence or experience that changed your thinking; the most credible counter-argument and why you're still right. **Watch for rant drift**: abstractions ("companies always do X") are the first sign — replace with named instances.

**For Project / Launch posts:** what problem, for whom; the hardest thing to build or decide; the thing you're most proud of that no one will notice.

> Arriving from Phase 0: skip what the repo already told you.

### Interview Tone

**Technical/professional posts** (How-To, Launch, Opinion): direct — ask for specifics, numbers, decisions.

**Emotionally weighted topics** (burnout, failure, grief, setbacks): open with curiosity, not diagnosis — "what was that like", not "what went wrong". Specifics once they're in the story.

### Interview Rules

1. **One question per turn.** Wait for the answer.
2. Follow up on vague or abstract answers: *"Can you give me a specific example?"*
3. **Offer hypothesis options when you can form plausible guesses.** Instead of *"How did you figure it out?"*: *"Did Claude critique it, did you read something, or did it crystallize on its own?"* Correcting a concrete guess is easier than composing from scratch — and gets a sharper reply. Open questions when you have no good hypotheses.
4. **Handle answer drift**: if the user answers a different question than asked, keep the answer — it's real material. Decide whether the original beat is still needed; if so, re-ask **once at most**, rephrased. Don't interrogate.
5. **Store quotable phrasing verbatim** as it arrives; mark the lines to use nearly word-for-word.
6. **If the first message already has strong specifics** (real numbers, named events, clear arc), draft after one confirming question — don't manufacture exchanges. The goal is a great post, not a thorough interview.
7. When you have enough (typically 2–5 exchanges; sometimes 1), say so and draft. For story-voice posts, "enough" includes the four beats — or an explicit note that a beat is missing, never an invented one.
8. If a tangent is more interesting than the stated topic: *"This angle — [X] — might be more compelling than [original]. Explore that instead?"*

---

## Phase 3 — Draft the Post

Produce a complete draft — not an outline, not a bullet summary.

### Draft Standards

- **Title**: sharp, specific, honest. No clickbait, no vague "My Thoughts on X". Aim for: *specific claim + implicit promise to reader*.
- **Opening**: inside a moment or a thought within the first 2 sentences — not background, not a product pitch.
- **Body**: match structure to post type (below). Use the user's own words — quotable interview lines go in nearly verbatim.
- **Closing**: the open thread (see Voice). No "I hope this was helpful", no manufactured takeaway/lesson/CTA.
- **Length**: what the content needs — don't pad, don't cut substance.
  - Opinion / Personal Story / Thought Leadership: 400–800 words. Tight is better.
  - Lessons Learned / Launch: 600–1,000 words.
  - How-To / Tutorial: 800–1,800 words, driven by steps and code samples — no ceiling if genuinely required.

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
The Origin: Why you built this — what was missing, what frustrated you, why existing tools didn't cut it (this IS the problem)
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
- **Missing the specific**: draft generalizes where the interview has real numbers, names, or moments — insert them.
- **Wrong angle**: post reads for practitioners but audience is beginners (or vice versa).
- **Conclusion fizzles or lectures**: ending restates the intro, trails off, or lands on a tidy takeaway/CTA — replace with the genuinely open thread or a reserved verdict.
- **Influencer tells**: any banned tell present — rewrite quieter, per Voice.
- **Continuity slip**: a version, date, or fact contradicts an earlier episode — fix against the previous posts.
- **Paraphrased voice**: a quotable interview line got smoothed into generic prose — restore the user's phrasing.
- **Generic title**: could describe dozens of posts — push for a specific claim or hook.
- **Tone mismatch**: user speaks casually, draft is formal (or vice versa) — ask if they want the voice adjusted.

If the user wants a different angle or structure, **re-draft** — a revision that fights the original structure reads like a revision.

Once the user is satisfied, mention: *"When you're ready to share this, `/ceh-blog:blog-repurpose` can adapt it into a Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb."*

---

## Output Format

**During interview:** conversational, one question at a time, no lists, no preamble.

**Final draft**: complete post, ready to copy-paste — title; body (subheadings only if length warrants); one-line meta description `> **Meta:** [description]` — ~150 chars, specific angle, readable without the title.

---

## Edge Cases

**No clear topic yet**: ask what they've been working on, thinking about, or frustrated by lately. The topic is in there.

**Wall of notes**: extract the most interesting thread and run with it — say which angle you picked and why.

**Multiple posts wanted**: one at a time — complete the first interview and draft before starting the next.

**Expert writing for beginners**: push them to explain jargon, add examples, and not skip "obvious" steps.

**Listicle / generic SEO post**: write it well anyway, but flag a more compelling angle if one is hiding underneath.
