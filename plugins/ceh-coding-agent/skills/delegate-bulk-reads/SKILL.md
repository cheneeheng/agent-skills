---
name: delegate-bulk-reads
description: >-
  How to delegate a read to the bulk-reader subagent and what to do with its answer. Load this
  before dispatching bulk-reader, or when a PreToolUse guard has denied a Read or a bash
  cat/head/tail, or when about to answer one question by reading several large files. Covers
  writing the delegation prompt so the answer is usable, and the verification rules that apply
  afterwards: the files were never seen in this context, so the summary is a lead, not evidence.
  Load it before acting on a subagent's summary — editing, refactoring, or reporting a claim to
  the user based on lines nobody here has read is the failure mode this exists to prevent.
---

# Delegate Bulk Reads

The `bulk-reader` subagent reads on Haiku and returns anchored bullets. The file contents never
enter this context, so its answer is all there is to work with. Its own description says when it
is the wrong tool; this covers how to drive it and how to treat what comes back.

## Write the delegation prompt

```
Agent(
  subagent_type: "bulk-reader",
  description: "Read auth flow files",
  prompt: """
  QUESTION: Which methods write to the database, and what transaction boundaries do they use?

  FILES:
  - src/service/UserService.java
  - src/db/TransactionManager.java

  Answer only the question. Anchor every claim with path:line.
  """
)
```

- **One question per call.** A delegation asking three things returns three shallow answers.
- **Name explicit paths.** If they are unknown, that is a Glob/Grep job first — those are cheap
  and return no file contents.
- **Prefer two narrow calls to one broad one.** Re-sending the same paths with a different
  question costs nothing here, since the files go to the worker and never come back.
- **Never ask it to edit.** Writing from a summary is how wrong changes get made.

## Trust the anchors, not the prose

The reply has three sections: `## Answer` with every claim anchored `path:line`,
`## Not found / uncertain`, and `## Coverage`.

- **Read the anchored lines before acting on them.** Before an edit, a refactor, or a claim
  reported to the user, `Read(path, offset=..., limit=...)` the region. These files were never
  seen here, so judging whether the summary "looks right" is not a check.
- **A bullet with no anchor is unverified.** Re-delegate with a narrower question instead of
  building on it.
- **`Not found / uncertain` matters more than `Answer`.** Silent omission is the dominant failure
  mode of a summarizing worker: an answer missing a case looks identical to a complete one.
- **Confirm empty answers with a cheap Grep.** "No matches" can mean the pattern is absent or that
  the worker read the wrong thing.
