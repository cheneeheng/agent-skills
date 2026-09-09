# delegate-bulk-reads evaluation

Ten cases that put a number on the trade the skill asks the caller to make: how much context
delegating to `bulk-reader` saves, and how much of the answer is lost to summarisation by a
smaller model.

Corpus is this repo. There are no fixtures — the answer key resolves against the live files,
so it cannot silently rot.

## Version under test

All six committed runs were taken against commit **`c8cfddc`**, with `ceh-coding-agent` at
**3.2.7**. One variable separates them: the worker model.

| Runs | Worker | How |
|------|--------|-----|
| 001–003 | Haiku | the model pinned in `agents/bulk-reader.md` |
| 004–006 | Sonnet | overridden per dispatch via the `Agent` tool's `model` parameter |

Because the skill, the agent, and the corpus are identical across all six, the Haiku/Sonnet gap is
attributable to the model alone. Later runs are not comparable unless all three are still
unchanged — record the commit and plugin version whenever you add a `run-NNN/`.

C09's corpus is the skill and agent files themselves, so an edit to either moves the ground under
that one case; its recorded replies describe `c8cfddc`, not necessarily HEAD.

## Run it

```bash
cd plugins/ceh-coding-agent/skills/delegate-bulk-reads/tests
python run_tests.py check     # every locate regex still matches; run this first
python run_tests.py prompts   # writes prompts/<case>.txt and the baseline cost table
# dispatch each prompt to the bulk-reader subagent, save the reply verbatim to
# responses/run-NNN/<case>.md
python run_tests.py score     # scores every run-* directory; writes report.md
```

Stdlib only. No API key, no network, no test framework.

The middle step is agentic and cannot be scripted from here: an agent session dispatches the ten
`Agent(subagent_type: "bulk-reader", ...)` calls and pastes each reply into a fresh
`responses/run-NNN/`. Six runs are committed, so `score` works out of the box.

**Run more than once.** The worker is non-deterministic and a single run cannot tell a property of
the question from a bad draw. `score` reads every `run-*` directory and reports the spread,
including which facts were lost in every run and which in only one.

## What each case probes

| Case | Kind | What it is built to expose |
|------|------|----------------------------|
| C01 | sweep | Silent omission across 8 files — the failure the skill calls dominant |
| C02 | negative | Fabrication when the honest answer is "nothing, anywhere" |
| C03 | semantic | Two near-identical sibling files, easy to conflate |
| C04 | semantic | A rule split between a docstring and the code that enforces it |
| C05 | exact-text | The skill's own exclusion: a summary cannot feed an edit exact text |
| C06 | sweep | Ten tiny files, where delegation overhead can exceed the read |
| C07 | semantic | Data flow that no single file states |
| C08 | sweep | Compression ceiling on one 22 KB file |
| C09 | detail | Two documents whose entire point is a caveat |
| C10 | sweep | A missed hit costs a silently failed skill invocation downstream |

## How the numbers are built

**Direct read** is every byte of the case's files, which is what a caller pays to read them itself.

**Delegated** is the honest total, not just the reply: prompt + reply + a re-read of ±20 lines
around every distinct anchor. The skill mandates that re-read before acting on an anchor, so
leaving it out would flatter the saving by a factor of five. It dominates the delegated cost in
every case here.

**Facts** is recall against the answer key. Each positive fact carries a `locate` regex resolved
against the live file at scoring time, so nothing is a hardcoded line number; `check` fails loudly
when a locate stops matching, which is also the signal that the corpus moved.

**Anchored** counts facts whose truth line the reply anchored within 3 lines. **Ghost anchors**
point past a file's end or at a file that was never sent — either way the caller reads the wrong
place.

**Line-count error** measures the Coverage rows against the real line counts. The skill warns that
Coverage is a claim and not a count; this is that warning as a number.

Tokens are `len(text) / 4`. Approximate, but applied identically to both arms, so the ratio holds.

## Result of the committed runs

| Run | Worker | Saved | Fact recall | Usable anchors | No-match | Ghosts | Coverage error |
|-----|--------|-------|-------------|----------------|----------|--------|----------------|
| run-001 | Haiku | 76% | 85% (47/55) | 67% | 12/12 | 5 | +32 over 39 rows |
| run-002 | Haiku | 78% | 87% (48/55) | 56% | 6/12 | 1 | +1325 over 39 rows |
| run-003 | Haiku | 73% | 87% (48/55) | 75% | 12/12 | 0 | +28 over 37 rows |
| run-004 | Sonnet | 60% | 93% (51/55) | 93% | 12/12 | 4 | +2415 over 39 rows |
| run-005 | Sonnet | 62% | 96% (53/55) | 93% | 12/12 | 4 | +2415 over 39 rows |
| run-006 | Sonnet | 58% | 93% (51/55) | 95% | 12/12 | 0 | +2345 over 39 rows |

