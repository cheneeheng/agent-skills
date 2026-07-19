#!/bin/bash
# usage-limit-watch.sh — PostToolUse hook (all tools)
#
# Reads the 5-hour rate-limit percentage that the user's statusline export
# writes to ~/.claude/statusline/<project-dir>/<session_id>.jsonl and, when it
# crosses the threshold, feeds a message back to Claude (exit 2) instructing it
# to stop starting new work and run the usage-limit-handoff skill.
#
# Prerequisites (documented in the plugin README): jq, and a statusline script
# that exports its stdin JSON to that path — e.g. ~/.claude/statusline-hook.ps1
# with C4_STATUSLINE_EXPORT=1. Without either, the hook is inert.
#
# Config (env or defaults):
#   CEH_USAGE_LIMIT_THRESHOLD  5h used_percentage that triggers handoff (default 95)
#
# Anti-spam: after firing, re-fires only when usage has climbed 5 more points,
# so an ignored warning escalates instead of repeating on every tool call.

set -euo pipefail

# Without jq the hook cannot parse its payload — degrade to inert. See README.
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)

session_id=$(printf '%s' "$input" | jq -r '.session_id // "default"')
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
[ -n "$cwd" ] || exit 0

# Encode cwd the same way the statusline export does (: and separators -> -)
enc=$(printf '%s' "$cwd" | sed -e 's/:/-/g' -e 's,[/\\],-,g')
log_file="$HOME/.claude/statusline/$enc/$session_id.jsonl"
[ -f "$log_file" ] || exit 0

last=$(tail -n 1 "$log_file" 2>/dev/null) || exit 0
[ -n "$last" ] || exit 0

pct=$(printf '%s' "$last" | jq -r '.data.rate_limits.five_hour.used_percentage // empty' 2>/dev/null) || exit 0
[ -n "$pct" ] || exit 0
pct=${pct%%.*}

threshold="${CEH_USAGE_LIMIT_THRESHOLD:-95}"
[ "$pct" -ge "$threshold" ] || exit 0

# Fire once per 5-point band above the threshold, not on every tool call
state_file="/tmp/ceh-usage-limit-${session_id}"
last_fired=$(cat "$state_file" 2>/dev/null || echo "-999")
[ "$pct" -ge $(( last_fired + 5 )) ] || exit 0
printf '%s' "$pct" > "$state_file"

msg="ceh usage-limit guard: 5-hour usage is at ${pct}% (threshold ${threshold}%). Do not start new subtasks, tool-call chains, or subagents. Finish only the current atomic step, then load and follow the ceh-agent-coding-contract:usage-limit-handoff skill: report what is done and what is open, and end the turn."

resets_at=$(printf '%s' "$last" | jq -r '.data.rate_limits.five_hour.resets_at // empty' 2>/dev/null || echo "")
if [ -n "$resets_at" ]; then
  reset_fmt=$(date -d "@$resets_at" '+%H:%M' 2>/dev/null || echo "")
  [ -n "$reset_fmt" ] && msg="$msg The 5-hour window resets at ${reset_fmt}."
fi

echo "$msg" >&2
exit 2
