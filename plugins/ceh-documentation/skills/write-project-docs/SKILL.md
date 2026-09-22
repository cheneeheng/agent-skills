---
name: write-project-docs
description: >-
  Load this skill to write a complete documentation set for a project as Markdown under docs/ —
  front page, why-X page, quickstart, how-to guides, concepts with design rationale, a full API
  reference, examples, troubleshooting, and migration notes — for the current workspace or for a
  project path the user gives. Trigger on "document this project", "write the docs for this
  library", "create documentation for <path>", "write docs for our SDK/API/CLI", "build out the
  docs folder", or "our docs are missing or out of date, redo them". This skill surveys, plans the
  page set, and sequences it: the reference goes to write-api-reference, concept and
  design-rationale pages to write-concept-docs, guides to user-operator-guide. Not for one guide or
  runbook alone (use user-operator-guide), a README refresh (use update-readme), or a maintainer
  architecture doc (use ceh-architecture:document-architecture).
argument-hint: '[project-path]'
compatibility: >-
  Reads the target project's files and, when present, its git history through the git CLI on PATH
  (`git -C <root> log`, `git tag`). Without git or without history it still runs, but drops the
  "Added in" markers and commit-sourced design rationale. Writes Markdown only; it installs no docs
  framework and runs none of the project's code unless a sample needs checking.
---

# Write Project Docs

Produce a docs set that a newcomer can use in five minutes and an experienced user can mine for
every feature and the reason behind it. The balance does not come from trimming words. It comes
from **giving every page exactly one job**, so each page can go to its own extreme: the quickstart
as short as possible, the reference as complete as possible, the concepts as deep as needed.

This skill owns the target, the survey, the page plan, the front pages, and the final link pass.
Every other page type is delegated to the skill that owns it.

## Step 0 — Resolve the target

