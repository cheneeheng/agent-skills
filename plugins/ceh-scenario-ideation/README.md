# ceh-scenario-ideation

CEH scenario bundle: shaping an idea before a stack is chosen — brainstorming the product, testing it for product-market fit, planning the build, and sketching the architecture.

This plugin ships **no skills, agents, or hooks**. It is a scenario bundle: a manifest whose only
job is to name the set of `ceh-*` plugins that belong together for one situation, so you install
one thing instead of remembering a catalogue.

## Install

```
/plugin install ceh-scenario-ideation@ceh-plugins --scope user
```

Its dependencies are resolved and installed automatically, and enabling this plugin enables all of
them at the same scope.

## What it pulls in

| Plugin |
|--------|
| `ceh-scenario-core` |
| `ceh-business-plan` |
| `ceh-plan-build-review` |
| `ceh-architecture` |

## Notes

- Disabling any plugin above is refused while this bundle is enabled. Disable the bundle first.
- Experimental plugins (`ceh-fabled`, `ceh-advisor`), session-mechanics plugins
  (`ceh-summarize-chat`, `ceh-orchestration`, `ceh-lessons-learned`), and `ceh-ops` are
  deliberately **not** bundled — install them on their own when you want them.
