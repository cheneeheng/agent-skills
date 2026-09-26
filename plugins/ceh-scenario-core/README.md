# ceh-scenario-core

CEH scenario bundle: coding in any repo, including a stack no ceh-* plugin covers — the coding-agent contract, git workflow, and test technique every other scenario builds on.

This plugin ships **no skills, agents, or hooks**. It is a scenario bundle: a manifest whose only
job is to name the set of `ceh-*` plugins that belong together for one situation, so you install
one thing instead of remembering a catalogue.

Every other scenario bundle depends on this one, so you only install it directly when no other
bundle fits — a Go or Rust project, a scripts repo, or anything else without a stack plugin.

## Install

```
/plugin install ceh-scenario-core@ceh-plugins --scope user
```

Its dependencies are resolved and installed automatically, and enabling this plugin enables all of
them at the same scope.

## What it pulls in

| Plugin |
|--------|
| `ceh-coding-agent` |
| `ceh-git-workflow` |
| `ceh-testing` |

## Notes

- Disabling any plugin above is refused while this bundle is enabled. Disable the bundle first.
- Experimental plugins (`ceh-fabled`, `ceh-advisor`), session-mechanics plugins
  (`ceh-summarize-chat`, `ceh-orchestration`, `ceh-lessons-learned`), and `ceh-ops` are
  deliberately **not** bundled — install them on their own when you want them.
