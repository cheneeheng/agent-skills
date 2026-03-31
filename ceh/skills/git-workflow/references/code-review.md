# Code Review Comment Conventions

Every comment must be clearly marked as **blocking** or **advisory**. Ambiguous comments slow merges and create guesswork.

| Prefix | Meaning | Author must |
|--------|---------|-------------|
| `[blocking]` | Must be resolved before merge | Fix or discuss with reviewer |
| `[advisory]` | Suggestion, nit, optional improvement | Address or explicitly acknowledge |
| `[question]` | Seeking understanding, not a change request | Answer the question |

**Examples:**
```
[blocking] This query is not parameterized — SQL injection risk on line 47.

[advisory] This helper could be extracted to a utility function for reuse.
           Not required for this PR but worth considering.

[question] Why is this retry limit set to 3? Is there a reason not to use
           the global default?
```

## Review Focus (Priority Order)

1. **Correctness** — does it do what it claims? Are edge cases handled?
2. **Security** — injection risks, secrets exposure, input validation gaps
3. **Test coverage** — is new behavior tested? Are tests testing behavior?
4. **Design** — is this the right abstraction? Does it fit existing patterns?
5. **Style** — only flag if linting tools don't catch it

Do not leave style comments that a linter would catch. Configure the linter instead.

Review does not re-litigate resolved decisions in `ARCHITECTURE_DECISIONS.md` unless new risk is identified.
