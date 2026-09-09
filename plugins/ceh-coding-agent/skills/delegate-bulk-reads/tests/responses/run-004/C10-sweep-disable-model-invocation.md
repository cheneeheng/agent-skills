## Answer
- `refactor-repo` sets `disable-model-invocation: true` — plugins/ceh-coding-agent/skills/refactor-repo/SKILL.md:3
- `evaluate-skill` sets `disable-model-invocation: true` — plugins/ceh-evaluation/skills/evaluate-skill/SKILL.md:3
- `lessons-learned` sets `disable-model-invocation: true` — plugins/ceh-lessons-learned/skills/lessons-learned/SKILL.md:3
- `orchestrate` sets `disable-model-invocation: true` — plugins/ceh-orchestration/skills/orchestrate/SKILL.md:3
- `summarize-chat` sets `disable-model-invocation: true` — plugins/ceh-summarize-chat/skills/summarize-chat/SKILL.md:3
- `shrink-diff` does not set it — plugins/ceh-coding-agent/skills/shrink-diff/SKILL.md:1-20 (frontmatter has no `disable-model-invocation` key)
- `design-test-cases` does not set it — plugins/ceh-testing/skills/design-test-cases/SKILL.md:1-14 (frontmatter has no `disable-model-invocation` key)

## Not found / uncertain
- Nothing outstanding.

## Coverage
- plugins/ceh-coding-agent/skills/refactor-repo/SKILL.md — 20 lines read
- plugins/ceh-evaluation/skills/evaluate-skill/SKILL.md — 20 lines read
- plugins/ceh-lessons-learned/skills/lessons-learned/SKILL.md — 20 lines read
- plugins/ceh-orchestration/skills/orchestrate/SKILL.md — 20 lines read
- plugins/ceh-summarize-chat/skills/summarize-chat/SKILL.md — 20 lines read
- plugins/ceh-coding-agent/skills/shrink-diff/SKILL.md — 20 lines read
- plugins/ceh-testing/skills/design-test-cases/SKILL.md — 20 lines read
- Total: 140 lines across 7 files. Only the frontmatter and immediately following lines were read since the question concerns only frontmatter keys.
