## Answer
- The skill says Coverage rows do sum correctly, but each file's line count usually comes back inflated by about one line, because a trailing newline is miscounted as an extra line — "the rows do add up — the worker sums them correctly — and each file usually comes back about one line too long, because a trailing newline reads as an extra line" — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:80-82
  - The more dangerous failure it warns about is a partial read reported as if complete: "a worker that read only the first 50 lines of a 300-line file reports `50 lines read`, accurately, under an answer that looks finished" — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:83-84
  - It instructs treating Coverage as a claim to verify, not a trusted count: "Treat `Coverage` as a claim, never as a count." — plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md:80
- The agent spec (bulk-reader.md) requires the Total to be computed by adding the already-written rows, not produced independently: "`Total` is the rows added up. Write the rows first, then add them; a total you produced any other way is a guess, and the caller treats that number as a coverage guarantee." — plugins/ceh-coding-agent/agents/bulk-reader.md:55-56
  - The output template itself defines Total as "the sum of the rows above" — plugins/ceh-coding-agent/agents/bulk-reader.md:49

## Not found / uncertain
- Nothing outstanding.

## Coverage
- plugins/ceh-coding-agent/skills/delegate-bulk-reads/SKILL.md — 93 lines read
- plugins/ceh-coding-agent/agents/bulk-reader.md — 91 lines read
- Total: 184 lines across 2 files.
