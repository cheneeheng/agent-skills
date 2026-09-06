#!/usr/bin/env python3
"""PreToolUse hook: catch bash commands that dump large files into context.

Closes the obvious hole in bulk-read-guard.py — denying the Read tool does
nothing if `cat bigfile` still works.

Opt-in: does nothing unless BULK_READER_MIN_LINES is set.

Passes through:
  - piped commands (`cat f | grep x`) — the pipe is doing the narrowing
  - redirections (`cat f > out`) — not reading into context at all
  - head/tail with a sane line count — already targeted

Fails open on anything it cannot parse.
"""

import fnmatch
import json
import os
import re
import shlex
import sys

FALLBACK_MIN_LINES = 350
DUMP_COMMANDS = {"cat", "less", "more", "bat", "batcat"}
WINDOW_COMMANDS = {"head", "tail"}
SEGMENT_SPLIT = re.compile(r"&&|\|\||;")


def min_lines():
    """Threshold, or None when enforcement is off."""
    raw = os.environ.get("BULK_READER_MIN_LINES", "").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return FALLBACK_MIN_LINES


def is_allowed(path):
    extra = os.environ.get("BULK_READER_ALLOW", "").strip()
    if not extra:
        return False
    base = os.path.basename(path)
    return any(
        fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(base, pat)
        for pat in extra.split(":") if pat
    )


def count_lines(path):
    try:
        if not os.path.isfile(path):
            return None
        with open(path, "rb") as fh:
            if b"\x00" in fh.read(8192):
                return None
        with open(path, "r", encoding="utf-8", errors="strict") as fh:
            return sum(1 for _ in fh)
    except (OSError, UnicodeDecodeError):
        return None


def window_size(tokens):
    """Explicit -n/-c value for head/tail, if present."""
    for i, tok in enumerate(tokens):
        if tok in ("-n", "-c") and i + 1 < len(tokens):
            try:
                return abs(int(tokens[i + 1].lstrip("+-")))
            except ValueError:
                return None
        if re.fullmatch(r"-\d+", tok):
            return abs(int(tok))
        m = re.fullmatch(r"-[nc](\d+)", tok)
        if m:
            return int(m.group(1))
    return None


def offending_file(segment, threshold):
    if "|" in segment or ">" in segment or "<" in segment:
        return None  # narrowed or redirected — not a context dump

    try:
        tokens = shlex.split(segment)
    except ValueError:
        return None
    if not tokens:
        return None

    cmd = os.path.basename(tokens[0])
    if cmd in WINDOW_COMMANDS:
        size = window_size(tokens)
        if size is None or size < threshold:
            return None  # default 10 lines, or an explicitly small window
    elif cmd not in DUMP_COMMANDS:
        return None

    for tok in tokens[1:]:
        if tok.startswith("-") or not tok:
            continue
        if is_allowed(tok):
            continue
        lines = count_lines(tok)
        if lines is not None and lines >= threshold:
            return tok, lines
    return None


def deny(reason):
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, sys.stdout)
    sys.exit(0)


def main():
    threshold = min_lines()
    if threshold is None:
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        sys.exit(0)

    for segment in SEGMENT_SPLIT.split(command):
        hit = offending_file(segment.strip(), threshold)
        if hit:
            path, lines = hit
            deny(
                f"Blocked: `{path}` is {lines} lines (threshold {threshold}) and this "
                f"command would dump it into context. Decide which you need:\n\n"
                f"1. A specific part: narrow it here. Pipe through grep/sed/awk, or use "
                f"head/tail with a small -n; piped and redirected commands pass through. "
                f"This is the right branch if you are about to edit, debug, or review this "
                f"file, since a summary cannot give you the exact text an edit needs.\n\n"
                f"2. An understanding of the file: invoke the Skill tool with "
                f"skill=\"ceh-coding-agent:delegate-bulk-reads\", then delegate to the "
                f"`bulk-reader` subagent with your question and this path."
            )
    sys.exit(0)


if __name__ == "__main__":
    main()
