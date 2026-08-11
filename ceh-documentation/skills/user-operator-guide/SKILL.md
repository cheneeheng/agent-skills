---
name: user-operator-guide
description: >-
  Load this skill when writing or revising end-user or operator-facing documentation — user guides,
  user manuals, getting-started guides, how-to manuals, operator runbooks,
  installation/configuration guides, administration manuals, and troubleshooting references. Trigger
  when the user says "write a user guide", "write a user manual", "operator guide", "admin manual",
  "ops runbook", "getting-started guide", "installation guide", "document how to use this",
  "document how to operate this", or asks to produce end-user or operations documentation. Not for
  API reference docs generated from code, blog posts (use ceh-blog), or README files (use
  update-readme).
---

# User & Operator Guide

Write task-oriented docs that let a reader reach a goal without already knowing the system. Two audiences — never blur them. When a request covers both (common for internal tools), keep them in separate sections/files; never interleave end-user steps with privileged operator commands.

| | **User guide** | **Operator guide / runbook** |
|---|---|---|
| Reader | Uses the product to do their own work | Installs, configures, runs, monitors, recovers the system |
| Asks | "How do I do *my* task?" | "How do I keep this healthy and fix it when it breaks?" |
| Assumes | No internals; UI/CLI surface only | Shell access, infra context, privileged credentials |
| Worst day | "I can't figure out how to do X" | "It's down at 2am and I'm on call" |
| Voice | Friendly, plain | Terse, precise, copy-pasteable |

## Non-negotiable rules

- **Task-oriented, not feature-oriented.** Organize by what the reader wants to *do* ("Reset a password"), not by what the software *has* ("Settings Panel"). Features go in a reference appendix, not the spine.
- **One procedure = one numbered list.** Numbered = ordered sequence; bullets = unordered options only.
- **Every step has a verifiable result.** "Click **Save**; the banner turns green." A step the reader can't confirm is broken.
- **Imperative, second person.** "Run the migration", not "The migration should be run."
- **Show the exact thing** — real command, bolded UI label, real path, real output. No `<placeholder>` without a concrete example beside it.
- **Prerequisites up front**, never buried in step 4.
- **Write for the reader's worst day** — front-load the answer, defer the theory.

## Phase 1 — Audience, scope, source of truth

Pin down before writing:

1. **Audience** — user, operator, or both? Sets voice, assumed knowledge, structure.
2. **Scope** — name the tasks in scope. Covering everything covers nothing.
3. **Source of truth** — code, CLI `--help`, config, existing draft. **Never invent commands, flags, env vars, or UI labels**; mark anything unverifiable `[VERIFY: …]` and surface it — don't guess. Fabricated docs are worse than missing ones; they break trust on first use.
4. **Prerequisites/environment** — supported OS/versions, access, dependencies.

## Phase 2 — Pick the document type

Most guides combine a getting-started front and a how-to body.

| Type | Reader's goal | Spine |
|------|---------------|-------|
| **Getting Started** | Zero to first success | Install → configure → run the smallest real task → "you're set up" |
| **How-To Guide** | One specific task | Goal → prerequisites → steps → verify → troubleshoot |
| **User Manual** | Reference for the whole product | Task-grouped chapters + feature reference + glossary |
| **Operator Runbook** | Operate/recover a system | Architecture → routine ops → incident procedures → escalation |
| **Install / Config Guide** | Stand the system up correctly | Requirements → install → configure → verify health → common failures |
| **Troubleshooting** | Diagnose a known failure | Symptom → cause → fix, as a lookup table or flat entries |

## Phase 3 — Structure

### Where files go

New docs always go under `docs/guide/`. When revising or extending docs that already live elsewhere, edit them in place — don't relocate or duplicate them into `docs/guide/`.

A focused single-topic guide is one file: `docs/guide/index.md`. Anything broader — many tasks, both audiences, or a docs-site target — becomes a cross-linked tree rooted at `docs/guide/`, with `index.md` as the overview and table of contents. Link between pages; never duplicate. The per-audience split below applies only when a guide serves both users and operators; for a single audience, drop the `operations/` subtree and lay sections out directly.

