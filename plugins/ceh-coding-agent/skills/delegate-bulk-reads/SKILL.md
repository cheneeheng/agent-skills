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
- **Treat `Coverage` as a claim, never as a count.** The rows do add up — the worker sums them
  correctly — but each file comes back about one line too long, because a trailing newline reads as
  an extra line. That is the worst shape of wrong: close enough to look right at a glance, never exact
  enough to prove a file was read to its end.
- **Check every path got a verdict, then confirm with a cheap Grep.** The free check first: the
  worker owes every path you sent a verdict in `Answer` — a hit with anchors, or `no match` — so a
  path appearing in none of the three sections was dropped. That costs no tool call and works on a
  question with no greppable pattern. Where the question does have one, `grep -c` it against the
  paths you sent and compare with what came back. Do both when the answer is empty, when
  `Not found / uncertain` is empty, and whenever `Coverage` quotes a number you have not checked.
