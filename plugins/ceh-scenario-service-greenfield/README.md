# ceh-scenario-service-greenfield

CEH scenario bundle: starting a Python backend service from nothing — everything in the -iterate bundle plus planning and scaffolding.

This plugin ships **no skills, agents, or hooks**. It is a scenario bundle: a manifest whose only
job is to name the set of `ceh-*` plugins that belong together for one situation, so you install
one thing instead of remembering a catalogue.

## Install

```
/plugin install ceh-scenario-service-greenfield@ceh-plugins --scope user
```

Its dependencies are resolved and installed automatically, and enabling this plugin enables all of
them at the same scope.

## What it pulls in

| Plugin |
|--------|
| `ceh-scenario-service-iterate` |
| `ceh-scaffolding` |
| `ceh-business-plan` |

## Notes

- Disabling any plugin above is refused while this bundle is enabled. Disable the bundle first.
- Experimental plugins (`ceh-fabled`, `ceh-advisor`), session-mechanics plugins
  (`ceh-summarize-chat`, `ceh-orchestration`, `ceh-lessons-learned`), and `ceh-ops` are
  deliberately **not** bundled — install them on their own when you want them.
