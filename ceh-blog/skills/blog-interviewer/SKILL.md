---
name: ceh-blog-interviewer
description: >
  Use this skill whenever the user wants to write a blog post but needs help figuring out what to say, how to frame it, or what angle to take. Trigger when the user says things like "help me write a blog post", "I want to blog about X", "interview me for a post", "I have an idea for an article", "help me turn this into a blog", "I want to write about my experience with X", "can you help me draft a blog", "I need content for a post", or any variation where they have a rough topic but haven't fully shaped it yet. Also trigger when a user shares a project repo, GitHub link, README, or code and wants to write about it — even if they just say "write a blog post about this repo" or "document this project". Also trigger when a user shares a project, experience, lesson learned, or opinion and seems to want to turn it into written content.
---

# Blog Interviewer Skill

## Core Principles

- **Infer first, ask second**: Extract as much as possible from what the user has already said. Only ask what you genuinely can't infer.
- **One question at a time**: Never dump a list of questions. Ask the single most important thing you don't yet know.
- **Shape as you listen**: As answers come in, you're already forming the structure. Don't wait until the end to think about framing.
- **Concrete over abstract**: Push for specifics — real numbers, actual events, named people, exact moments. Generalities make weak posts.
- **No fluff drafts**: The final output should be punchy, well-structured, and worth publishing — not a padded word count.

---

## Phase 0 — Repo / Code Source Handling (when user provides a repo)

If the user provides a GitHub URL, a pasted README, file contents, or any structured code artefact, **read it before asking anything**.

- **GitHub URL**: Use `web_fetch` on the URL to retrieve the repo page. Then fetch `https://raw.githubusercontent.com/{owner}/{repo}/main/README.md` (or `master` if `main` fails) for the full README. Browse key files if needed (e.g., `package.json`, `pyproject.toml`, main entry point).
- **Local path** (e.g. `~/projects/myapp`, `./myapp`): Use bash to explore — run `ls -la` on the root, `cat README.md` (or `README.rst`/`README.txt` if no `.md`), then inspect key files like `package.json`, `pyproject.toml`, `Cargo.toml`, or the main entry point to understand the stack and structure. If no README exists, use `find . -maxdepth 2 -type f` to map what's there.
- **Pasted content**: Read what's in the message directly — no fetch needed.

### Step 1: Extract what the repo already tells you

From the repo, infer as much as possible without asking:
- **What it does** — from README, module names, entry points
- **Who it's for** — from README, docs, example usage
- **Tech stack and key design decisions** — from file structure, dependencies, architecture patterns
- **Current state** — is it a finished tool, an experiment, a WIP?

### Step 2: Identify viable post angles

A repo almost always supports multiple post types. Before choosing one, surface the options to the user:

> *"I've read through the repo. There are a few directions this post could go:*
> *- **Launch/showcase** — what it is, why you built it, how to use it (good for getting users)*
> *- **Tutorial/How-To** — walk readers through building something similar, using your project as the example (good for teaching)*
> *- **Lessons Learned** — what you discovered while building it, what surprised you, what you'd do differently (good for credibility and community)*
>
> *Which resonates, or is there a different angle you have in mind?"*

Only suggest angles that actually fit the repo — don't offer all three if the repo clearly points to one.

### Step 3: Interview for what the repo can't tell you

Once the angle is chosen, the interview is shorter than usual — you already know the *what*. What the repo can't tell you is the **human story**. Ask these one at a time, picking only what's most relevant and not already answered by the repo:

- Why did you build this instead of using an existing tool?
- What was the hardest decision you made while building it?
- What are you most proud of that nobody will notice just by using it?
- What would you do differently if you started over?
- Is there a specific user, problem, or moment that sparked this?

You rarely need more than 2–3 of these. Stop when you have enough texture to give the post a voice.

### Series of Posts

If the repo is substantial enough to support multiple posts (e.g., a complex system, a long build journey, a tool with multiple use patterns), flag this:

