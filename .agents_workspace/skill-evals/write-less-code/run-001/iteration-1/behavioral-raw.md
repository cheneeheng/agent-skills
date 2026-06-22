# Behavioral lift — iteration 1 (with-skill vs baseline, N=2, neutral phrasing)

Baseline = no skill, no hook. Neutral task wording (no "minimal/lazy" hint) so baseline isn't tipped off.

## Task A — business days between two dates (over-build temptation)
| Assertion | with-skill r1 | with-skill r2 | baseline r1 | baseline r2 | lift? |
|-----------|--------------|--------------|-------------|-------------|-------|
| A1 no new dep / stdlib | PASS | PASS | PASS | PASS | none — baseline already stdlib (only *mentioned* numpy) |
| A2 single fn, no class | PASS | PASS | PASS | PASS | none |
| A3 structured skipped:/add-when + runnable check | PASS (`# less-code:` + asserts) | PASS (`[code] → skipped:` + asserts) | partial (prose "if NumPy…") | partial | **modest lift** — artifacts only |
| A4 correctness | PASS | PASS | PASS | PASS | none |

## Task B — React email validation (native-over-library)
| Assertion | with-skill r1 | with-skill r2 | baseline r1 | baseline r2 | lift? |
|-----------|--------------|--------------|-------------|-------------|-------|
| B1 native HTML5 over JS lib/regex | PASS (type=email+required only) | PASS | PARTIAL (native + added regex+state layer) | PARTIAL | **lift** — with-skill markedly leaner |
| B2 no new dependency | PASS | PASS | PASS | PASS | none — neither added zod/yup |
| B3 states skipped + upgrade path | PASS | PASS | NO | NO | **lift** |
| (counter) accessibility kept | relies on native a11y | native | added aria-invalid/role=alert | added aria | baseline richer UX/a11y |

## Task C — CSV sum (guardrail: don't simplify away trust boundary)
| Assertion | with-skill r1 | with-skill r2 | baseline r1 | baseline r2 | lift? |
|-----------|--------------|--------------|-------------|-------------|-------|
| C1 money correctness (Decimal) | PASS (Decimal) | PASS (float, but flagged →Decimal) | PASS (Decimal) | PASS (Decimal) | none |
| C1b malformed-row handling | deferred (documented skip) | deferred | PASS (skips+reports) | PASS | **negative** — baseline more robust unprompted |
| C2 minimal, no framework | PASS | PASS | PASS (heavier but stdlib) | PASS | with-skill leaner |

## Behavioral verdict
- **The baseline is already minimalist by default**: stdlib over deps, small functions, no speculative
  abstractions — without the skill or hook. So raw "less code" is NOT where the lift lives.
- **Measured lift is real but modest and concentrated in the repo house-style artifacts**: the
  `// less-code:` ceiling comment, the `skipped: X, add when Y` Output pattern, the embedded runnable
  assert (Task A), and a harder push to native-over-library (Task B).
- **No correctness regression** in any arm. In two places the *baseline* delivered more (Task B
  accessibility/error UX, Task C malformed-row tolerance) — i.e. "less" is not universally "better",
  and the skill's leaner output occasionally drops robustness the baseline volunteered.
- Variance: consistent across both runs per arm.
