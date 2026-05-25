---
name: "gitignore"
description: "Load this skill when editing or creating a .gitignore file: verifying the required entries are present (.venv/, .env, __pycache__/, node_modules/, dist/, etc.). Auto-load whenever a .gitignore file is being created or modified."
---

# .gitignore Requirements

Must include:
```
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/
.ruff_cache/
node_modules/
.svelte-kit/
dist/
build/
*.db
.DS_Store
```
