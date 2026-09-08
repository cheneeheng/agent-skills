#!/usr/bin/env python3
"""Measure what delegating a read to bulk-reader saves, and what it costs in accuracy.

Three modes:

    python run_tests.py check      # answer key still resolves against the live repo
    python run_tests.py prompts    # emit the 10 delegation prompts + the baseline cost
    python run_tests.py score      # grade responses/<case>.md, print the trade-off table

The run itself is agentic: `prompts` writes prompts/<case>.txt, an agent dispatches each
one to the bulk-reader subagent, saves the reply verbatim to responses/<case>.md, and
`score` does the arithmetic. Stdlib only, no API key, no network.

Token counts are len(text)/chars_per_token from cases.json. Approximate, but applied
identically to both arms, so the ratio it reports is the honest number.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPTS = HERE / "prompts"
RESPONSES = HERE / "responses"

# path:line or path:start-end, for any extension in the corpus.
ANCHOR = re.compile(r"([A-Za-z0-9_./\\-]+\.(?:md|py|js|json))[:](\d+)(?:\s*-\s*(\d+))?")
# The agent spec mandates `- <path> - no match.`, but the question here is whether the caller
# learned the file has no hit, not whether the worker used the house phrase. Accept the
# paraphrases seen in practice: scoring the wording would report a format slip as a lost fact.
NO_MATCH = re.compile(
    r"no match|none found|no occurrence"
    r"|does not (?:import|contain|use|declare|set|have|define)"
    r"|no [`'\"]?[\w.:-]+[`'\"]? (?:field|key|entry|import|declaration)",
    re.I)
# A Coverage row: `- <path> - 301 lines read`. Thousands separators are common.
COVERAGE_ROW = re.compile(r"^\s*-\s+(\S+?)\s*[-—:]+\s*([\d,]+)\s+lines", re.M)


def repo_root() -> Path:
    for d in [HERE, *HERE.parents]:
        if (d / ".claude-plugin" / "marketplace.json").exists():
            return d
    sys.exit("cannot locate repo root (no .claude-plugin/marketplace.json above this file)")


ROOT = repo_root()


def load_cases() -> dict:
    return json.loads((HERE / "cases.json").read_text(encoding="utf-8"))


def tokens(text: str, per: int) -> int:
    return math.ceil(len(text) / per)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def truth_lines(fact: dict) -> list[int]:
    """1-indexed lines in the live file matching the fact's locate regex."""
    pat = re.compile(fact["locate"])
    return [i for i, line in enumerate(read(fact["file"]).splitlines(), 1) if pat.search(line)]


def anchors(text: str) -> list[tuple[str, int, int]]:
    out = []
    for path, start, end in ANCHOR.findall(text):
        s = int(start)
        out.append((path.replace("\\", "/"), s, int(end) if end else s))
    return out


def same_file(anchor_path: str, case_path: str) -> bool:
    """An anchor may be written short (`state.js`) or full. Suffix match on segments."""
    a, c = anchor_path.split("/"), case_path.split("/")
    return a == c[-len(a):] if len(a) <= len(c) else False


def mentions(text: str, patterns: list[str]) -> bool:
    return all(re.search(p, text, re.I) for p in patterns)


# Segments that identify nothing - every path in the corpus has them.
GENERIC_SEGMENTS = {"plugins", "skills", "agents", "scripts", "tools", "js", ".claude-plugin"}


def names_for(path: str) -> list[str]:
    """Every string that could stand for this file in a reply: the path, the basename,
    and each distinctive directory (SKILL.md and plugin.json are named by their folder)."""
    parts = path.split("/")
    return [path, parts[-1]] + [p for p in parts[:-1] if p not in GENERIC_SEGMENTS]


def no_match_stated(text: str, path: str) -> bool:
    """The response must name the file and, on that same line, say it did not match."""
    names = names_for(path)
    return any(any(n in line for n in names) and NO_MATCH.search(line)
               for line in text.splitlines())


# --- check -----------------------------------------------------------------

