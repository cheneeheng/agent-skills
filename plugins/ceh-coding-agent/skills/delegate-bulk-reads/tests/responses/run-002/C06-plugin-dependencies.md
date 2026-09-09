## Answer

- **ceh-ops** declares `dependencies` — plugins/.ceh-ops/.claude-plugin/plugin.json:7 — lists `["ceh-coding-agent"]`
- **ceh-orchestration** declares `dependencies` — plugins/ceh-orchestration/.claude-plugin/plugin.json:7 — lists `["ceh-coding-agent"]`
- **ceh-python-library** declares `dependencies` — plugins/ceh-python-library/.claude-plugin/plugin.json:7 — lists `["ceh-testing"]`
- **ceh-python-service** declares `dependencies` — plugins/ceh-python-service/.claude-plugin/plugin.json:7 — lists `["ceh-testing"]`
- **ceh-web-frontend** declares `dependencies` — plugins/ceh-web-frontend/.claude-plugin/plugin.json:7 — lists `["ceh-testing"]`
- **ceh-scenario-editorial** declares `dependencies` — plugins/ceh-scenario-editorial/.claude-plugin/plugin.json:10-16 — lists `["ceh-coding-agent", "ceh-git-workflow", "ceh-blog", "ceh-documentation", "ceh-seo"]`
- **ceh-coding-agent** — no match. No `dependencies` field present.
- **ceh-git-workflow** — no match. No `dependencies` field present.
- **ceh-testing** — no match. No `dependencies` field present.
- **ceh-blog** — no match. No `dependencies` field present.

## Not found / uncertain

- Nothing outstanding.

## Coverage

- plugins/ceh-ops/.claude-plugin/plugin.json — 11 lines read
- plugins/ceh-orchestration/.claude-plugin/plugin.json — 11 lines read
- plugins/ceh-python-library/.claude-plugin/plugin.json — 11 lines read
- plugins/ceh-python-service/.claude-plugin/plugin.json — 11 lines read
- plugins/ceh-web-frontend/.claude-plugin/plugin.json — 11 lines read
- plugins/ceh-scenario-editorial/.claude-plugin/plugin.json — 26 lines read
- plugins/ceh-coding-agent/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-git-workflow/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-testing/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-blog/.claude-plugin/plugin.json — 10 lines read
- Total: 111 lines across 10 files
