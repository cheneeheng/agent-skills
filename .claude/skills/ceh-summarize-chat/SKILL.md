---
name: "ceh-summarize-chat"
description: >
  Use this skill to summarize the current conversation history into a structured markdown document
  that an LLM can read and act on in a future session. Produces a concise, factual summary covering
  what was worked on, decisions made, problems encountered, solutions applied, and current state.
  Trigger when the user asks to "summarize the chat", "summarize the conversation", "create a
  session summary", "summarize what we did", or any similar request to capture the current session
  as a reusable context document.
---

# Chat History Summarizer: Structured Markdown Summary for LLM Context, Covering Session Goal, Actions Taken, Decisions Made, Problems and Solutions, Current State, and Pending Work

---

## Purpose

Produce a summary that lets a future LLM session pick up exactly where this one left off — without re-reading the full conversation. The summary must be factual, structured, and optimized for machine reading, not narrative prose.

---

## Output Format

Return the summary as a markdown document using this structure. Only include sections that are relevant — omit empty ones.

```markdown
# Session Summary
**Date:** YYYY-MM-DD
**Branch / Repo:** <branch name and repo if known>

## Goal
One or two sentences: what was the user trying to accomplish in this session?

## What Was Done
Ordered list of actions taken, from first to last. Each item is one line.
- Action 1
- Action 2
- ...

## Decisions Made
Decisions that affect future work — naming conventions chosen, locations agreed on, approaches selected.
| Decision | Rationale |
|----------|-----------|
| ... | ... |

## Problems and Solutions
Issues that came up and how they were resolved. Only include non-obvious problems — skip routine steps.
| Problem | Solution |
|---------|----------|
| ... | ... |

## Current State
What is the repo / codebase in right now? What files were created, changed, or deleted?
- Created: `path/to/file` — purpose
- Modified: `path/to/file` — what changed
- Deleted: `path/to/file`

## Pending / Next Steps
Work that was discussed but not completed, or logical next actions.
- [ ] Item

## Key Facts for Next Session
Non-obvious facts a future LLM must know to avoid repeating mistakes or asking redundant questions.
- Fact 1
- Fact 2
```

---

## Writing Rules

**Be factual, not narrative.** Write what happened, not a story about it. Avoid phrases like "we explored" or "the user wanted to" — just state what was done.

**One fact per line.** Dense bullet points are easier for an LLM to parse than paragraphs.

**Prefer specifics over generalities.** File paths, command names, and exact decisions are more useful than vague descriptions.
- Good: `Skill name field must be lowercase letters, numbers, and hyphens matching the folder name`
- Bad: `There were some naming constraints to be aware of`

**Current State is the most important section.** A future LLM needs to know exactly what exists now. List every file that was created, modified, or deleted.

**Key Facts is for gotchas.** If something caused a mistake or required correction during the session, it belongs here so the next session does not repeat it.

**Omit the obvious.** Do not summarize routine tool use, standard git operations, or information derivable from reading the files directly.

---

## Tone and Length

- Use imperative or declarative statements, not questions or hedging
- Aim for the minimum length that preserves full context — no padding
- The summary should be readable in under 2 minutes by a human, and parseable in one pass by an LLM
