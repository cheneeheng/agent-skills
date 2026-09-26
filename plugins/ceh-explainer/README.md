# ceh-explainer

Claude Code plugin for explaining a topic **one part at a time**, using **only what the accessible
workspaces contain**. Every claim cites the file it came from, gaps are named rather than guessed,
and each part is either standalone or opens by restating the one fact it needs from an earlier
part.

## Skill

| Skill | Description |
|-------|-------------|
| `explain-in-chunks` | Check the workspace covers the topic, plan it as 3–7 ordered parts, deliver one cited part per turn, and handle "next", questions, jumps, and inserted foundation parts between them |

Invoke manually:

```
/ceh-explainer:explain-in-chunks <topic>
```

Or load automatically when you say:
- `"explain X to me step by step"`
- `"walk me through how X works here"`
- `"explain this in chunks — don't dump it all at once"`
- `"explain X using only what's in the repo"`

## How a series runs

| Step | What happens |
|------|--------------|
| Coverage check | Searches every readable workspace for the topic. Nothing found → stops and lists where it looked. Fragments → offers a plan over the covered aspects only |
| Plan | 3–7 parts, each answering one question, foundations first; each marked *standalone* or *builds on Part N* |
| Deliver | The plan plus Part 1, then one part per turn — heading, link line, body, `Sources:` with `path:line`, and a `Next:` line |
| Between parts | "next", re-explain a part differently, answer a question, jump, or insert a missing foundation part |
| Close | One-line recap per part, plus the gaps the workspace did not cover |

Long series (more than 5 parts, or "I'll come back to this") also persist their plan to
`.agents_workspace/explanations/<topic-slug>.md` so a later session can resume.

This plugin is standalone: it has no dependencies and belongs to no scenario bundle.
