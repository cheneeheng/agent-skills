# Triggering raw results — run-002 / iteration-1 (lite, N=1, cold subagents)

Method: each prompt handed to a fresh `general-purpose` subagent framed as a normal Claude Code
session with the skill library available; agent told to "begin handling as you normally would …
report which skill(s) you loaded". Final `SKILLS_LOADED:` line recorded. N=1 (lite sanity, not a
statistic). NOTE: this framing asks the agent to deliberate about skill choice, which primes
skill-consideration and likely inflates positive triggering vs. natural cold invocation. See the
contradiction note in SKILL_EVAL §03.

## Positives (should fire write-less-code)

| ID | Prompt (abridged) | SKILLS_LOADED | Fired? |
|----|-------------------|---------------|--------|
| P1 | "date picker in Signup.tsx — leanest way" | ceh-agent-coding-contract:write-less-code | yes |
| P2 | "csv export … without pulling in another dependency" | ceh-agent-coding-contract:write-less-code | yes |
| P3 | "write less code … dedupe a list of user ids" | ceh-agent-coding-contract:write-less-code | yes |
| P4 | "config loader feels over-engineered … add env var" | ceh-agent-coding-contract:write-less-code | yes |
| P5 | "yagni mode … retry-with-backoff" | ceh-agent-coding-contract:write-less-code | yes |
| P6 | "json config parser in go … lazy version first" | ceh-agent-coding-contract:write-less-code | yes |

Positive trigger rate: **6/6**.

## Near-miss negatives (should NOT fire write-less-code)

| ID | Prompt (abridged) | SKILLS_LOADED | False positive? |
|----|-------------------|---------------|-----------------|
| N1 | "PR is bloated … review it, leave comments" | ceh-git-workflow:code-review | no (correct route) |
| N2 | "remove the unused lodash dependency" | ceh-git-workflow:dependency-management | no (correct route) |
| N3 | "build failing with TS2345 … fix it" | none | no |
| N4 | "do this properly — full OAuth2 … no shortcuts" | none | no |
| N5 | "comprehensive test suite for payment module" | none | no |
| N6 | "refactor 800-line god class into modules" | write-less-code + agent-coding-contract | borderline yes |

Near-miss false-positive rate: **1/6** (N6). N6 is defensible: the agent loaded write-less-code to
apply "deletion over addition / collapse duplication" *while* refactoring, which is on-claim, not a
keyword misfire. Treat effective FP as 0–1/6; either way ≤ threshold (1/6 default → 0.6/6 scaled).