- **A path was given** (skill argument or in the request): that directory is `<root>`. Resolve it
  to an absolute path and confirm it exists and holds a project (a manifest such as
  `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, or a source tree). If it does not,
  stop and say so — never document the current workspace in its place.
- **No path given:** `<root>` is the current working directory.

Every read is from `<root>`; every git command is `git -C <root> …`. Every write goes under
`<root>/docs/`, plus one README link in Step 5. Nothing is written into the workspace the agent
happens to be running in when `<root>` is somewhere else.

## Step 1 — Survey

Read before planning. Record the answers in a survey table in the session; every later step reads
from it and the delegated skills receive it verbatim.

| Question | Where to look |
|----------|---------------|
| What kind of project? (library, CLI, HTTP API / SaaS, service, app) | Manifest, entry points, route files, `Dockerfile` |
| What is the public surface, roughly how big? | Package exports, routes, CLI definitions, env reads — `write-api-reference` does the exact count |
| How is it installed and run? | Manifest, README, `Makefile`, CI config, `.env.example` |
| What does a first working result look like? | README, `examples/`, the simplest test that exercises the public API |
| What are the core ideas a user must hold? | Public class and type names, repeated terms in docstrings and errors |
| Where does design rationale live? | ADRs, `ARCHITECTURE.md`, decision logs, PR/commit bodies, `CHANGELOG.md` |
| Release history? | `git -C <root> tag --sort=-creatordate`, `CHANGELOG.md` |
| What docs exist already, and is a docs framework configured? | `docs/`, `mkdocs.yml`, `conf.py`, `docusaurus.config.*`, `astro.config.*` |
| Known limitations and failure modes? | Raised errors, `TODO`/`NotImplementedError`, issue templates, README caveats |

## Step 2 — Plan the page set

Map the survey onto this layout. **Cut every page that has no real content** — no `migration.md`
without a breaking change in history, no `examples/` without a runnable example, no
`guide/operations/` for a library. An empty section costs the reader a click and trust.

```
docs/
├── index.md          # front page: what it is, one code sample, where to go next  (this skill)
├── why.md            # why X, X vs alternatives, when NOT to use it, limitations   (this skill)
├── guide/            # getting-started (the quickstart), how-to/, troubleshooting, operations/
│                     #                                           (user-operator-guide)
├── concepts/         # the mental model + why it is built this way   (write-concept-docs)
├── reference/        # every public item, exhaustively               (write-api-reference)
├── examples/         # complete runnable programs, EX-NN-<name>.md   (this skill)
└── migration.md      # per-major-version upgrade steps               (this skill)
```

Write the plan as a table — **Page | Mode | The one question it answers | Source** — and hold it in
the session. Modes are *tutorial*, *how-to*, *concept*, *reference*. A page that needs two modes is
two pages. A page whose question you cannot state in one line is not planned yet.

**Existing docs:** edit in place and fill gaps. Map each existing page to a mode, keep its path, and
add only the missing pages. Never relocate or duplicate existing pages into the layout above. When
a docs framework is configured, add every new page to its nav config (`nav:` in `mkdocs.yml`,
`sidebars.*`, `toctree`) in the same pass.

## Step 3 — Pipeline

Run in order. Reference comes first because every other page links into it; the front pages come
last because they link to everything.

| # | Pages | Delegate to | Gate before next step |
|---|-------|-------------|-----------------------|
| 1 | `docs/reference/` | Invoke the Skill tool with skill="ceh-documentation:write-api-reference" — pass `<root>` and the survey table | Every surface item counted in its coverage check has an entry, or is listed as an open item |
| 2 | `docs/concepts/` | Invoke the Skill tool with skill="ceh-documentation:write-concept-docs" — pass `<root>`, the survey table, the reference page list | Each concept page has a "Why it works this way" section with a cited source, or an open item |
| 3 | `docs/guide/` | Invoke the Skill tool with skill="ceh-documentation:user-operator-guide" — pass `<root>`, the audience, and the brief below | Getting-started reaches a working result; every how-to ends in a verify step |
| 4 | `docs/examples/`, `docs/migration.md` | this skill — see below | Each example runs or is marked `[VERIFY: …]` |
| 5 | `docs/why.md`, `docs/index.md` | this skill — see below | Index links every section; no page unreachable from it |
| 6 | Link pass | this skill — see below | Zero broken relative links |

**Brief for `user-operator-guide`:** its `docs/guide/` means `<root>/docs/guide/`, and its
`getting-started.md` *is* the site quickstart — the
shortest path from install to a first working result, no options, no configuration beyond the
minimum, each optional knob replaced by a link to its reference entry. How-to pages cover the tasks
from the survey, show the handful of options that task needs, and link to `docs/reference/` for the
rest. Troubleshooting entries are keyed by the literal error text a user will search for, each
linking to the error's reference entry. A term that needs explaining links to its concept page
instead of explaining it inline.

**Examples:** only programs that already exist in the repo (`examples/`, runnable snippets from
tests) or that you ran successfully. Each page: what it builds (one line), the full code, how to run
it, expected output, and the guide and reference pages it draws on. `EX-NN-<name>.md`, at least two
or fold the single one into a how-to.

**Migration:** one section per major version with a breaking change, newest first — what broke,
the before/after code, and the "why" link to its concept or decision. Link `CHANGELOG.md` for
everything smaller; never copy the changelog into the docs.

## Step 4 — Front pages

`docs/index.md` fits on one screen:

````markdown
# <Project>

<One sentence: what it is and who it is for.>

```<lang>
<the smallest real usage — 10 lines or fewer, copied from getting-started>
```

- **New here?** [Get started](guide/getting-started.md) — a working result in minutes.
- **Doing a specific task?** [Guides](guide/index.md)
- **Want to understand how it works and why?** [Concepts](concepts/index.md)
- **Looking up a function, flag, or setting?** [Reference](reference/index.md)
- **Choosing between tools?** [Why <Project>](why.md)
- **Upgrading?** [Migration](migration.md) · [Changelog](<link>)
````

`docs/why.md` is for someone deciding whether to adopt: the problem it solves, what it does
differently (link the concept page carrying each claim), a comparison with named alternatives only
where the repo or its docs make the comparison, **when not to use it**, and **Known limitations**
with the workaround where one exists. Claims come from the code and the survey, never from
marketing adjectives.

## Step 5 — Link pass and consistency

- Every page is reachable from `docs/index.md` in at most two clicks.
- Every relative link resolves to a file that exists, and every `#anchor` to a heading that exists.
- An idea is explained once, in its home mode, and linked everywhere else — collapse any second
  explanation into a link.
- One term per concept across every page; the reference name wins when two pages disagree.
- Code samples are copied from something that ran, or marked `[VERIFY: …]`.

Then invoke the Skill tool with skill="ceh-documentation:update-readme" to add a link to
`docs/index.md` near the top of `<root>/README.md`. The README stays the storefront; the docs are
the manual.

## Page budgets

| Page | Budget | Why |
|------|--------|-----|
| `index.md` | One screen | It routes; it does not teach |
| `guide/getting-started.md` | 5–7 steps, zero options | Every option is a place to stall |
| How-to page | One task, ≤ 2 screens | Longer means two tasks |
| Concept page | ≤ 2 screens | Longer means two concepts |
| Reference page | Unbounded, but one module/resource per page | Completeness is its job; findability comes from structure |

## Hard rules

- **Never invent.** Every command, flag, default, signature, and rationale comes from the code, its
  history, or a design record. Anything unverified is marked `[VERIFY: …]` in place and listed under
  **Open items** in the report.
- **Markdown only.** Do not install or configure a docs generator. If none is configured, name the
  fitting one for the stack in the report (MkDocs or Sphinx for Python, Starlight or Docusaurus for
  TypeScript, an OpenAPI renderer for HTTP APIs) — the Markdown written here is its input.
- **Stay inside `<root>/docs/`**, plus the one README link.
- **Do not commit.** The caller decides what lands.

## Report

Open with one line: pages written, pages updated, pages cut and why. Then the page plan table with
a Status column, the reference coverage count (`N of M public items documented`), and **Open items**
— every `[VERIFY: …]` with its file.