def cmd_check(cfg: dict) -> int:
    bad = 0
    for case in cfg["cases"]:
        for rel in case["files"]:
            if not (ROOT / rel).exists():
                print(f"MISSING FILE  {case['id']}  {rel}")
                bad += 1
        for fact in case["facts"]:
            if "locate" not in fact:
                continue
            if not (ROOT / fact["file"]).exists():
                continue
            hits = truth_lines(fact)
            if not hits:
                print(f"STALE LOCATE  {case['id']}/{fact['id']}  {fact['locate']!r} matches nothing in {fact['file']}")
                bad += 1
        for fact in case["facts"]:
            if fact.get("expect") == "no-match" and fact["file"] not in case["files"]:
                print(f"ORPHAN FACT   {case['id']}/{fact['id']}  file not in the case's file list")
                bad += 1
    print(f"\n{len(cfg['cases'])} cases, {sum(len(c['facts']) for c in cfg['cases'])} facts, {bad} problem(s).")
    return 1 if bad else 0


# --- prompts ---------------------------------------------------------------

PROMPT_TMPL = """QUESTION: {question}

FILES:
{files}

Answer only the question. Anchor every claim with path:line.
Use the three-section format: ## Answer, ## Not found / uncertain, ## Coverage.
"""


def prompt_text(case: dict) -> str:
    return PROMPT_TMPL.format(
        question=case["question"],
        files="\n".join(f"- {f}" for f in case["files"]),
    )


def cmd_prompts(cfg: dict) -> int:
    PROMPTS.mkdir(exist_ok=True)
    RESPONSES.mkdir(exist_ok=True)
    per = cfg["chars_per_token"]
    print("| Case | Files | Corpus lines | Baseline tokens | Prompt tokens |")
    print("|------|-------|--------------|-----------------|---------------|")
    for case in cfg["cases"]:
        body = prompt_text(case)
        (PROMPTS / f"{case['id']}.txt").write_text(body, encoding="utf-8")
        corpus = "".join(read(f) for f in case["files"])
        print(f"| {case['id']} | {len(case['files'])} | {len(corpus.splitlines())} | "
              f"{tokens(corpus, per)} | {tokens(body, per)} |")
    nxt = f"run-{len(runs()) + 1:03d}"
    print(f"\nWrote {len(cfg['cases'])} prompts to {PROMPTS}")
    print(f"Dispatch each to the bulk-reader subagent, save the reply verbatim to "
          f"{RESPONSES}/{nxt}/<case-id>.md, then run: python run_tests.py score")
    print("The worker is non-deterministic, so one run is a sample. `score` reads every "
          "run-* directory and reports the spread.")
    return 0


# --- score -----------------------------------------------------------------

