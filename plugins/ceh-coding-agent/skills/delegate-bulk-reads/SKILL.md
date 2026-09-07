---
name: delegate-bulk-reads
description: >-
  How to delegate a read to the bulk-reader subagent and what to do with its answer. Load this
  before dispatching bulk-reader, or when a PreToolUse guard has denied a Read or a bash
  cat/head/tail, or when about to answer one question by reading several large files. Covers
  writing the delegation prompt so the answer is usable, and the verification rules that apply
  afterwards: the files were never seen in this context, so the summary is a lead, not evidence.
  Load it before acting on a subagent's summary — editing, refactoring, or reporting a claim to
  the user based on lines nobody here has read is the failure mode this exists to prevent. Not for
  a file you are about to edit, debug or review: that wants a direct Read with offset/limit, since
  a summary cannot give an edit the exact text it needs.
---

# Delegate Bulk Reads

The `bulk-reader` subagent reads on Haiku and returns anchored bullets. The file contents never
enter this context, so its answer is all there is to work with. Its own description says when it
is the wrong tool; this covers how to drive it and how to treat what comes back.

## Shape the call

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

**Prefer two narrow calls to one broad one.** Re-sending the same paths with a different question
costs nothing here, since the files go to the worker and never come back — the second call is
priced like the first, not like a re-read. This is the rule that does not carry over from ordinary
delegation, where re-sending context is the expensive part. So when a follow-up question occurs to
you, ask it; do not bundle it into the first call to save a trip you are not paying for.

## Trust the anchors, not the prose

The reply has three sections: `## Answer` with every claim anchored `path:line`,
`## Not found / uncertain`, and `## Coverage`.

- **Read the anchored lines before acting on them.** Before an edit, a refactor, or a claim
  reported to the user, `Read(path, offset=..., limit=...)` the region. These files were never
  seen here, so judging whether the summary "looks right" is not a check. An anchor can point at a
  real line and still describe it backwards — the line number being right is not the claim being
  right.
- **A bullet with no anchor is unverified.** Re-delegate with a narrower question instead of
  building on it.
- **Distrust a clean `Not found / uncertain`.** Silent omission is the dominant failure mode of a
  summarizing worker: an answer missing a case looks identical to a complete one. This section is
  the worker's own account of its gaps, so it fails exactly when you most need it — `- Nothing
  outstanding.` has come back from runs that missed a quarter of the real hits. An empty section on
  a multi-file question is a reason to check, not a reassurance.
- **Treat `Coverage` as a claim, never as a count.** Its line totals are wrong far more often than
  they are right, and "all files read in full" gets written next to a number that contradicts it.
  The worker does not do the arithmetic the section implies, so the figure carries no information
  about what it actually read.
- **Confirm coverage with a cheap Grep.** One `grep -c` of the pattern you asked about, against the
  paths you sent, tells you whether the count matches what came back — and it is the only cheap
  check that catches a file the worker silently dropped. Do it when the answer is empty, when
  `Not found / uncertain` is empty, and whenever `Coverage` quotes a number you have not checked.
