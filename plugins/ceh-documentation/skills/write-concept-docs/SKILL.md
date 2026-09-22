---
name: write-concept-docs
description: >-
  Load this skill when writing user-facing concept pages for a project in Markdown: the mental model
  a user needs (core objects, lifecycle, data flow, configuration precedence, error and retry
  model) and why it is built that way — the decision, the alternatives rejected, the trade-off,
  each traced to a source in the repo or its history. Trigger on "explain how this works in the
  docs", "document the design decisions for users", "write a concepts section", "why does it work
  this way — put it in the docs", or when ceh-documentation:write-project-docs delegates its
  concepts step. Not for a maintainer architecture doc with diagrams and a decision log (use
  ceh-architecture:document-architecture), a per-module codebase walkthrough (use
  ceh-coding-agent:explain-codebase), task steps (use user-operator-guide), or lookups (use
  write-api-reference).
compatibility: >-
  Reads the target project's files. Uses the git CLI on PATH to mine commit and merge messages for
  design rationale (`git log --grep`, `git log -S`); without git that source is skipped and more
  rationale lands in open items.
---

# Write Concept Docs

Concept pages are where an experienced user goes to learn **why** — why the timeout is per chunk,
why there is no sync client, why config files lose to env vars. They are also what keeps every
other page short: a term explained once here is linked from guides and reference instead of being
re-explained on each.

Work against `<root>` — the project path handed over by the caller, or the current working
directory. Write under `<root>/docs/concepts/`.

## Step 1 — Pick the concepts

A concept earns a page when **at least two guide or reference pages would otherwise have to explain
it**. Candidates, in the order to check:

1. The core objects a user creates or receives (the public classes and resources, and how they
   relate).
2. Lifecycle — what is created, when it is valid, what cleans it up.
3. Data flow — what happens between the user's call and the result.
4. Configuration precedence — where settings come from and which source wins.
5. The error and retry model — what fails, what retries, what the user must handle.
6. The security and trust model, when there are credentials or untrusted input.

Three to seven concepts is typical. More than ten means some are reference entries in disguise.

## Step 2 — Find the rationale

Collect the "why" before writing, ordered by how much to trust each source:

| Source | How |
|--------|-----|
| Design records | ADRs (`docs/adr/`, `docs/decisions/`), `ARCHITECTURE.md` Key Decisions, decision logs |
| Merge and commit bodies | `git -C <root> log --grep='<term>' --format='%h %s%n%b'`; `git -C <root> log -S'<symbol>' --reverse` for the commit that introduced a behavior |
| Code comments | Comments next to the behavior, especially `NOTE`, `WHY`, and "we do X because" prose |
| Changelog | `CHANGELOG.md` entries that changed the behavior, and the breaking-change notes |
| The code itself | A constraint the code makes visible (a lock, a bounded queue, a version check) — label it as inferred |

**Never invent a reason.** A plausible-sounding rationale that is wrong is worse than none: an
expert will act on it. When no source states why, write what the behavior *is* and its
consequence, and put `[VERIFY: why <behavior>]` in the "Why" section so the owner can fill it.

## Step 3 — Write each page

````markdown
# CO-03 — Streaming

[← Concepts](index.md)

<One or two sentences: what this concept is and when a user runs into it.>

## The model

<How it works, in the user's terms. A Mermaid diagram when there is structure or a sequence.>

```mermaid
sequenceDiagram
    Client->>Server: request
    Server-->>Client: chunk (timeout resets)
```

## Terms

- **Chunk** — <definition, linking its reference entry>

## How it behaves

<Defaults, edge cases, limits — each linking the reference entry that holds the exact values.>

## Why it works this way

<The decision, the alternative that was rejected and why, the trade-off accepted.>
Source: <link to the ADR, commit, or changelog entry>.

## What this means for you

- <Practical consequence, linking the guide that handles it.>

---

[← CO-02 Sessions](CO-02-sessions.md) · [Concepts](index.md) · [CO-04 Errors and retries →](CO-04-errors.md)
````

- **One concept per page, two screens at most.** Longer means it is two concepts.
- **Explain, do not instruct.** No numbered procedures — a task belongs in a guide, and the page
  links to it.
- **Exact values live in the reference.** Say "the timeout resets per chunk" here, and link to the
  reference for the default.
- **Every "Why" names its source** or carries a `[VERIFY: …]`.

## Step 4 — Layout and furniture

```
docs/concepts/
├── index.md             # hub: every page in reading order, one line each — "read this when…"
├── CO-01-<name>.md      # foundational first; later pages may assume earlier ones
└── CO-02-<name>.md
```

File naming follows the scheme canonical in `ceh-documentation:user-operator-guide` (Phase 3):
`CO-<NN>-<kebab-name>.md`, two digits, contiguous from `01`, the number carrying reading order.
Inserting or removing a page renumbers the rest and fixes every link to a renamed file in the same
pass. A single concept is not a folder: write it as `docs/concepts.md` instead.

Every page has the breadcrumb `[← Concepts](index.md)` under its H1 and a prev/next footer in `CO`
order; the first page drops prev, the last drops next. The H1 repeats the ID (`# CO-03 — Streaming`).
Blank lines surround every list, table, and fence.

## Self-review

- [ ] Each concept is needed by at least two other pages.
- [ ] Every "Why it works this way" section cites a source, or carries `[VERIFY: …]`.
- [ ] No rationale reads as fact without a source; inferred reasons say "inferred from the code".
- [ ] No procedures; exact values linked to the reference, not restated.
- [ ] Files numbered contiguously in reading order; footers and breadcrumbs resolve.

## Output

Report pages written, the concept list in reading order with each page's source for its "Why", and
**Open items** — every `[VERIFY: …]` with its file.
