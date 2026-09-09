## Answer
- The skill says `Coverage` must be treated as a claim, never a count, and identifies two specific failure patterns — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:80-86
  - Off-by-one noise: "each file usually comes back about one line too long, because a trailing newline reads as an extra line" — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:81-82
  - The real risk: "a worker that read only the first 50 lines of a 300-line file reports `50 lines read`, accurately, under an answer that looks finished" — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:83-84
  - Remedy stated: "Compare the row against the real length whenever the answer matters — it is the only claim in the reply you can check without opening the file." — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:85-86
- The agent spec's requirement on how `Total` is produced — plugins/ceh-coding-agent/agents/bulk-reader.md:55-56
  - Verbatim: "`Total` is the rows added up. Write the rows first, then add them; a total you produced any other way is a guess, and the caller treats that number as a coverage guarantee." — plugins/ceh-coding-agent/agents/bulk-reader.md:55-56

## Not found / uncertain
- Nothing outstanding.

## Coverage
- plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md — 93 lines read
- plugins/ceh-coding-agent/agents/bulk-reader.md — 91 lines read
- Total: 184 lines across 2 files. Nothing skipped.
