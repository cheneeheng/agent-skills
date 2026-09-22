# ceh-documentation

Claude Code plugin for writing end-user and operator-facing documentation — task-oriented guides that let a reader achieve a goal without already knowing the system.

## Skills

| Skill | Description |
|-------|-------------|
| `write-guides-and-runbooks` | Write or revise user guides (`docs/guide/`) and operator runbooks (`docs/operations/`) — one section per audience, the right document type, task-oriented verifiable procedures |
| `update-readme` | Keep `README.md` accurate after significant changes (new features, CLI changes, config changes) |
| `write-project-docs` | Write a full docs set under `docs/` for the current workspace or a given project path — index, why, quickstart, guides, concepts, reference, examples, migration — one job per page; sequences the three skills below and itself |
| `write-api-reference` | The exhaustive layer: every public item, counted against the surface, alphabetical within kind, "Added in" markers for the last three releases, rationale behind "Why" links |
| `write-concept-docs` | The "why" layer: mental model per concept, design rationale sourced from ADRs, commits, and the changelog, never invented |

Invoke manually:

```
/ceh-documentation:write-guides-and-runbooks
```

**write-guides-and-runbooks** loads automatically when you say:
- `"write a user guide"` / `"write a user manual"`
- `"write an operator guide"` / `"write an ops runbook"`
- `"getting-started guide"` / `"installation guide"`
- `"document how to use this"` / `"document how to operate this"`
- `"admin manual"` / `"configuration guide"`

**write-project-docs** loads automatically when you say:
- `"document this project"` / `"write the docs for this library"`
- `"create documentation for <path>"` / `"our docs are out of date, redo them"`

Pass a path to document another project: `/ceh-documentation:write-project-docs ../my-lib`

**update-readme** loads automatically when you say:
- `"update the readme"` / `"refresh the docs"`
- `"document this feature"` / `"I just shipped X — update docs"`

> Changelog maintenance moved to `ceh-git-workflow:update-changelog` — every input that skill reads
> is git (`git describe --tags`, `git log`, `git tag`, `git remote`), so it fires on a git moment,
> not a documentation one. `check-semver.py` moved with it.

## What It Produces

Markdown under `docs/` in one fixed format, whichever skill writes the page. The format lives in
`references/docs-standard.md`, shipped word-for-word in each of the four writing skills
(`update-readme` excepted) so each works when loaded alone:

- **Layout** — `docs/index.md` front page, site-level `why.md` / `migration.md`, and the sections
  `guide/` (the user's tasks), `operations/` (the operator's runbook), `concepts/`, `reference/`,
  `examples/`, each with an `index.md` hub
- **One mode per page** — tutorial, how-to, concept, reference, or example; a page needing two is two pages
- **File naming** — numbered folders use `<PREFIX>-<NN>-<name>.md` with fixed prefixes (`HT`, `OP`,
  `TS`, `CO`, `EX`), contiguous from `01`; reference pages are named after the code, never numbered
- **Page anatomy** — one H1 (repeating the ID on numbered pages), a breadcrumb to the nearest hub, a
  one-to-two-sentence summary, and a prev · hub · next footer on numbered pages
- **Markdown that survives a renderer** — blank lines around every block, a language tag on every
  fence, Mermaid for diagrams, relative `.md` links with verified anchors
- **Fixed markers** — `[VERIFY: …]`, `*Added in vX.Y.*`, the deprecation, warning, and note blockquotes
- **One report shape** — a page table plus **Open items** listing every unverified claim

### File naming — two rules worth knowing

**Numbers stay contiguous.** The number carries reading order, so there are never gaps. Appending a
page at the end takes the next number and renumbers nothing; inserting or deleting one renumbers
the rest of that folder, and every link to a renamed file is updated in the same pass. The
alternative — append-only numbers with gaps — was rejected because it turns the number into an
arbitrary ID, at which point numbering earns nothing. Revisit only if these filenames become
externally referenced (published URLs, tickets, support macros); stable IDs then beat reading order.

**The scheme beats the docs system.** Docusaurus, MkDocs and mdBook derive nav order from filenames,
which would otherwise compete with the prefix. It does not get to: nav order and page metadata are
expressed in frontmatter or nav config, never by renaming a file out of the scheme.

## Document Types Supported

| Type | Reader's goal |
|------|---------------|
| Getting Started | Go from zero to first success |
| How-To Guide | Accomplish one specific task |
| User Manual | Reference for the whole product |
| Operator Runbook | Operate and recover a system |
| Installation / Config Guide | Stand the system up correctly |
| Troubleshooting Reference | Diagnose and fix a known failure |
