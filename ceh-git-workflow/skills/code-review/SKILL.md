---
name: "code-review"
description: >
  Load this skill when reviewing a pull request or leaving code review comments: deciding whether
  a comment is blocking or advisory, prioritizing what to review first, or structuring review
  feedback. Auto-load whenever a PR review is being written, review comments are being left,
  or a PR is being assessed for approval.
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
