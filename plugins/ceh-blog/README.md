# ceh-blog

Claude Code plugin for writing compelling, publishable blog posts — whether you're starting from a half-formed idea or already have raw material ready to shape.

## Voice

Posts come out in a **personal**, first-person voice — not influencer style. No CTA endings, no
tidy takeaway sign-offs, no aphoristic one-liners; posts end on the honest open thread (what's
unresolved, what comes next), and a reserved verdict is a valid ending. The blog is treated as
**serials**: each project is a series, each post an episode that picks up the previous episode's
thread, keeps continuity facts straight, and leaves a thread of its own. If the target repo's
`CLAUDE.md` defines a blog voice, it overrides the built-in templates.

## Skills

| Skill | Description |
|-------|-------------|
| `blog-interviewer` | Interview the user to extract the core story or argument, then produce a full draft |
| `blog-writer` | Draft straight from existing notes, bullets, or outline — no interview |
| `blog-editor` | Diagnose and polish an existing draft — diagnosis first, then a full revised version |
| `blog-repurpose` | Adapt a finished post into Twitter/X thread, LinkedIn post, TL;DR, or newsletter blurb |

These skills are designed for **manual invocation** — pick the one matching your starting point:

```
/ceh-blog:blog-interviewer   # only a topic, idea, repo, or experience — nothing written yet
/ceh-blog:blog-writer        # notes, bullets, or an outline ready — no interview needed
/ceh-blog:blog-editor        # a draft in prose that needs diagnosis and revision
/ceh-blog:blog-repurpose     # a finished post to adapt for other channels
```

They can still load automatically when a request clearly matches ("help me write a blog post about this repo", "turn these notes into a post", "edit this draft", "make a thread from this"), but manual invocation is the primary path.

## What It Produces

A complete, publication-ready blog post with:
- Title
- Structured body matched to post type (Lessons Learned, How-To, Opinion, Launch, Thought Leadership, Personal Story)
- Meta description for SEO/sharing

## Post Types Supported

| Type | When to use |
|------|-------------|
| Lessons Learned | "I tried X", "we built Y", "I made a mistake" |
| How-To / Tutorial | "how to do X", "step-by-step" |
| Opinion / Take | "I think X is wrong", "here's my hot take" |
| Project / Launch | "I shipped X", "we launched" |
| Thought Leadership | "my view on [trend/industry]" |
| Personal Story | "something happened to me", "my journey" |
