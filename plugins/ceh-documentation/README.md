# ceh-documentation

Claude Code plugin for writing end-user and operator-facing documentation — task-oriented guides that let a reader achieve a goal without already knowing the system.

## Skills

| Skill | Description |
|-------|-------------|
| `user-operator-guide` | Write or revise user guides and operator runbooks — distinguishes the two audiences, picks the right document type, and enforces task-oriented, verifiable procedures |
| `update-readme` | Keep `README.md` accurate after significant changes (new features, CLI changes, config changes) |

Invoke manually:

```
/ceh-documentation:user-operator-guide
```

**user-operator-guide** loads automatically when you say:
- `"write a user guide"` / `"write a user manual"`
- `"write an operator guide"` / `"write an ops runbook"`
- `"getting-started guide"` / `"installation guide"`
- `"document how to use this"` / `"document how to operate this"`
- `"admin manual"` / `"configuration guide"`

**update-readme** loads automatically when you say:
- `"update the readme"` / `"refresh the docs"`
- `"document this feature"` / `"I just shipped X — update docs"`

> Changelog maintenance moved to `ceh-git-workflow:update-changelog` — every input that skill reads
> is git (`git describe --tags`, `git log`, `git tag`, `git remote`), so it fires on a git moment,
> not a documentation one. `check-semver.py` moved with it.

## What It Produces

Markdown written under `docs/guide/` — a single `index.md` for a focused guide, or a cross-linked tree rooted there with `index.md` as the entry point for a full manual or runbook:
- Audience-correct voice (friendly for users, terse and precise for operators)
- Task-oriented structure — organized by what the reader is trying to do, not by feature
- Numbered procedures where every step has a verifiable result
- Prerequisites and warnings before the steps that need them
- A fixed file-naming scheme — root-level pages keep plain names, subfolder pages are `<PREFIX>-<NN>-<name>.md` (`how-to/HT-01-reset-password.md`), numbered contiguously from `01` per subfolder
- Page furniture that survives a real renderer — an index breadcrumb and prev/next footer on every subfolder page, and Markdown that breaks lines where it looks like it does
- An **Open items** list of anything assumed or left unverified — never invented detail

### File naming — two rules worth knowing

**Numbers stay contiguous.** The number carries reading order, so there are never gaps. Appending a
guide at the end takes the next number and renumbers nothing; inserting or deleting one renumbers
the rest of that subfolder, and every link to a renamed file is updated in the same pass. The
alternative — append-only numbers with gaps — was rejected because it turns the number into an
arbitrary ID, at which point numbering earns nothing. Revisit only if these filenames become
externally referenced (published URLs, tickets, support macros); stable IDs then beat reading order.

**The scheme beats the docs system.** Docusaurus, MkDocs and mdBook derive nav order from filenames,
which would otherwise compete with the prefix. It does not get to: nav order and page metadata are
expressed in frontmatter (`sidebar_position`, `title`) or nav config, never by renaming a file out
of the scheme.

## Document Types Supported

| Type | Reader's goal |
|------|---------------|
| Getting Started | Go from zero to first success |
| How-To Guide | Accomplish one specific task |
| User Manual | Reference for the whole product |
| Operator Runbook | Operate and recover a system |
| Installation / Config Guide | Stand the system up correctly |
| Troubleshooting Reference | Diagnose and fix a known failure |
