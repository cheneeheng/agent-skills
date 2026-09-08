# delegate-bulk-reads evaluation

Ten cases that put a number on the trade the skill asks the caller to make: how much context
delegating to `bulk-reader` saves, and how much of the answer is lost to summarisation by a
smaller model.

Corpus is this repo. There are no fixtures — the answer key resolves against the live files,
so it cannot silently rot.

## Version under test

The three committed runs were taken against **repo tag `v6.3.2`**, with `ceh-coding-agent` at
**3.2.5** — the skill and agent text as of commit `de112ba`, before any finding here was folded
back in. The worker ran on Haiku, the model pinned in `agents/bulk-reader.md`.

Two consequences. Later runs are not comparable to these unless the skill, the agent, and the
worker model are all unchanged — record the tag and plugin version whenever you add a `run-NNN/`.
And C09's corpus is the skill and agent files themselves, so an edit to either moves the ground
under that one case; its recorded replies describe `de112ba`, not necessarily HEAD.

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
`responses/run-NNN/`. Three runs are committed, so `score` works out of the box.

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

## Result of the three committed runs

| Run | Saved | Fact recall | Usable anchors | No-match | Ghosts | Coverage error |
|-----|-------|-------------|----------------|----------|--------|----------------|
| run-001 | 71% | 87% (48/55) | 87% | 12/12 | 0 | +30 over 39 rows |
| run-002 | 73% | 82% (45/55) | 76% | 12/12 | 0 | +38 over 39 rows |
| run-003 | 75% | 87% (48/55) | 73% | 12/12 | 0 | +682 over 39 rows |

Full tables in `report.md`.

**The saving is stable, the answer quality is not.** Context saved moved 71–75% across the three
runs, and per case it barely moved at all. Usable anchors swung 87% → 73%: in run-003 the C03 reply
wrote `line 16` under a filename heading instead of `path:line`, so not one of its eight anchors was
machine-checkable. The caller pays the same either way and sometimes cannot verify what it got.

**Seven of the nine losses are structural, two are variance.** The same seven facts were missed in
all three runs, all in `semantic` and `detail` cases — the worker reliably keeps the enumeration and
drops the reasoning-shaped detail. Only two misses (C03 `fallback-read`/`fallback-bash`, run-002)
were a bad draw. That split is why three runs are worth the cost: one run cannot distinguish them.

**Coverage is a claim, and run-003 proved it.** Its C10 reply reported "50 lines read" for all seven
files, which are 59 to 301 lines long — it read the first 50 of each and said so. The answer was
still right, because frontmatter sits on line 3. Nothing but the Coverage rows would have told the
caller the files were never read to the end.

**Two cases go negative every run.** C03 (2 files, 352 lines) and C06 (10 files, 111 lines) cost more
delegated than read directly, and C08 saves 1% because verifying 19 anchors re-reads most of the one
file. Below roughly 400 lines the round trip is not worth taking.

Across all 30 replies, every lossy one closed with `- Nothing outstanding.` and no run produced a
single ghost anchor. The worker does not invent anchors; it omits, silently.

## Verdict

Split the 30 replies by what the question asks for, and the two halves behave nothing alike:

| Question kind | Cases | Saved | Fact recall | No-match |
|---------------|-------|-------|-------------|----------|
| Enumerative (sweep, negative) | C01, C02, C06, C08, C10 | 76% | **100%** (81/81) | 36/36 |
| Reasoning (semantic, detail) | C03, C04, C07, C09 | 60% | **69%** (54/78) | n/a |

Worth it for enumerative questions over a large corpus. "Which of these files declare X", "does any
of this import Y", "list every heading" — 81 of 81 facts across three runs, 36 of 36 honest
no-match verdicts, no invented anchors, at roughly a quarter of the direct-read cost. Over 400-plus
lines that is a clear win and the answer is cheap to spot-check with one `grep`.

Not worth it for reasoning questions. Three in ten facts vanished, the same seven every run, and the
reply said `- Nothing outstanding.` each time. You cannot tell a complete answer from a gutted one
without reading the files, and reading the files is the thing you were trying to avoid. Ask a
narrower enumerative question instead, or read directly.

Not worth it below roughly 400 lines at all. C03 (352 lines) and C06 (111 lines) cost more delegated
than read, every run. Neither is the skill worth it for an outline of one file you will then verify:
C08 saved 1%, because checking 19 anchors re-reads the file you skipped.

The skill's own guidance survives contact with the data. Its three warnings — treat Coverage as a
claim, distrust a clean `Not found / uncertain`, read the anchored lines before acting — each
reproduced here, in that order of severity.
