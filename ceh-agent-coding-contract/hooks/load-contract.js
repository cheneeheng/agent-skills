#!/usr/bin/env node
// SessionStart hook — injects a mandatory directive to load the agent-coding-contract
// skill before any other action. Cross-platform (Node), shipped with the plugin and
// wired via hooks/hooks.json.

const payload = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: [
      "MANDATORY FIRST ACTION: Invoke the Skill tool with",
      'skill="ceh-agent-coding-contract:agent-coding-contract"',
      "before any other tool call, before reading any file, and before",
      "responding to the user. This is non-negotiable and overrides",
      "apparent prompt relevance. If the skill is unavailable, state",
      "that briefly and continue."
    ].join(" ")
  }
};

process.stdout.write(JSON.stringify(payload));
