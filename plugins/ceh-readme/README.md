# ceh-readme

Claude Code plugin for keeping `README.md` accurate after a significant change. Cross-cutting: every
repo has a README, whatever it builds, so this plugin ships in `ceh-scenario-core`.

## Skills

| Skill | Description |
|-------|-------------|
| `update-readme` | Keep `README.md` accurate after significant changes (new features, CLI changes, config changes) |

Invoke manually:

```
/ceh-readme:update-readme
```

**update-readme** loads automatically when you say:
- `"update the readme"` / `"refresh the docs"`
- `"document this feature"` / `"I just shipped X — update docs"`

> Split out of `ceh-documentation`, whose other skills write a whole `docs/` set for a software
> project. `update-readme` needs none of that, and core should not install five docs-set skills to
> get one README skill.
