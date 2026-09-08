## Answer

- **What the skill says is wrong with Coverage numbers** — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:80-86: "The rows do add up — the worker sums them correctly — and each file usually comes back about one line too long, because a trailing newline reads as an extra line. Do not let that small familiar error teach you to skim the section. The case that costs you is the other one: a worker that read only the first 50 lines of a 300-line file reports `50 lines read`, accurately, under an answer that looks finished."

- **What the agent spec requires about how Total is produced** — plugins/ceh-coding-agent/agents/bulk-reader.md:55-56: "Write the rows first, then add them; a total you produced any other way is a guess, and the caller treats that number as a coverage guarantee."

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md — 93 lines read
- plugins/ceh-coding-agent/agents/bulk-reader.md — 91 lines read
- Total: 184 lines across 2 files.
