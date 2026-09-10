#!/usr/bin/env python3
"""Run a skill's evals/evals.json as isolated with-skill and without-skill `claude -p` sessions.

Writes skill-creator's workspace layout, so its aggregate_benchmark.py and
eval-viewer/generate_review.py read the result unchanged:

  <workspace>/iteration-<N>/eval-<id>-<name>/
      eval_metadata.json
      <config>/run-<K>/timing.json
      <config>/run-<K>/outputs/{transcript.jsonl,final_message.md,commits.txt,status.txt,refs.txt}

Each run gets a fresh git repo built from the eval's `setup` steps, and a `claude -p` session
with --setting-sources project, so no user-installed plugin (the one under test included) or
user hook reaches either arm. The with-skill arm is told to read SKILL.md first; the baseline
is not. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# less-code: fixed allowlist sized for local-git skills; skills that call gh or push need a
# per-eval override (and a gh stand-in) when they get evals.
ALLOWED_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep",
    "Bash(git:*)", "PowerShell(git:*)",
    "Bash(rm:*)", "PowerShell(rm:*)", "PowerShell(Remove-Item:*)",
]


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout


def build_fixture(setup: list[dict], remote: bool = False) -> Path:
    """Fresh repo at <tmp>/repo. Each step switches to its branch, writes its files, commits them
    if it names a message, then tags. With `remote`, a bare <tmp>/origin.git gets every branch
    and tag, upstreams set."""
    repo = Path(tempfile.mkdtemp(prefix="skill-eval-")) / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Eval User")
    git(repo, "config", "user.email", "eval@example.com")
    git(repo, "config", "commit.gpgsign", "false")
    for step in setup:
        if "branch" in step:
            try:
                git(repo, "switch", "-q", step["branch"])
            except subprocess.CalledProcessError:
                git(repo, "switch", "-q", "-c", step["branch"])
        for path, content in step.get("files", {}).items():
            f = repo / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8", newline="\n")
        if "commit" in step:
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", step["commit"])
        if "tag" in step:
            git(repo, "tag", "-a", step["tag"], "-m", step["tag"])
    if remote:
        git(repo.parent, "init", "-q", "--bare", "-b", "main", "origin.git")
        git(repo, "remote", "add", "origin", str(repo.parent / "origin.git"))
        git(repo, "push", "-q", "-u", "origin", "--all")
        git(repo, "push", "-q", "origin", "--tags")
    return repo


def run_one(skill_md: Path, ev: dict, config: str, run_dir: Path, model: str, timeout: int) -> None:
    repo = build_fixture(ev.get("setup", []), ev.get("remote", False))
    base = git(repo, "rev-parse", "HEAD").strip()
    prompt = ev["prompt"]
    cmd = [
        "claude", "-p", "--setting-sources", "project", "--no-session-persistence",
        "--model", model, "--output-format", "stream-json", "--verbose",
    ]
    if config == "with_skill":
        prompt = f"Before you start, read the skill at {skill_md} and follow it.\n\n{prompt}"
        cmd += ["--add-dir", str(skill_md.parent)]
    cmd += ["--allowedTools", *ALLOWED_TOOLS]  # variadic, so it goes last; the prompt is stdin

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    start = time.time()
    proc = subprocess.run(
        cmd, cwd=repo, input=prompt, capture_output=True, text=True, encoding="utf-8",
        env=env, timeout=timeout,
    )
    elapsed = time.time() - start

    out = run_dir / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    (out / "transcript.jsonl").write_text(proc.stdout, encoding="utf-8")
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
    result = next((e for e in reversed(events) if e.get("type") == "result"), {})
    usage = result.get("usage", {})
    (run_dir / "timing.json").write_text(json.dumps({
        "total_tokens": sum(usage.get(k, 0) for k in (
            "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"
        )),
        "duration_ms": result.get("duration_ms", int(elapsed * 1000)),
        "total_duration_seconds": round(elapsed, 1),
        "total_cost_usd": result.get("total_cost_usd"),
        "permission_denials": result.get("permission_denials", []),
    }, indent=2), encoding="utf-8")
    (out / "final_message.md").write_text(result.get("result", proc.stderr), encoding="utf-8")
    (out / "commits.txt").write_text(
        git(repo, "log", "--reverse", "--stat", "--format=commit %H%nparents %P%n%B", f"{base}..HEAD")
        or "(no new commits)\n", encoding="utf-8",
    )
    (out / "status.txt").write_text(
        git(repo, "status", "--porcelain", "--untracked-files=all") or "(clean)\n", encoding="utf-8"
    )
    # Branch/tag skills leave their result in refs, not in the working tree: the whole graph,
    # tag object types (annotated shows as `tag`), and what origin received.
    refs = [
        "HEAD: " + git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        git(repo, "log", "--graph", "--all", "--oneline", "--decorate"),
        "tags:\n" + git(repo, "for-each-ref", "--format=%(refname:short) %(objecttype)", "refs/tags"),
    ]
    if (repo.parent / "origin.git").is_dir():
        refs.append("origin:\n" + git(repo.parent / "origin.git", "for-each-ref",
                                      "--format=%(refname) %(objectname:short)"))
    (out / "refs.txt").write_text("\n".join(refs), encoding="utf-8")
    # git marks object files read-only, which rmtree cannot delete on Windows without a chmod.
    shutil.rmtree(repo.parent, onexc=lambda func, path, _: (os.chmod(path, stat.S_IWRITE), func(path)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("skill_dir", type=Path, help="skill folder holding SKILL.md and evals/evals.json")
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--iteration", type=int, default=1)
    ap.add_argument("--runs", type=int, default=1, help="runs per eval per configuration")
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=600, help="seconds per run")
    ap.add_argument("--only", type=int, nargs="*", help="eval ids to run (default: all)")
    args = ap.parse_args()

    skill_md = (args.skill_dir / "SKILL.md").resolve()
    evals = json.loads((args.skill_dir / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
    jobs = []
    for ev in evals:
        if args.only and ev["id"] not in args.only:
            continue
        ev_dir = args.workspace / f"iteration-{args.iteration}" / f"eval-{ev['id']}-{ev['name']}"
        meta = json.dumps({
            "eval_id": ev["id"], "eval_name": ev["name"], "prompt": ev["prompt"],
            "assertions": ev.get("expectations", []),
        }, indent=2)
        run_dirs = [(cfg, ev_dir / cfg / f"run-{k}")
                    for cfg in ("with_skill", "without_skill") for k in range(1, args.runs + 1)]
        # aggregate_benchmark reads the eval dir's copy; the viewer looks only in the run dir and its parent.
        for d in (ev_dir, *(rd for _, rd in run_dirs)):
            d.mkdir(parents=True, exist_ok=True)
            (d / "eval_metadata.json").write_text(meta, encoding="utf-8")
        jobs += [(ev, cfg, rd) for cfg, rd in run_dirs]

    with ThreadPoolExecutor(args.workers) as pool:
        futures = {
            pool.submit(run_one, skill_md, ev, cfg, rd, args.model, args.timeout): rd
            for ev, cfg, rd in jobs
        }
        for f in as_completed(futures):
            try:
                f.result()
                print("done  ", futures[f])
            except Exception as e:  # one failed run must not sink the batch
                print("FAILED", futures[f], e)


if __name__ == "__main__":
    main()