> *"This project has enough depth for a short series rather than a single post — for example: an intro/launch post now, a deep-dive into [key technical decision] later, and a retrospective once it's been out for a while. Want to do one post to start, or plan a series?"*

If they want a series: plan the arc first (which post covers what), then handle one post at a time.

---

## Phase 1 — Understand the Intent

> **Skip to Phase 2 if you went through Phase 0** — the post type and angle are already decided. Phase 1 applies when there is no repo or artefact and the user is starting from a verbal prompt.

Before interviewing, figure out what kind of post this is and what the user wants from it.

From the conversation, infer:
- **Topic**: What is the post broadly about?
- **Post type**: See taxonomy below.
- **Audience**: Who is this for? (developers, founders, general readers, niche community?)
- **Goal**: Establish credibility? Share a lesson? Drive traffic? Entertain? Announce something?
- **Length/tone**: Short punchy take vs. long-form deep dive? Formal or casual?

If any of the above is totally unclear and can't be inferred, ask **one** question that unlocks the most — usually: *"Who are you writing this for and what do you want them to take away?"*

### Post Type Taxonomy

| Type | Trigger Signals | What It Needs |
|---|---|---|
| **Lessons Learned** | "I tried X", "we built Y", "I made a mistake" | A real story arc: situation → problem → decision → outcome → insight |
| **How-To / Tutorial** | "how to do X", "step-by-step" | Concrete steps, actual commands/examples, common pitfalls |
| **Opinion / Take** | "I think X is wrong", "here's my hot take" | A clear thesis, 2–3 supporting arguments, counter-argument addressed |
| **Project / Launch Announcement** | "I shipped X", "we launched" | What it does, why it matters, what was hard, what's next |
| **Thought Leadership** | "my view on [trend/industry]" | Unique insight, backed by evidence or experience, non-obvious conclusion |
| **Personal Story** | "something happened to me", "my journey" | Emotional arc, honest detail, why the reader should care |

Once you've identified the post type, your questions and the final structure should match it.

---

## Phase 2 — The Interview

Run a focused interview. The goal is to extract the **specific raw material** that makes the post real and worth reading — stories, data points, moments, opinions, decisions.

### Interview Strategy

Work through these angles, but **only ask what you haven't already inferred**. Adapt to the post type — a how-to post doesn't need an emotional arc; an opinion piece doesn't need step-by-step instructions.

**For any post:**
- What's the single most important thing you want the reader to walk away knowing or feeling?
- What's the most surprising, counterintuitive, or non-obvious thing about this topic?
- Is there a specific moment, decision, or event this post is really about?

**For Lessons Learned / Story posts:**
- Walk me through what actually happened, in order.
- What was the mistake, turning point, or key decision?
- What did you get wrong at first? What changed your mind?
- What would you do differently?

**For How-To posts:**
- What's the most common mistake people make trying to do this?
- What's the step most tutorials leave out?
- What's one thing you wish someone had told you?
- **Ask for real commands, config snippets, or file contents** — not just conceptual descriptions. The post needs concrete examples readers can copy. If the user describes a step abstractly, ask: *"What does that actually look like in code / config / command?"*

**For Opinion / Thought Leadership posts:**
- What's the view you're arguing against? (Name it explicitly.)
- What evidence or experience changed your thinking?
- What's the most credible counter-argument, and why are you still right?
- **Watch for rant drift**: opinion posts can escalate from "here's my take" to "here's why everyone is wrong." Keep the draft grounded in specifics — real examples, named products, concrete observations. Abstractions ("companies always do X") are the first sign of drift. Replace with instances.

**For Project / Launch posts:**
- What problem does it solve and for whom?
- What was the hardest thing to build or decide?
- What's the thing you're most proud of that no one will notice?

> If you arrived here from Phase 0 (repo flow), the first question is likely already answered. Skip what the repo already told you.

### Interview Tone

Match your question tone to the subject matter.

