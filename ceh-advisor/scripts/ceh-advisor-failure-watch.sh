#!/bin/bash
# ceh-advisor-failure-watch.sh — PostToolUse hook (matcher: Bash)
#
# Counts consecutive failed Bash tool calls in the session. When the count
# reaches the threshold, feeds a message back to Claude (exit 2) instructing
# it to stop iterating and consult ceh-advisor to re-examine the diagnosis.
#
# Config (env or defaults):
#   CEH_ADVISOR_FAIL_THRESHOLD  consecutive failures before firing (default 3)

set -euo pipefail

# Without jq the hook cannot parse its payload — degrade to inert. See README.
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)

tool_name=$(printf '%s' "$input" | jq -r '.tool_name // empty')
[ "$tool_name" = "Bash" ] || exit 0

session_id=$(printf '%s' "$input" | jq -r '.session_id // "default"')
threshold="${CEH_ADVISOR_FAIL_THRESHOLD:-3}"
state_file="/tmp/ceh-advisor-failcount-${session_id}"

# --- Failure detection (defensive across response shapes) ---
# Claude Code's PostToolUse payload shape has varied; check several signals.
is_error=$(printf '%s' "$input" | jq -r '
  (.tool_response.is_error // .tool_result.is_error // false)' 2>/dev/null || echo false)

resp_text=$(printf '%s' "$input" | jq -r '
  (.tool_response | tostring) // (.tool_result | tostring) // ""' 2>/dev/null || echo "")

failed=false
if [ "$is_error" = "true" ]; then
  failed=true
elif printf '%s' "$resp_text" | grep -Eq '(Exit code:? [1-9]|exited with code [1-9]|command not found|Traceback \(most recent call last\)|FAILED|AssertionError|npm ERR!)'; then
  failed=true
fi

if [ "$failed" = "false" ]; then
  # Success resets the streak
  rm -f "$state_file"
  exit 0
fi

count=0
[ -f "$state_file" ] && count=$(cat "$state_file" 2>/dev/null || echo 0)
count=$(( count + 1 ))
printf '%s' "$count" > "$state_file"

if [ "$count" -ge "$threshold" ]; then
  # Reset so we don't fire on every subsequent failure
  rm -f "$state_file"
  echo "ceh-advisor guard: ${count} consecutive failed commands. Stop iterating on the current fix. Invoke the ceh-advisor subagent via the Task tool with a handoff block (Situation / what you've tried / current diagnosis / relevant files) and have it challenge the DIAGNOSIS, not just the patch, before attempting another fix." >&2
  exit 2
fi

exit 0
