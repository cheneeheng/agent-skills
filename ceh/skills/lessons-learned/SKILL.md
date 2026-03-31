---
name: "lessons-learned"
description: >
  Use this skill to extract lessons learned from the current conversation and append them to
  LESSONS_LEARNED.md in the working directory. Triggers when the user asks to "extract lessons
  learned", "do a retrospective", "capture what went wrong", "write up lessons learned", or
  any similar request to reflect on mistakes, misunderstandings, or corrections made during the
  session. Also trigger proactively at the end of a session that involved notable errors or
  rework — the user may not think to ask, but the lessons are worth capturing.
---

# Lessons Learned Extractor

Review the full conversation history, identify moments where something went wrong or required
correction, and append structured lessons to `LESSONS_LEARNED.md` in the current working directory.

---

## What counts as a lesson

Scan the conversation for:

- **Corrections** — the user had to ask you to redo, move, rename, or restructure something
- **Failed commands** — a tool call errored and required a follow-up to fix it
- **Misunderstood requirements** — you built something in the wrong place, wrong format, or wrong scope
- **Wrong assumptions** — you assumed something that turned out to be false
- **Sequencing mistakes** — you did steps out of order or skipped a prerequisite

Do NOT capture:
- Things that worked correctly the first time
- Routine tool use (reading files, running standard commands)
- User preference changes that weren't errors (e.g. "actually let's rename this")

The target audience for each lesson is a future LLM reading it cold — write so the next session
avoids repeating the same mistake, not as a narrative for the human.

---

## Output format

Each lesson uses this structure:

```markdown
## YYYY-MM-DD — <short title describing the mistake>

**What happened:** One or two sentences describing the concrete mistake or misunderstanding
that occurred in this session.

**Lesson:** One or two sentences stating the actionable rule or check to apply next time
to avoid repeating this.
```

- Use today's actual date (from system context or `date` command if needed)
- Title should name the mistake, not the fix (e.g. "mv requires parent directory to exist", not "use mkdir before mv")
- Keep each entry under 6 sentences total — dense and specific beats thorough and vague
- Prefer file paths, command names, and exact decisions over abstract descriptions

---

## File handling

1. Check whether `LESSONS_LEARNED.md` exists in the current working directory
2. If it does not exist, create it with this header before appending:
   ```markdown
   # Lessons Learned

   ---
   ```
3. Append new lessons after any existing content — never overwrite or reorder existing entries
4. Separate each lesson from the previous content with a blank line

---

## After writing

Tell the user:
- How many lessons were added
- The title of each one (one line each)
- If no lessons were found, say so explicitly rather than writing a placeholder entry
