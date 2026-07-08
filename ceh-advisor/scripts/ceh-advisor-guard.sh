#!/bin/bash
# ceh-advisor-guard.sh — PreToolUse hook (matcher: Bash)
#
# Hard-trigger backstop for ceh-advisor. Denies destructive bash commands
# unless a fresh advisor acknowledgement exists, forcing the main session
# to consult ceh-advisor before irreversible actions.
#
# Protocol:
#   1. Destructive command detected, no fresh ack -> deny with instructions.
#   2. Main session invokes ceh-advisor (Task tool) with a handoff block.
#   3. Main session writes the advisor's one-line verdict into the ack file
#      (this doubles as an audit trail).
#   4. Re-run the command; ack is fresh -> allowed.
#
# Config (env or defaults):
#   CEH_ADVISOR_ACK_TTL   seconds an ack stays valid (default 900 = 15 min)
#   CEH_ADVISOR_PATTERNS  extra patterns file, one ERE per line (optional)

set -euo pipefail

# Without jq the hook cannot parse its payload or emit decisions — degrade to
# inert (exit 0 allows) rather than erroring on every Bash call. See README.
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)

tool_name=$(printf '%s' "$input" | jq -r '.tool_name // empty')
[ "$tool_name" = "Bash" ] || exit 0

cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
[ -n "$cmd" ] || exit 0

project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
ack_file="$project_dir/.claude/.ceh-advisor-ack"
ttl="${CEH_ADVISOR_ACK_TTL:-900}"

# --- Destructive patterns (extended regex, one per line) ---
patterns='rm[[:space:]]+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)[a-zA-Z]*[[:space:]]
git[[:space:]]+push[[:space:]].*(--force|[[:space:]]-f([[:space:]]|$))
git[[:space:]]+reset[[:space:]]+--hard
git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f
git[[:space:]]+branch[[:space:]]+-D
DROP[[:space:]]+(TABLE|DATABASE|SCHEMA)
TRUNCATE[[:space:]]+TABLE
(prisma|alembic|rails|django-admin|manage\.py|npx[[:space:]]+prisma)[[:space:]]+.*migrate
terraform[[:space:]]+(apply|destroy)
kubectl[[:space:]]+delete
docker[[:space:]]+(system|volume|image)[[:space:]]+prune
aws[[:space:]]+s3[[:space:]]+(rm|rb)'

# Merge user-supplied extra patterns if present
extra="${CEH_ADVISOR_PATTERNS:-$project_dir/.claude/ceh-advisor-patterns.txt}"
if [ -f "$extra" ]; then
  patterns="$patterns
$(cat "$extra")"
fi

matched=""
while IFS= read -r pat; do
  [ -n "$pat" ] || continue
  if printf '%s' "$cmd" | grep -Eq "$pat"; then
    matched="$pat"
    break
  fi
done <<< "$patterns"

# Not destructive -> allow silently
[ -n "$matched" ] || exit 0

# Destructive: check for a fresh advisor ack
if [ -f "$ack_file" ]; then
  now=$(date +%s)
  mtime=$(stat -c %Y "$ack_file" 2>/dev/null || stat -f %m "$ack_file")
  age=$(( now - mtime ))
  if [ "$age" -le "$ttl" ]; then
    verdict=$(head -c 200 "$ack_file" | tr '\n' ' ')
    jq -n --arg v "$verdict" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "allow",
        permissionDecisionReason: ("ceh-advisor consulted (ack fresh): " + $v)
      }
    }'
    exit 0
  fi
fi

# No fresh ack -> deny with the consult protocol
jq -n --arg cmd "$cmd" --arg ttl "$ttl" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: ("Destructive command blocked by ceh-advisor guard: " + $cmd)
  },
  systemMessage: ("This command is irreversible. Before re-running it: (1) invoke the ceh-advisor subagent via the Task tool with a full handoff block (Situation / Options considered / Leaning toward / Relevant files) covering WHY this command is necessary and its blast radius; (2) write the advisor'\''s one-line verdict into .claude/.ceh-advisor-ack; (3) re-run the command. The ack expires after " + $ttl + " seconds.")
}'
exit 0