```
docs/guide/
├── index.md            # root level: overview + table of contents linking every page
├── getting-started.md
├── troubleshooting.md
├── how-to/             # HT
│   ├── HT-01-reset-password.md
│   └── HT-02-export-data.md
└── operations/         # OP — operator content, its own subtree, never interleaved
    ├── OP-01-install.md
    ├── OP-02-configure.md
    └── database/       # OP-DB — nested folder chains its parent prefix
        ├── OP-DB-01-backup.md
        └── OP-DB-02-restore.md
```

### How to name the files

Files sitting directly in `docs/guide/` keep plain kebab-case names — **no prefix, no number**. Every file inside a subfolder is `<PREFIX>-<NN>-<kebab-name>.md`:

- **Prefix** — a capitalized abbreviation of the subfolder name, as short as stays readable, minimum 2 characters: `how-to/` → `HT`, `operations/` → `OP`, `troubleshooting/` → `TS`. One prefix per subfolder, unique across the whole tree; if two subfolders abbreviate to the same letters, lengthen one of them (`onboarding/` → `ONB` next to `operations/` → `OP`).
- **Number** — two digits, starting at `01`, restarting at `01` inside each subfolder. `HT-01` and `OP-01` coexist; the prefix keeps them apart.
- **Reading order** — the number *is* the order the reader should follow, so it stays contiguous. Appending a guide at the end takes the next number and renumbers nothing. Inserting or removing one renumbers the rest of that subfolder — update every link to a renamed file in the same pass. Never leave a gap.
- **Nested subfolder** — chains its parent prefix and adds its own (`operations/database/` → `OP-DB-`), and starts its own `01` sequence.
- **At least two files per subfolder.** One file is not a folder: put it at the root level instead, unprefixed and unnumbered. The same applies in reverse — once a root-level topic grows to two or more files, move them into a subfolder and prefix/number them.

This naming scheme wins over any docs-system convention. If the target docs system (Docusaurus, MkDocs, mdBook) needs a particular nav order or page metadata, express it in frontmatter (`sidebar_position`, `title`) or the nav config — never by renaming a file out of the scheme.

### User guide skeleton

```
# <Product> User Guide
## Overview          — what it does, who it's for (2-3 sentences)
## Before you begin  — prerequisites, access, supported platforms
## Getting started   — shortest path to first success
## How-to: <task>    — one section per task, numbered steps + verify
## Troubleshooting   — symptom → fix table for common stumbles
## Reference         — features, settings, shortcuts (appendix)
## Glossary          — only if the domain has unfamiliar jargon
```

### Operator guide / runbook skeleton

```
# <System> Operator Guide
## System overview     — components, data flow, where things run (diagram if it helps)
## Prerequisites       — access, tools, credentials, network
## Installation        — steps + post-install health check
## Configuration       — each setting: name, purpose, default, valid range, effect
## Routine operations  — start/stop/restart, deploy, backup, scale, rotate secrets
## Monitoring          — what to watch, healthy ranges, where dashboards/logs live
## Incident procedures — per failure: detection → diagnosis → remediation → verification
## Rollback / recovery — safe revert and restore from backup
## Escalation          — who/what to page when the runbook runs out
```

## Phase 4 — Page furniture and markdown that renders

A human reads these pages in a Markdown renderer; nothing parses them. Two faults spoil that more than any other: a page with no way out, and line breaks that silently collapse.

### Every page carries navigation

Put a breadcrumb directly under the H1, and a prev/next/index footer at the bottom. The footer follows `NN` order **within the page's own subfolder** — each subfolder is a separate chain, never linked across.

```markdown
# HT-02 — Reset a password

[← Guide index](../index.md)

<body>

---

[← HT-01 Change your email](HT-01-change-email.md) · [Guide index](../index.md) · [HT-03 Export data →](HT-03-export-data.md)
```