Full tables in `report.md`.

**The saving is stable within a model and moves 15 points between them.** Haiku held 73–78% across
three runs, Sonnet 58–62% across three. Per case the spread is tighter still. Sonnet buys accuracy
with context and the price is roughly a sixth of the corpus.

**Recall splits cleanly by model.** Haiku 85–87%, Sonnet 93–96%, with no overlap. Three facts
separate them: C04 `max-len`, C04 `missing-desc` and C09 `claim-not-count` were missed in all three
Haiku runs and found in all three Sonnet runs. Those are the reasoning-shaped details the smaller
worker reliably drops.

**Four facts are properties of the question, not the worker.** C03 `deny-payload` and C07 `dom-map`
went missing in all six runs; C03 `dump-cmds` and `window-cmds` in five of six (only run-005 found
them). A bigger model does not fix these — ask a narrower question or read directly.

**Haiku's anchors are frequently unusable; Sonnet's are not.** 56–75% against 93–95%. The losses
are formatting, not fabrication: Haiku wrote bare `line 34` or `validates.py:167` — a filename that
was never sent — instead of `path:line`, so run-001's whole C04 reply scored 0/5 anchored and 5
ghosts. The caller pays the same either way and sometimes cannot verify what it got.

**Sonnet's four ghost anchors are a one-line overshoot.** Runs 004 and 005 cited
`plugin.json:1-10` for four 9-line manifests. Substantively harmless, the answers were right, but
the scorer cannot tell a one-line overshoot from a fabricated citation. Verified by hand.

**Coverage is a claim, and both models proved it, Sonnet louder.** Haiku's run-002 reported 50 lines
for each of eight files running to 300; Sonnet reports 20 lines per file in C01 and C10 every run,
which is the whole +2400 error. Every one of those answers was still correct, because frontmatter
sits at the top. Nothing but the Coverage rows would have told the caller the files were never read
to the end.

**One Haiku run collapsed the negative verdicts.** run-002's C02 answered with a single blanket
"no match" line instead of one per file, and its C10 named the two negatives without anchoring
them, costing 6 of 12 no-match verdicts. Sonnet stated all 12, all three runs.

**Two cases go negative for both models, and worse for Sonnet.** C03 (2 files, 352 lines) and C06
(10 files, 111 lines) cost more delegated than read. C03 runs 75–77% saved on Haiku but -37% to
-45% on Sonnet; C06 is -6% to +3% on Haiku, -49% to -53% on Sonnet. Sonnet writes more about a
small corpus, so the sub-400-line floor holds harder for the bigger model. C08 saves 1–2% either
way, because verifying 19 anchors re-reads most of the one file.

## Verdict

Split the 60 replies by what the question asks for, and the two halves behave nothing alike:

| Question kind | Cases | Haiku saved | Haiku recall | Sonnet saved | Sonnet recall |
|---------------|-------|-------------|--------------|--------------|---------------|
| Enumerative (sweep, negative) | C01, C02, C06, C08, C10 | 78% | **100%** (81/81) | 68% | **100%** (81/81) |
| Reasoning (semantic, detail) | C03, C04, C07, C09 | 62% | **71%** (56/78) | 25% | **87%** (68/78) |

Worth it for enumerative questions over a large corpus, on either model. "Which of these files
declare X", "does any of this import Y", "list every heading" — 162 of 162 facts across six runs,
no invented answers, at a fraction of the direct-read cost. Haiku is the better buy here: same
perfect recall, 10 more points of saving. Its only enumerative weakness is honesty about negatives
(run-002's 6/12) and anchor formatting, both cheap to spot-check with one `grep`.

Not worth it for reasoning questions on Haiku. Three in ten facts vanished and the reply said
`- Nothing outstanding.` every time. Sonnet cuts that to roughly one in eight but pays 37 points of
saving to do it, which leaves 25% — barely worth the round trip. Ask a narrower enumerative
question instead, or read directly.

Not worth it below roughly 400 lines on either model. C03 (352 lines) and C06 (111 lines) cost more
delegated than read in every one of the six runs, and the penalty triples on Sonnet. Neither is the
skill worth it for an outline of one file you will then verify: C08 saved 1–2%.

**Choosing the worker.** Switching to Sonnet moves the failure mode from *silent omission* to
*expensive thoroughness*. It closes most of the reasoning gap, anchors almost everything it claims,
and states every negative — and costs about 15 points of overall saving, more on small corpora. On
enumerative questions, where Haiku already scores 100%, it is a straight loss. Keep the pinned
Haiku; override to Sonnet only when the question is genuinely semantic and the corpus is large.

The skill's own guidance survives contact with the data. Its three warnings — treat Coverage as a
claim, distrust a clean `Not found / uncertain`, read the anchored lines before acting — each
reproduced here, in that order of severity, under both workers.
