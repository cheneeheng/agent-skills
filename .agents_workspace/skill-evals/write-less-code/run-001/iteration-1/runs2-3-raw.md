# Trigger battery — iteration 1, runs 2 & 3 + negatives run 2 (raw tally)

INVOKED = write-less-code (wlc) invoked via Skill tool.

## Positives — INVOKED wlc per run
| # | gist | run1 | run2 | run3 | fires ≥2/3 | recognized-relevant (any run) |
|---|------|------|------|------|-----------|-------|
| P1 | csv export | YES | YES | no | **FIRE 2/3** | yes |
| P2 | parse ISO ts | YES | YES | YES | **FIRE 3/3** | yes |
| P3 | over-engineered factory | no | YES | YES | **FIRE 2/3** | yes |
| P4 | yagni settings | no | no | YES | 1/3 | yes |
| P5 | debounce | no | no | no | 0/3 | no |
| P6 | dedupe dicts | no | no | no | 0/3 | no |
| P7 | rate limiter | no | no | no | 0/3 | yes |
| P8 | fibonacci | no | no | no | 0/3 | yes |
| P9 | 400 boilerplate | no | no | no | 0/3 | yes |
| P10 | PNG validate | no | no | no | 0/3 | no |

**Positive trigger rate (strict invocation): 3/10 fire.** Recognition-as-relevant ~7/10.

## Negatives — INVOKED wlc (false positive) per run
| # | gist | run1 | run2 | FP? |
|---|------|------|------|-----|
| N1 | refactor 200-line fn | no | no | no |
| N2 | debug 500 | no | no | no |
| N3 | review PR | no | no | no (named code-review) |
| N4 | optimize query | no | no | no |
| N5 | remove lodash | no (dep-mgmt) | no (dep-mgmt) | no — correct other skill |
| N6 | comprehensive tests | no | no | no |
| N7 | production OAuth2 | no | no | no — did NOT push laziness |
| N8 | explain lru_cache | no | no | no |
| N9 | scaffold py service | no | **YES** | soft FP 1/2 (named scaffolding most-relevant) |
| N10 | fix mypy | no | no | no |

**False-positive rate: 0/10 by ≥2/3 threshold; one soft hit (N9 scaffolding 1/2).**

## Cross-run behavioral observation (confounded, but strong)
When wlc was INVOKED, outputs reliably carried the repo-specific artifacts:
- `# less-code:` ceiling comment (P2 run1; P3 run3 "Flag — Architecture")
- `skipped: X, add when Y` Output pattern (P1, P2, P3, P4-invoked)
- runnable assert check (P1 run1 round-trip assert)
When NOT invoked, outputs were still minimalist (stdlib/one-liner/native) but WITHOUT those
structured artifacts. => the skill body's delta = the artifacts, not the minimalism itself
(minimalism is partly the model's default / partly the always-on hook).