- The H1 repeats the file's ID, so a printed or pasted page still says where it came from.
- The first page in a chain drops the prev link, the last drops the next. Never leave a dead link.
- Prev/next point at siblings in the same subfolder, so they need no path prefix; the breadcrumb climbs to the root `index.md` — `../index.md` from a subfolder, `../../index.md` from a nested one. Check each link resolves rather than copying the neighbour's footer.
- Root-level pages are unnumbered and belong to no chain: breadcrumb only, no prev/next.
- `index.md` gets no footer — it *is* the hub. It lists every page grouped by subfolder in `NN` order, each with a one-line "read this when…".
- Renumbering a subfolder (Phase 3) means fixing the affected footers in the same pass, not only the links in prose.

### Line-break rules

**A single newline is not a line break.** Two lines separated by one newline render as one paragraph — the most common way a finished guide arrives looking wrong.

| Want | Write |
|------|-------|
| A new paragraph | A blank line between the two lines |
| A hard break inside one paragraph | Two trailing spaces at the end of the first line |
| A stack of labelled fields | A bullet list — not stacked bold labels |

Prefer the blank line. Trailing spaces are invisible in review and formatters strip them, so use them only where a blank line would wrongly split a block.

Blank lines that carry the same weight:

- One blank line **before and after** every list, table, fenced code block, blockquote, and heading. A list or table glued to the paragraph above it renders as literal text in strict parsers.
- Inside a numbered step, indent a nested fence or paragraph by **3 spaces** so it stays in the item; any less and the list restarts at 1.
- One `#` H1 per page, then `##`/`###` — never skip a level.
- Don't hard-wrap paragraphs at a fixed column. Wrapping is the renderer's job, and hard wraps read badly on a narrow screen.
- Tables need the header separator row and leading/trailing `|`. A table past ~5 columns is a list in disguise.

## Phase 5 — Write each procedure

````markdown
### <Goal-stated task, e.g. "Rotate the API signing key">

- **When:** <triggering condition — for runbooks, the alert/symptom>
- **Prerequisites:** <access, tools, preconditions>
- **Time / impact:** <duration; for ops, whether it causes downtime>

1. <Action>. <Result the reader can confirm.>

2. <Action>.

   ```bash
   actual --command --here
   ```

   Expected output:

   ```
   the real output to compare against
   ```

**Verify:** <the single check that proves it worked>

**If it fails:** <1-2 likely failure modes + fix, or a link to troubleshooting>
````

Step standards:
- One action per step; if a step has an "and", consider splitting.
- Warnings go **before** the dangerous step: `> **Warning:** this drops the table.`
- Bold UI labels exactly as shown: click **Advanced settings**.
- Fence every command and path; never leave a command inline where whitespace is ambiguous.
- For destructive/irreversible ops, state blast radius and recovery in the same block.
- Cross-reference, don't repeat: link to the canonical procedure instead of copy-pasting it.

## Phase 6 — Self-review

- [ ] Every command, flag, path, env var, UI label comes from a real source — none invented; unverifiable items marked `[VERIFY: …]`.
- [ ] A reader with only the stated prerequisites can complete each task end to end.
- [ ] Each procedure ends with a verifiable success check.
- [ ] Prerequisites and warnings precede the steps that need them.
- [ ] User and operator content are not interleaved.
- [ ] Numbered = ordered; bullets = unordered.
- [ ] Destructive ops state blast radius and recovery.
- [ ] Spine is tasks, not a feature dump.
- [ ] Terminology is consistent throughout.
- [ ] Every subfolder file is `<PREFIX>-<NN>-<name>.md`; root-level files carry no prefix and no number.
- [ ] Each subfolder holds at least two files, numbered contiguously from `01`, and every link to a renamed file was updated.
- [ ] Every page has its breadcrumb and — inside a subfolder — a prev/next footer; no dead links, no link across two subfolders' chains; `index.md` lists every page.
- [ ] No two lines rely on a single newline for a break; blank lines surround every list, table, and code fence.

## Output

All files live under `docs/guide/` — one `index.md` for a focused guide, or a cross-linked tree rooted there with `index.md` as the entry point, root-level files unnumbered and subfolder files named `<PREFIX>-<NN>-<name>.md`, each page carrying its breadcrumb and prev/next footer (Phases 3-4). Open with a one-line summary: what you produced, the audience, and the file layout if multi-file. List anything assumed or unverified under a final **Open items** heading — never bury invented detail in confident prose.
