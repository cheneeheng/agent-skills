---
name: "code-review"
description: "Load this skill when reviewing a pull request or leaving code review comments: deciding whether a comment is blocking or advisory, prioritizing what to review first, or structuring review feedback. Auto-load whenever a PR review is being written, review comments are being left, or a PR is being assessed for approval."
---

# Code Review

Every comment must be clearly marked as **blocking** or **advisory**.

| Prefix | Meaning | Author must |
|--------|---------|-------------|
| `[blocking]` | Must be resolved before merge | Fix or discuss with reviewer |
| `[advisory]` | Suggestion, optional improvement | Address or explicitly acknowledge |
| `[question]` | Seeking understanding, not a change request | Answer the question |

Examples:
```
[blocking] This query is not parameterized — SQL injection risk on line 47.

[advisory] This helper could be extracted to a utility function for reuse.

[question] Why is this retry limit set to 3?
```

## Review Focus (Priority Order)

1. **Correctness** — does it do what it claims? Are edge cases handled?
2. **Security** — injection risks, secrets exposure, input validation gaps
3. **Test coverage** — is new behavior tested? Are tests testing behavior?
4. **Design** — right abstraction? Fits existing patterns?
5. **Style** — only flag if linting tools don't catch it

Do not comment on style a linter would catch. Do not re-litigate decisions in `docs/adr/DECISIONS.md` unless new risk is identified. Do not review from memory — verify against current file contents.

## Structure of a Review

Leave a short summary comment plus line-anchored comments:

1. **Summary** — one or two sentences: what the PR does and your overall read. Lead with anything
   that blocks.
2. **Line comments** — each prefixed `[blocking]` / `[advisory]` / `[question]`, anchored to the
   exact line, stating the problem and (for blocking) what would resolve it.

End with an explicit verdict:

| Verdict | When |
|---------|------|
| **Approve** | No `[blocking]` comments. Advisory items can be left to the author's judgment. |
| **Request changes** | One or more `[blocking]` comments. Say what must change to flip to approve. |
| **Comment** | Questions outstanding, or not your call to approve — no verdict yet. |

Approve with non-blocking nits rather than withholding approval to force trivial changes.

## Responding as the Author

- `[blocking]`: fix it, or reply with the reasoning and reach agreement before merge.
- `[advisory]`: address it or acknowledge why you're not ("good idea, out of scope for this PR").
- `[question]`: answer in-thread; if the code was unclear enough to prompt the question, that's
  often a signal to clarify the code or a comment.

Resolve a thread only once it's actually addressed. Don't merge over unresolved `[blocking]` threads.