def grade(case: dict, answer: str, cfg: dict) -> dict:
    tol = cfg["anchor_tolerance_lines"]
    found = anchors(answer)
    hit_facts = anchored_facts = neg_ok = 0
    positives = negatives = 0
    misses: list[str] = []

    for fact in case["facts"]:
        if fact.get("expect") == "no-match":
            negatives += 1
            if no_match_stated(answer, fact["file"]):
                neg_ok += 1
            else:
                misses.append(f"{fact['id']}(no-match not stated)")
            continue
        positives += 1
        if mentions(answer, fact["must_mention"]):
            hit_facts += 1
        else:
            misses.append(fact["id"])
        lines = truth_lines(fact)
        if any(same_file(p, fact["file"]) and any(s - tol <= t <= e + tol for t in lines)
               for p, s, e in found):
            anchored_facts += 1

    # An anchor is a ghost when it points past the end of a file it names, or names a
    # file that was never sent. Either way the caller would read the wrong place.
    lengths = {f: len(read(f).splitlines()) for f in case["files"]}
    ghosts = 0
    for path, start, end in found:
        owner = next((f for f in case["files"] if same_file(path, f)), None)
        if owner is None or max(start, end) > lengths[owner]:
            ghosts += 1

    # `SKILL.md` names nothing when eight of them were sent, so a file counts as reported
    # only via a name no sibling in this case shares.
    shared = {n for f in case["files"] for n in set(names_for(f))
              if sum(n in names_for(g) for g in case["files"]) > 1}
    covered = sum(1 for f in case["files"]
                  if any(n in answer for n in names_for(f) if n not in shared))

    # The skill warns the Coverage rows run about a line long each. Measure it rather
    # than take its word: a stated count is the only claim in the reply that is checkable
    # without reading the file, so it is the cheapest read on how careful the worker was.
    row_err = rows_seen = 0
    for path, count in COVERAGE_ROW.findall(answer):
        owner = next((f for f in case["files"] if same_file(path.replace("\\", "/"), f)), None)
        if owner:
            rows_seen += 1
            row_err += abs(int(count.replace(",", "")) - lengths[owner])

    per = cfg["chars_per_token"]
    corpus = "".join(read(f) for f in case["files"])
    prompt_tok = tokens(prompt_text(case), per)
    answer_tok = tokens(answer, per)

    # The skill mandates re-reading anchored regions before acting. That re-read is part
    # of the delegated cost; leaving it out would flatter the saving.
    win = cfg["verify_window_lines"]
    verify_tok = 0
    for owner in {next((f for f in case["files"] if same_file(p, f)), None) for p, _, _ in found}:
        if owner is None:
            continue
        src = read(owner).splitlines()
        regions = sorted({(s, e) for p, s, e in found if same_file(p, owner)})
        merged: list[tuple[int, int]] = []
        for s, e in regions:
            lo, hi = max(1, s - win), min(len(src), e + win)
            if merged and lo <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
            else:
                merged.append((lo, hi))
        verify_tok += sum(tokens("\n".join(src[lo - 1:hi]), per) for lo, hi in merged)

    return {
        "id": case["id"],
        "kind": case["kind"],
        "baseline": tokens(corpus, per),
        "answer": answer_tok,
        "delegated": prompt_tok + answer_tok + verify_tok,
        "verify": verify_tok,
        "positives": positives,
        "hits": hit_facts,
        "anchored": anchored_facts,
        "negatives": negatives,
        "neg_ok": neg_ok,
        "ghosts": ghosts,
        "coverage": f"{covered}/{len(case['files'])}",
        "rows_seen": rows_seen,
        "row_err": row_err,
        "misses": misses,
    }


def pct(num: float, den: float) -> str:
    return "n/a" if not den else f"{100 * num / den:.0f}%"


def runs() -> list[Path]:
    return sorted(d for d in RESPONSES.glob("run-*") if d.is_dir())


def score_run(cfg: dict, run: Path) -> tuple[list[dict], list[str]]:
    rows, skipped = [], []
    for case in cfg["cases"]:
        f = run / f"{case['id']}.md"
        if f.exists():
            rows.append(grade(case, f.read_text(encoding="utf-8"), cfg))
        else:
            skipped.append(case["id"])
    return rows, skipped


def totals(rows: list[dict]) -> dict:
    keys = ("baseline", "delegated", "answer", "verify", "positives", "hits", "anchored",
            "negatives", "neg_ok", "ghosts", "rows_seen", "row_err")
    return {k: sum(r[k] for r in rows) for k in keys}


def case_table(rows: list[dict]) -> list[str]:
    out = ["| Case | Kind | Direct read | Delegated | Saved | Facts | Anchored | No-match | Ghost anchors | Files reported | Line-count error |",
           "|------|------|-------------|-----------|-------|-------|----------|----------|---------------|----------------|------------------|"]
    for r in rows:
        out.append(
            f"| {r['id']} | {r['kind']} | {r['baseline']} | {r['delegated']} | "
            f"{pct(r['baseline'] - r['delegated'], r['baseline'])} | "
            f"{r['hits']}/{r['positives']} | {r['anchored']}/{r['positives']} | "
            f"{r['neg_ok']}/{r['negatives']} | {r['ghosts']} | {r['coverage']} | "
            f"+{r['row_err']} over {r['rows_seen']} rows |"
        )
    return out


