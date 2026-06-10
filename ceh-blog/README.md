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

Invoke manually:

```
/ceh-blog:blog-interviewer
/ceh-blog:blog-writer
/ceh-blog:blog-editor
/ceh-blog:blog-repurpose
```

**blog-interviewer** loads automatically when you say:
- `"help me write a blog post"`
- `"I want to blog about X"`
- `"interview me for a post"`
- `"I have an idea for an article"`
- `"write a blog post about this repo"`

Also triggers when a user shares a project repo, README, or code and wants to write about it.

**blog-writer** loads automatically when you say:
- `"turn this into a blog post"`
- `"write a post from these notes"`
- `"draft a blog post from this"`
- `"here's my outline, write the post"`

**blog-editor** loads automatically when you say:
- `"edit this draft"`
- `"polish this post"`
- `"this post feels off"`
- `"make this better"`
- `"review my draft"`

**blog-repurpose** loads automatically when you say:
- `"turn this into a thread"`
- `"make a LinkedIn post from this"`
- `"repurpose this post"`
- `"write a TL;DR for this"`
- `"make a newsletter blurb"`

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
