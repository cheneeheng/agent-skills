# delegate-bulk-reads: token saving vs accuracy loss

6 run(s): run-001, run-002, run-003, run-004, run-005, run-006. Corpus: this repo. Token estimate: chars / 4. Delegated cost = prompt + reply + the verification re-reads the skill mandates (+/-20 lines around every distinct anchor).

## Runs compared

| Run | Direct read | Delegated | Saved | Fact recall | Anchored | No-match | Ghosts | Coverage error |
|-----|-------------|-----------|-------|-------------|----------|----------|--------|----------------|
| run-001 | 71287 | 17395 | 76% | 85% (47/55) | 67% | 12/12 | 5 | +32 over 39 rows |
| run-002 | 71287 | 15717 | 78% | 87% (48/55) | 56% | 6/12 | 1 | +1325 over 39 rows |
| run-003 | 71287 | 19313 | 73% | 87% (48/55) | 75% | 12/12 | 0 | +28 over 37 rows |
| run-004 | 71287 | 28777 | 60% | 93% (51/55) | 93% | 12/12 | 4 | +2415 over 39 rows |
| run-005 | 71287 | 27404 | 62% | 96% (53/55) | 93% | 12/12 | 4 | +2415 over 39 rows |
| run-006 | 71287 | 29803 | 58% | 93% (51/55) | 95% | 12/12 | 0 | +2345 over 39 rows |

## Per case, across runs

| Case | run-001 saved | run-002 saved | run-003 saved | run-004 saved | run-005 saved | run-006 saved | run-001 facts | run-002 facts | run-003 facts | run-004 facts | run-005 facts | run-006 facts |
|------|---|---|---|---|---|---|---|---|---|---|---|---|
| C01-sweep-frontmatter-effort | 85% | 85% | 85% | 82% | 82% | 82% | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| C02-negative-only | 95% | 97% | 96% | 77% | 75% | 75% | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| C03-guard-deny-conditions | 76% | 77% | 75% | -38% | -37% | -45% | 5/8 | 5/8 | 5/8 | 5/8 | 7/8 | 5/8 |
| C04-validate-description-rules | 93% | 74% | 75% | 49% | 64% | 67% | 3/5 | 3/5 | 3/5 | 5/5 | 5/5 | 5/5 |
| C05-exact-literal-for-edit | 69% | 70% | 71% | 71% | 71% | 71% | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| C06-plugin-dependencies | -6% | 3% | -3% | -53% | -51% | -49% | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| C07-js-shared-state | 80% | 17% | 56% | 37% | 52% | 4% | 6/8 | 7/8 | 7/8 | 7/8 | 7/8 | 7/8 |
| C08-single-large-file-outline | 2% | 95% | -3% | 1% | 1% | 2% | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| C09-fine-detail-retention | 41% | 43% | 42% | 31% | 36% | 36% | 4/5 | 4/5 | 4/5 | 5/5 | 5/5 | 5/5 |
| C10-sweep-disable-model-invocation | 86% | 85% | 86% | 78% | 78% | 78% | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |

## What was lost, and in how many runs

A miss in every run is a property of the question. A miss in one is variance.

| Fact | Missed in |
|------|-----------|
| C03-guard-deny-conditions / deny-payload | 6/6 (run-001, run-002, run-003, run-004, run-005, run-006) |
| C07-js-shared-state / dom-map | 6/6 (run-001, run-002, run-003, run-004, run-005, run-006) |
| C03-guard-deny-conditions / dump-cmds | 5/6 (run-001, run-002, run-003, run-004, run-006) |
| C03-guard-deny-conditions / window-cmds | 5/6 (run-001, run-002, run-003, run-004, run-006) |
| C04-validate-description-rules / max-len | 3/6 (run-001, run-002, run-003) |
| C04-validate-description-rules / missing-desc | 3/6 (run-001, run-002, run-003) |
| C09-fine-detail-retention / claim-not-count | 3/6 (run-001, run-002, run-003) |
| C02-negative-only / github-js(no-match not stated) | 1/6 (run-002) |
| C02-negative-only / guard(no-match not stated) | 1/6 (run-002) |
| C02-negative-only / validate(no-match not stated) | 1/6 (run-002) |
| C02-negative-only / watch(no-match not stated) | 1/6 (run-002) |
| C07-js-shared-state / declaration | 1/6 (run-001) |
| C10-sweep-disable-model-invocation / design-test-cases-none(no-match not stated) | 1/6 (run-002) |
| C10-sweep-disable-model-invocation / shrink-diff-none(no-match not stated) | 1/6 (run-002) |

## run-001 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 4097 | 85% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +8 over 8 rows |
| C02-negative-only | negative | 7962 | 369 | 95% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +3 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 692 | 76% | 5/8 | 0/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 277 | 93% | 3/5 | 0/5 | 0/0 | 5 | 1/1 | +0 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 605 | 69% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 1543 | -6% | 6/6 | 6/6 | 4/4 | 0 | 10/10 | +5 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 952 | 80% | 6/8 | 4/8 | 0/0 | 0 | 3/3 | +3 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5497 | 2% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1559 | 41% | 4/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 1804 | 86% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +7 over 7 rows |

- Saved **76%** (53892 tokens); reply 3480 + verification re-reads 12628 + prompts.
- Fact recall **85%** (47/55), anchors within 3 lines **67%**, ghost anchors **5**.
- Exchange rate: **6736 tokens saved per fact lost**.

