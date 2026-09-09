## Answer

- Coverage section problem: "each file usually comes back about one line too long, because a trailing newline reads as an extra line" — SKILL.md:81-82
  - The worse issue is silent omission: "a worker that read only the first 50 lines of a 300-line file reports `50 lines read`, accurately, under an answer that looks finished" — SKILL.md:83-84

- Total production requirement: "`Total` is the rows added up. Write the rows first, then add them; a total you produced any other way is a guess, and the caller treats that number as a coverage guarantee." — bulk-reader.md:55-56

## Not found / uncertain

- Nothing outstanding.

## Coverage

- SKILL.md — 93 lines read
- bulk-reader.md — 91 lines read
- Total: 184 lines across 2 files.