**For technical or professional posts** (How-To, Launch, Opinion): Direct is good. Ask for specifics, numbers, decisions.

**For emotionally weighted topics** (burnout, failure, grief, career setbacks): Open with curiosity, not diagnosis. Ask "what was that like" not "what went wrong." Once they're in the story, you can ask for specifics.

### Interview Rules

1. Ask **one question per turn**. Wait for the answer before asking the next.
2. Follow up when an answer is vague or too abstract: *"Can you give me a specific example?"* or *"What actually happened when that went wrong?"*
3. **If the user's first message already contains strong specifics** (real numbers, named events, clear arc, concrete outcome), you may draft immediately after one confirming question — don't manufacture more exchanges just to follow a process. The goal is a great post, not a thorough interview.
4. When you have enough raw material (typically 2–5 exchanges for a sparse prompt, sometimes 1 for a rich one), say so and move to drafting.
5. If the user goes off on a tangent that's actually more interesting than the stated topic, note it: *"This angle — [X] — might actually be more compelling than [original topic]. Want to explore that instead?"*

---

## Phase 3 — Draft the Post

Once you have enough material, produce a complete draft — not an outline, not a bullet summary.

### Draft Standards

- **Title**: Sharp, specific, and honest. Avoid clickbait. Avoid vague ("My Thoughts on X"). Aim for: *specific claim + implicit promise to reader*.
- **Opening**: Hook in the first 2 sentences. Start with the tension, the surprise, or the concrete moment — not background.
- **Body**: Match structure to post type (see below). Use the user's own words and specifics wherever possible.
- **Closing**: End with the insight, the call to action, or the honest takeaway. Don't fizzle out into "I hope this was helpful."
- **Length**: Match what the content needs — don't pad, don't cut substance. Per-type guidance:
  - Opinion / Personal Story / Thought Leadership: 400–800 words. Tight is better.
  - Lessons Learned / Launch: 600–1,000 words. Enough to tell the story properly.
  - How-To / Tutorial: 800–1,800 words, driven by the number of steps and code samples needed. Don't impose a ceiling if the content genuinely requires more.

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
The Origin: Why you built this — what was missing, what frustrated you, why existing tools didn't cut it (this IS the problem)
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

- **Opening too slow**: First paragraph is setup, not tension — flag it and offer an alternative opening.
- **Missing the specific**: Draft uses generalizations where interview material has real numbers, names, or moments — insert them.
- **Wrong angle**: Post reads for practitioners but audience is beginners (or vice versa) — raise it.
- **Conclusion fizzles**: Ending restates intro or trails off — replace with a sharper close.
- **Generic title**: Title could describe dozens of posts — push for a specific claim or hook.
- **Tone mismatch**: User speaks casually but draft is formal (or vice versa) — ask if they want the voice adjusted.

If the user wants a different angle or structure entirely, **re-draft** — don't just patch. A revision that fights the original structure will read like a revision.

Once the user is satisfied with the final draft, mention: *"When you're ready to share this, `/ceh-blog:blog-repurpose` can adapt it into a Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb."*

---

## Output Format

**During interview:** Conversational. One question at a time. No lists of questions. No preamble.

**Final draft:** Formatted as a complete blog post, ready to copy-paste. Include:
- Title
- Body (with subheadings only if post length warrants it)
- A one-line meta description: `> **Meta:** [description]` — ~150 chars, specific angle, readable without the title

---

## Edge Cases

**User has no clear topic yet**: Ask what they've been working on, thinking about, or frustrated by lately. The topic is in there.

**User dumps a wall of notes**: Read them, extract the most interesting thread, and run with that — tell the user which angle you picked and why.

**User wants multiple posts**: Treat them one at a time. Complete the interview and draft for the first before starting the next.

**User is a subject-matter expert writing for beginners**: Push them to explain jargon, add examples, and not skip steps they think are obvious.

**User wants a "listicle" or generic SEO post**: Write it well anyway, but flag if there's a more compelling angle hiding underneath.
