#!/usr/bin/env python3
"""usage-limit-watch.py - PostToolUse hook (all tools)

Reads the 5-hour rate-limit percentage that the user's statusline export
writes to ~/.claude/statusline/<project-dir>/<session_id>.jsonl and, when it
crosses the threshold, feeds a message back to Claude (exit 2) instructing it
to stop starting new work and run the usage-limit-handoff skill.

Prerequisite (documented in the plugin README): a statusline script that
exports its stdin JSON to that path - e.g. ~/.claude/statusline-hook.ps1 with
C4_STATUSLINE_EXPORT=1. Without it the hook is inert.

Config (env or defaults):
  CEH_USAGE_LIMIT_THRESHOLD  5h used_percentage that triggers handoff (default 95)

Anti-spam: after firing, re-fires only when usage has climbed 5 more points,
so an ignored warning escalates instead of repeating on every tool call.
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def main() -> None:
    payload = json.loads(sys.stdin.read())

    session_id = payload.get("session_id") or "default"
    cwd = payload.get("cwd")
    if not cwd:
        return

    # Encode cwd the same way the statusline export does (: and separators -> -)
    enc = cwd.replace(":", "-").replace("/", "-").replace("\\", "-")
    log_file = Path.home() / ".claude" / "statusline" / enc / f"{session_id}.jsonl"
    if not log_file.is_file():
        return

    lines = [ln for ln in log_file.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    if not lines:
        return

    try:
        five_hour = json.loads(lines[-1])["data"]["rate_limits"]["five_hour"]
        pct = int(float(five_hour["used_percentage"]))
    except (ValueError, KeyError, TypeError):
        return

    threshold = int(os.environ.get("CEH_USAGE_LIMIT_THRESHOLD", "95"))
    if pct < threshold:
        return

    # Fire once per 5-point band above the threshold, not on every tool call
    state = Path(tempfile.gettempdir()) / f"ceh-usage-limit-{session_id}"
    last_fired = -999
    if state.is_file():
        try:
            last_fired = int(state.read_text(encoding="utf-8").strip())
        except ValueError:
            pass
    if pct < last_fired + 5:
        return
    state.write_text(str(pct), encoding="utf-8")

    msg = (
        f"ceh usage-limit guard: 5-hour usage is at {pct}% (threshold {threshold}%). "
        "Do not start new subtasks, tool-call chains, or subagents. Finish only the current "
        "atomic step, then load and follow the ceh-agent-coding-contract:usage-limit-handoff "
        "skill: report what is done and what is open, and end the turn."
    )

    resets_at = five_hour.get("resets_at")
    if resets_at:
        try:
            reset_fmt = datetime.fromtimestamp(float(resets_at)).strftime("%H:%M")
            msg += f" The 5-hour window resets at {reset_fmt}."
        except (ValueError, TypeError, OSError):
            pass

    print(msg, file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - report, never block a tool call
        # Advisory hook: surface one readable line instead of a traceback on
        # every tool call, and exit 1 (visible warning) rather than 2 (blocks).
        print(f"ceh usage-limit guard disabled this call: {exc}", file=sys.stderr)
        sys.exit(1)
