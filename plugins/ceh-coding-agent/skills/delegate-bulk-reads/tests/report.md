# delegate-bulk-reads: token saving vs accuracy loss

3 run(s): run-001, run-002, run-003. Corpus: this repo. Token estimate: chars / 4. Delegated cost = prompt + reply + the verification re-reads the skill mandates (+/-20 lines around every distinct anchor).

## Runs compared

| Run | Direct read | Delegated | Saved | Fact recall | Anchored | No-match | Ghosts | Coverage error |
|-----|-------------|-----------|-------|-------------|----------|----------|--------|----------------|
| run-001 | 71287 | 20854 | 71% | 87% (48/55) | 87% | 12/12 | 0 | +30 over 39 rows |
| run-002 | 71287 | 19186 | 73% | 82% (45/55) | 76% | 12/12 | 0 | +38 over 39 rows |
| run-003 | 71287 | 17941 | 75% | 87% (48/55) | 73% | 12/12 | 0 | +682 over 39 rows |

## Per case, across runs

| Case | run-001 saved | run-002 saved | run-003 saved | run-001 facts | run-002 facts | run-003 facts |
|------|---|---|---|---|---|---|
| C01-sweep-frontmatter-effort | 85% | 85% | 85% | 6/6 | 6/6 | 6/6 |
| C02-negative-only | 96% | 96% | 96% | 0/0 | 0/0 | 0/0 |
| C03-guard-deny-conditions | -16% | 79% | 72% | 5/8 | 3/8 | 5/8 |
| C04-validate-description-rules | 74% | 75% | 76% | 3/5 | 3/5 | 3/5 |
| C05-exact-literal-for-edit | 71% | 71% | 71% | 2/2 | 2/2 | 2/2 |
| C06-plugin-dependencies | -3% | -3% | -4% | 6/6 | 6/6 | 6/6 |
| C07-js-shared-state | 74% | 50% | 81% | 7/8 | 7/8 | 7/8 |
| C08-single-large-file-outline | 1% | 2% | 1% | 10/10 | 10/10 | 10/10 |
| C09-fine-detail-retention | 42% | 40% | 40% | 4/5 | 3/5 | 4/5 |
| C10-sweep-disable-model-invocation | 86% | 86% | 86% | 5/5 | 5/5 | 5/5 |

## What was lost, and in how many runs

A miss in every run is a property of the question. A miss in one is variance.

| Fact | Missed in |
|------|-----------|
| C03-guard-deny-conditions / deny-payload | 3/3 (run-001, run-002, run-003) |
| C03-guard-deny-conditions / dump-cmds | 3/3 (run-001, run-002, run-003) |
| C03-guard-deny-conditions / window-cmds | 3/3 (run-001, run-002, run-003) |
| C04-validate-description-rules / max-len | 3/3 (run-001, run-002, run-003) |
| C04-validate-description-rules / missing-desc | 3/3 (run-001, run-002, run-003) |
| C07-js-shared-state / dom-map | 3/3 (run-001, run-002, run-003) |
| C09-fine-detail-retention / claim-not-count | 3/3 (run-001, run-002, run-003) |
| C03-guard-deny-conditions / fallback-bash | 1/3 (run-002) |
| C03-guard-deny-conditions / fallback-read | 1/3 (run-002) |
| C09-fine-detail-retention / off-by-one | 1/3 (run-002) |

## run-001 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 3952 | 85% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +8 over 8 rows |
| C02-negative-only | negative | 7962 | 341 | 96% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 3362 | -16% | 5/8 | 7/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 1072 | 74% | 3/5 | 3/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 574 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 1501 | -3% | 6/6 | 6/6 | 4/4 | 0 | 10/10 | +2 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 1253 | 74% | 7/8 | 5/8 | 0/0 | 0 | 3/3 | +2 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5525 | 1% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1513 | 42% | 4/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 1761 | 86% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +7 over 7 rows |

- Saved **71%** (50433 tokens); reply 3432 + verification re-reads 16135 + prompts.
- Fact recall **87%** (48/55), anchors within 3 lines **87%**, ghost anchors **0**.
- Exchange rate: **7204 tokens saved per fact lost**.

## run-002 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 3927 | 85% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +8 over 8 rows |
| C02-negative-only | negative | 7962 | 331 | 96% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 612 | 79% | 3/8 | 0/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 1035 | 75% | 3/5 | 3/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 570 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 1500 | -3% | 6/6 | 6/6 | 4/4 | 0 | 10/10 | +9 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 2374 | 50% | 7/8 | 6/8 | 0/0 | 0 | 3/3 | +3 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5501 | 2% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1566 | 40% | 3/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 1770 | 86% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +7 over 7 rows |

- Saved **73%** (52101 tokens); reply 2970 + verification re-reads 14929 + prompts.
- Fact recall **82%** (45/55), anchors within 3 lines **76%**, ghost anchors **0**.
- Exchange rate: **5210 tokens saved per fact lost**.

## run-003 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 3950 | 85% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +8 over 8 rows |
| C02-negative-only | negative | 7962 | 339 | 96% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 823 | 72% | 5/8 | 0/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 995 | 76% | 3/5 | 3/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 575 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 1509 | -4% | 6/6 | 6/6 | 4/4 | 0 | 10/10 | +5 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 885 | 81% | 7/8 | 4/8 | 0/0 | 0 | 3/3 | +2 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5521 | 1% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1584 | 40% | 4/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 1760 | 86% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +656 over 7 rows |

- Saved **75%** (53346 tokens); reply 3280 + verification re-reads 13374 + prompts.
- Fact recall **87%** (48/55), anchors within 3 lines **73%**, ghost anchors **0**.
- Exchange rate: **7620 tokens saved per fact lost**.
