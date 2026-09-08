## Answer

- ceh-ops — plugins/ceh-ops/.claude-plugin/plugin.json:7
  - Declares `"dependencies": ["ceh-coding-agent"]`
  
- ceh-orchestration — plugins/ceh-orchestration/.claude-plugin/plugin.json:7
  - Declares `"dependencies": ["ceh-coding-agent"]`
  
- ceh-python-library — plugins/ceh-python-library/.claude-plugin/plugin.json:7
  - Declares `"dependencies": ["ceh-testing"]`
  
- ceh-python-service — plugins/ceh-python-service/.claude-plugin/plugin.json:7
  - Declares `"dependencies": ["ceh-testing"]`
  
- ceh-web-frontend — plugins/ceh-web-frontend/.claude-plugin/plugin.json:7
  - Declares `"dependencies": ["ceh-testing"]`
  
- ceh-scenario-editorial — plugins/ceh-scenario-editorial/.claude-plugin/plugin.json:10-16
  - Declares `"dependencies": ["ceh-coding-agent", "ceh-git-workflow", "ceh-blog", "ceh-documentation", "ceh-seo"]`

- ceh-coding-agent — no match. No `dependencies` field.
- ceh-git-workflow — no match. No `dependencies` field.
- ceh-testing — no match. No `dependencies` field.
- ceh-blog — no match. No `dependencies` field.

## Not found / uncertain
- Nothing outstanding.

## Coverage
- plugins/ceh-ops/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-orchestration/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-python-library/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-python-service/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-web-frontend/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-scenario-editorial/.claude-plugin/plugin.json — 26 lines read
- plugins/ceh-coding-agent/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-git-workflow/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-testing/.claude-plugin/plugin.json — 10 lines read
- plugins/ceh-blog/.claude-plugin/plugin.json — 10 lines read
- Total: 106 lines across 10 files.