## run-002 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 4103 | 85% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +1295 over 8 rows |
| C02-negative-only | negative | 7962 | 238 | 97% | 0/0 | 0/0 | 0/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 668 | 77% | 5/8 | 0/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 1047 | 74% | 3/5 | 3/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 595 | 70% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 1418 | 3% | 6/6 | 5/6 | 4/4 | 1 | 10/10 | +10 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 3982 | 17% | 7/8 | 6/8 | 0/0 | 0 | 3/3 | +2 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 307 | 95% | 10/10 | 0/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1482 | 43% | 4/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 1877 | 85% | 5/5 | 5/5 | 0/2 | 0 | 7/7 | +7 over 7 rows |

- Saved **78%** (55570 tokens); reply 3140 + verification re-reads 11290 + prompts.
- Fact recall **87%** (48/55), anchors within 3 lines **56%**, ghost anchors **1**.
- Exchange rate: **7938 tokens saved per fact lost**.

## run-003 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 4019 | 85% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +8 over 8 rows |
| C02-negative-only | negative | 7962 | 294 | 96% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 731 | 75% | 5/8 | 0/8 | 0/0 | 0 | 2/2 | +0 over 0 rows |
| C04-validate-description-rules | semantic | 4086 | 1027 | 75% | 3/5 | 3/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 570 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 1496 | -3% | 6/6 | 6/6 | 4/4 | 0 | 10/10 | +1 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 2096 | 56% | 7/8 | 5/8 | 0/0 | 0 | 3/3 | +3 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5742 | -3% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1511 | 42% | 4/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 1827 | 86% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +7 over 7 rows |

- Saved **73%** (51974 tokens); reply 3553 + verification re-reads 14473 + prompts.
- Fact recall **87%** (48/55), anchors within 3 lines **75%**, ghost anchors **0**.
- Exchange rate: **7424 tokens saved per fact lost**.

## run-004 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 4842 | 82% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +1535 over 8 rows |
| C02-negative-only | negative | 7962 | 1848 | 77% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 3995 | -38% | 5/8 | 7/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 2082 | 49% | 5/5 | 5/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 570 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 2222 | -53% | 6/6 | 6/6 | 4/4 | 4 | 10/10 | +0 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 3023 | 37% | 7/8 | 6/8 | 0/0 | 0 | 3/3 | +3 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5520 | 1% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1796 | 31% | 5/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 2879 | 78% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +866 over 7 rows |

- Saved **60%** (42510 tokens); reply 5087 + verification re-reads 22403 + prompts.
- Fact recall **93%** (51/55), anchors within 3 lines **93%**, ghost anchors **4**.
- Exchange rate: **10627 tokens saved per fact lost**.

## run-005 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 4837 | 82% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +1535 over 8 rows |
| C02-negative-only | negative | 7962 | 1989 | 75% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 3977 | -37% | 7/8 | 7/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 1461 | 64% | 5/5 | 5/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 570 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 2193 | -51% | 6/6 | 6/6 | 4/4 | 4 | 10/10 | +0 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 2278 | 52% | 7/8 | 6/8 | 0/0 | 0 | 3/3 | +3 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5548 | 1% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1670 | 36% | 5/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 2881 | 78% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +866 over 7 rows |

- Saved **62%** (43883 tokens); reply 4740 + verification re-reads 21377 + prompts.
- Fact recall **96%** (53/55), anchors within 3 lines **93%**, ghost anchors **4**.
- Exchange rate: **21941 tokens saved per fact lost**.

## run-006 in detail

| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |
|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|
| C01-sweep-frontmatter-effort | sweep | 27005 | 4827 | 82% | 6/6 | 6/6 | 2/2 | 0 | 8/8 | +1535 over 8 rows |
| C02-negative-only | negative | 7962 | 2029 | 75% | 0/0 | 0/0 | 4/4 | 0 | 4/4 | +4 over 4 rows |
| C03-guard-deny-conditions | semantic | 2901 | 4195 | -45% | 5/8 | 7/8 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C04-validate-description-rules | semantic | 4086 | 1366 | 67% | 5/5 | 5/5 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C05-exact-literal-for-edit | exact-text | 1958 | 570 | 71% | 2/2 | 2/2 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C06-plugin-dependencies | sweep | 1456 | 2163 | -49% | 6/6 | 6/6 | 4/4 | 0 | 10/10 | +0 over 10 rows |
| C07-js-shared-state | semantic | 4774 | 4572 | 4% | 7/8 | 7/8 | 0/0 | 0 | 3/3 | +3 over 3 rows |
| C08-single-large-file-outline | sweep | 5599 | 5497 | 2% | 10/10 | 10/10 | 0/0 | 0 | 1/1 | +1 over 1 rows |
| C09-fine-detail-retention | detail | 2621 | 1686 | 36% | 5/5 | 4/5 | 0/0 | 0 | 2/2 | +2 over 2 rows |
| C10-sweep-disable-model-invocation | sweep | 12925 | 2898 | 78% | 5/5 | 5/5 | 2/2 | 0 | 7/7 | +796 over 7 rows |

- Saved **58%** (41484 tokens); reply 4835 + verification re-reads 23681 + prompts.
- Fact recall **93%** (51/55), anchors within 3 lines **95%**, ghost anchors **0**.
- Exchange rate: **10371 tokens saved per fact lost**.
