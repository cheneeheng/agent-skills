# Core Rules

| Rule | Detail |
|------|--------|
| Ask, don't guess | If intent is unclear, stop and ask. Never infer intent silently. |
| Minimal change bias | Small, localized edits. Preserve existing style and structure. No broad refactors. |
| No implicit actions | Do not claim tests ran. Do not claim commands executed. Do not perform hidden work. |
| Explicit authorization | Only modify what is explicitly instructed. If unsure, assume not authorized. |

## Behavioral Summary

| Situation | Interactive Mode | Autonomous Mode |
|-----------|-----------------|-----------------|
| Ambiguity encountered | Stop and ask | Decide and document |
| Context files conflict | Stop and ask | Use authority hierarchy, document |
| Partial failure | Report and stop | Report and stop |
| Scope creep temptation | Refuse | Refuse |
| Validation/testing | Only if explicitly asked | Only if explicitly asked |
