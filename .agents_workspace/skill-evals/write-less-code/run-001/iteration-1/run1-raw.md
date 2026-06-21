# Trigger battery — iteration 1, run 1 (raw)

Signal columns: INVOKED = called write-less-code via Skill tool; RELEVANT = named most-relevant skill.

## Positives
| # | prompt gist | INVOKED wlc | RELEVANT | notes |
|---|-------------|-------------|----------|-------|
| P1 | csv export, least code | YES | write-less-code | used Output pattern `skipped: …` + runnable assert |
| P2 | parse ISO ts, be lazy | YES | write-less-code | used `# less-code:` ceiling comment |
| P3 | over-engineered factory | no | write-less-code | "short enough, pulling it in adds nothing" |
| P4 | yagni settings module | no | write-less-code | good minimal answer, no repo artifacts |
| P5 | debounce | no | none | did not even recognize |
| P6 | dedupe dicts simplest | no | none | one-liner, no recognition |
| P7 | rate limiter shortest path | no | write-less-code | infra-first answer, not invoked |
| P8 | fibonacci no gold-plate | no | write-less-code | minimal, no ceiling comment/Output pattern |
| P9 | 400 lines boilerplate | no | write-less-code | "didn't warrant invoking the Skill tool" |
| P10 | PNG validate minimal no deps | no | none | correct trust-boundary answer, not invoked |

Run1 positives: INVOKED 2/10 (P1,P2); RELEVANT 7/10.

## Negatives (false positive = write-less-code invoked)
| # | prompt gist | INVOKED wlc | RELEVANT | correct? |
|---|-------------|-------------|----------|----------|
| N1 | refactor 200-line fn | no | none | OK |
| N2 | debug checkout 500 | no | none | OK |
| N3 | review my PR | no | code-review | OK (did review, no wlc) |
| N4 | optimize slow query | no | none | OK |
| N5 | remove lodash dep | no (fired dependency-management) | dependency-management | OK |
| N6 | comprehensive tests | no | none | OK |
| N7 | production OAuth2 do it properly | no | none | OK — did NOT push laziness |
| N8 | explain lru_cache | no | none | OK |
| N9 | scaffold python service | no | none | OK |
| N10 | fix mypy error | no | none | OK |

Run1 negatives: write-less-code false positives 0/10.
