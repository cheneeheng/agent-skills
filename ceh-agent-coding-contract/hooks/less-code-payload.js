#!/usr/bin/env node
// UserPromptSubmit hook — re-injects the write-less-code reflex before every
// prompt so it survives long-session context drift (a once-per-session load
// decays as context grows). The full skill is loaded separately at session
// start via load-less-code.js; this is the compact per-turn digest. Runs
// unconditionally whenever the plugin is enabled. Inspired by ponytail (MIT,
// DietrichGebert).

const payload = {
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: [
      "WRITE LESS CODE — the best code is the code never written. Before writing any code, stop at the first rung that holds:",
      "1. Does this need to exist at all? (YAGNI) — speculative need: skip it, say so in one line.",
      "2. Stdlib does it? Use it.",
      '3. Native platform feature covers it? Use it (<input type="date"> over a picker lib, CSS over JS, DB constraint over app code).',
      "4. Already-installed dependency solves it? Use it — never add a new one for what a few lines do.",
      "5. Can it be one line? One line.",
      "6. Only then: the minimum code that works.",
      "Never simplify away: trust-boundary validation, data-loss handling, security, accessibility, anything explicitly requested.",
      "Mark deliberate shortcuts with a `// less-code:` comment naming the ceiling and upgrade path."
    ].join("\n")
  }
};

process.stdout.write(JSON.stringify(payload));
