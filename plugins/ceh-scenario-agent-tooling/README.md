# ceh-scenario-agent-tooling

CEH scenario bundle: building Claude Code skills and agentic workflows — turning a repetitive task into a runnable skill, then evaluating it until a readiness gate passes.

This plugin ships **no skills, agents, or hooks**. It is a scenario bundle: a manifest whose only
job is to name the set of `ceh-*` plugins that belong together for one situation, so you install
one thing instead of remembering a catalogue.

## Install

```
/plugin install ceh-scenario-agent-tooling@ceh-plugins --scope user
```

Its dependencies are resolved and installed automatically, and enabling this plugin enables all of
them at the same scope.

## What it pulls in

| Plugin |
|--------|
| `ceh-scenario-core` |
| `ceh-workflow-builder` |
| `ceh-evaluation` |

## Notes

- Disabling any plugin above is refused while this bundle is enabled. Disable the bundle first.
- Experimental plugins (`ceh-fabled`, `ceh-advisor`), session-mechanics plugins
  (`ceh-summarize-chat`, `ceh-orchestration`, `ceh-lessons-learned`), and `ceh-ops` are
  deliberately **not** bundled — install them on their own when you want them.
