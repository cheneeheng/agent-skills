# Definition of Done

## Bug Fix

- [ ] Root cause identified and documented in the PR description
- [ ] Failing test added that reproduces the bug
- [ ] Fix applied — the failing test now passes
- [ ] No regressions — full test suite passes
- [ ] Lint and type checks pass

## Feature

- [ ] Unit tests for new business logic
- [ ] Integration tests for new API surface
- [ ] Lint and type checks pass
- [ ] PR description explains the feature and how it was tested
- [ ] No `any`, `@ts-ignore`, or `# type: ignore` introduced

## Refactor

- [ ] No behavioral change — proven by existing tests passing unchanged
- [ ] Coverage unchanged (no tests deleted to make the refactor pass)
- [ ] Lint and type checks pass
- [ ] PR description explains what structural problem was addressed

## Coverage Targets

| Area | Minimum |
|------|---------|
| Python application package | 80% |
| Core business logic / domain services | 95% |
| TypeScript `src/lib/` | 70% |

`mypy --strict` and `tsc --noEmit` must pass with zero errors. Do not reduce strictness to meet coverage targets — fix the types.