def cmd_score(cfg: dict) -> int:
    found = runs()
    if not found:
        print(f"No run directories in {RESPONSES}. Run `prompts`, then save each reply to "
              f"{RESPONSES}/run-001/<case-id>.md.")
        return 1

    scored = {run.name: score_run(cfg, run) for run in found}
    names = list(scored)

    out = ["# delegate-bulk-reads: token saving vs accuracy loss", ""]
    out += [f"{len(names)} run(s): {', '.join(names)}. Corpus: this repo. Token estimate: "
            f"chars / {cfg['chars_per_token']}. Delegated cost = prompt + reply + the verification "
            f"re-reads the skill mandates (+/-{cfg['verify_window_lines']} lines around every "
            f"distinct anchor).", ""]

    # --- headline: one row per run ---
    out += ["## Runs compared", "",
            "| Run | Direct read | Delegated | Saved | Fact recall | Anchored | No-match | Ghosts | Coverage error |",
            "|-----|-------------|-----------|-------|-------------|----------|----------|--------|----------------|"]
    for name in names:
        t = totals(scored[name][0])
        out.append(
            f"| {name} | {t['baseline']} | {t['delegated']} | "
            f"{pct(t['baseline'] - t['delegated'], t['baseline'])} | "
            f"{pct(t['hits'], t['positives'])} ({t['hits']}/{t['positives']}) | "
            f"{pct(t['anchored'], t['positives'])} | "
            f"{t['neg_ok']}/{t['negatives']} | {t['ghosts']} | "
            f"+{t['row_err']} over {t['rows_seen']} rows |"
        )

    # --- per-case spread: the same case, run to run ---
    out += ["", "## Per case, across runs", "",
            "| Case | " + " | ".join(f"{n} saved" for n in names) + " | "
            + " | ".join(f"{n} facts" for n in names) + " |",
            "|------|" + "|".join(["---"] * 2 * len(names)) + "|"]
    by_case: dict[str, dict[str, dict]] = {}
    for name in names:
        for r in scored[name][0]:
            by_case.setdefault(r["id"], {})[name] = r
    for cid, per_run in by_case.items():
        saved = [pct(per_run[n]["baseline"] - per_run[n]["delegated"], per_run[n]["baseline"])
                 if n in per_run else "-" for n in names]
        facts = [f"{per_run[n]['hits']}/{per_run[n]['positives']}" if n in per_run else "-"
                 for n in names]
        out.append(f"| {cid} | " + " | ".join(saved) + " | " + " | ".join(facts) + " |")

    # --- fact-level stability: is the same thing lost every time? ---
    missed: dict[str, list[str]] = {}
    for name in names:
        for r in scored[name][0]:
            for m in r["misses"]:
                missed.setdefault(f"{r['id']} / {m}", []).append(name)
    if missed:
        out += ["", "## What was lost, and in how many runs", "",
                "A miss in every run is a property of the question. A miss in one is variance.", "",
                "| Fact | Missed in |", "|------|-----------|"]
        for fact, where in sorted(missed.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            out.append(f"| {fact} | {len(where)}/{len(names)} ({', '.join(where)}) |")

    # --- full per-run detail ---
    for name in names:
        rows, skipped = scored[name]
        out += ["", f"## {name} in detail", ""] + case_table(rows)
        t = totals(rows)
        out += ["", f"- Saved **{pct(t['baseline'] - t['delegated'], t['baseline'])}** "
                    f"({t['baseline'] - t['delegated']} tokens); reply {t['answer']} + "
                    f"verification re-reads {t['verify']} + prompts.",
                f"- Fact recall **{pct(t['hits'], t['positives'])}** ({t['hits']}/{t['positives']}), "
                f"anchors within {cfg['anchor_tolerance_lines']} lines "
                f"**{pct(t['anchored'], t['positives'])}**, ghost anchors **{t['ghosts']}**."]
        if t["baseline"] - t["delegated"] > 0 and t["positives"] - t["hits"] > 0:
            out.append(f"- Exchange rate: **{(t['baseline'] - t['delegated']) // (t['positives'] - t['hits'])} "
                       f"tokens saved per fact lost**.")
        elif t["positives"] == t["hits"]:
            out.append("- Exchange rate: no facts lost.")
        if skipped:
            out.append(f"- Not run (no response file): {', '.join(skipped)}")

    text = "\n".join(out) + "\n"
    (HERE / "report.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"Written to {HERE / 'report.md'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=("check", "prompts", "score"))
    mode = ap.parse_args().mode
    cfg = load_cases()
    return {"check": cmd_check, "prompts": cmd_prompts, "score": cmd_score}[mode](cfg)


if __name__ == "__main__":
    sys.exit(main())
