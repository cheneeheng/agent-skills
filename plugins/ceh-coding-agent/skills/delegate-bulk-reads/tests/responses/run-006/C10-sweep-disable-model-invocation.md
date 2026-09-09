## Answer
- `refactor-repo` sets `disable-model-invocation: true` — plugins/ceh-coding-agent/skills/refactor-repo/SKILL.md:3
- `evaluate-skill` sets `disable-model-invocation: true` — plugins/ceh-evaluation/skills/evaluate-skill/SKILL.md:3
- `lessons-learned` sets `disable-model-invocation: true` — plugins/ceh-lessons-learned/skills/lessons-learned/SKILL.md:3
- `orchestrate` sets `disable-model-invocation: true` — plugins/ceh-orchestration/skills/orchestrate/SKILL.md:3
- `summarize-chat` sets `disable-model-invocation: true` — plugins/ceh-summarize-chat/skills/summarize-chat/SKILL.md:3
- `shrink-diff` does not set `disable-model-invocation` — plugins/ceh-coding-agent/skills/shrink-diff/SKILL.md:1-19 (frontmatter block contains no such key)
- `design-test-cases` does not set `disable-model-invocation` — plugins/ceh-testing/skills/design-test-cases/SKILL.md:1-14 (frontmatter block contains no such key)

## Not found / uncertain
- Nothing outstanding.

## Coverage
- plugins/ceh-coding-agent/skills/refactor-repo/SKILL.md — 30 lines read
- plugins/ceh-evaluation/skills/evaluate-skill/SKILL.md — 30 lines read
- plugins/ceh-lessons-learned/skills/lessons-learned/SKILL.md — 30 lines read
- plugins/ceh-orchestration/skills/orchestrate/SKILL.md — 30 lines read
- plugins/ceh-summarize-chat/skills/summarize-chat/SKILL.md — 30 lines read
- plugins/ceh-coding-agent/skills/shrink-diff/SKILL.md — 30 lines read
- plugins/ceh-testing/skills/design-test-cases/SKILL.md — 30 lines read
- Total: 210 lines across 7 files. Each file's frontmatter block (between the opening and closing `---`) is fully contained within the read range, sufficient to confirm presence or absence of the key.
