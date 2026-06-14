#!/usr/bin/env node
// SessionStart hook — injects a directive to load the write-less-code skill at
// session start, and re-load it on resume/clear/compact (surviving context
// resets). Cross-platform (Node), shipped with the plugin and wired via
// hooks/hooks.json.

const payload = {
  systemMessage: "ceh-agent-coding-contract: loading the write-less-code skill for this session.",
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: [
      "Before implementing anything this session, invoke the Skill tool with",
      'skill="ceh-agent-coding-contract:write-less-code"',
      "to load the minimalism ladder (YAGNI -> stdlib -> native platform feature",
      "-> already-installed dependency -> one line) and apply it before writing",
      "code. If the skill is unavailable, state that briefly and continue."
    ].join(" ")
  }
};

process.stdout.write(JSON.stringify(payload));
