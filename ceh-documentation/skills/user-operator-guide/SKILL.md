---
name: user-operator-guide
description: Load this skill when writing or revising end-user or operator-facing documentation — user guides, user manuals, getting-started guides, how-to manuals, operator runbooks, installation/configuration guides, administration manuals, and troubleshooting references. Trigger when the user says "write a user guide", "write a user manual", "operator guide", "admin manual", "ops runbook", "getting-started guide", "installation guide", "document how to use this", "document how to operate this", or asks to produce end-user or operations documentation. Not for API reference docs generated from code, blog posts (use ceh-blog), or README files (use update-readme).
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
├── index.md            # overview + table of contents linking every page
├── getting-started.md
├── how-to/
│   ├── reset-password.md
│   └── export-data.md
├── operations/         # operator content, its own subtree, never interleaved
│   ├── install.md
│   ├── configure.md
│   └── runbook-<failure>.md
└── troubleshooting.md
```

If the target docs system (Docusaurus, MkDocs, mdBook) has its own naming/nav/frontmatter conventions, follow them within `docs/guide/`.

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

## Phase 4 — Write each procedure

```markdown
### <Goal-stated task, e.g. "Rotate the API signing key">

**When:** <triggering condition — for runbooks, the alert/symptom>
**Prerequisites:** <access, tools, preconditions>
**Time / impact:** <duration; for ops, whether it causes downtime>

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
```

Step standards:
- One action per step; if a step has an "and", consider splitting.
- Warnings go **before** the dangerous step: `> **Warning:** this drops the table.`
- Bold UI labels exactly as shown: click **Advanced settings**.
- Fence every command and path; never leave a command inline where whitespace is ambiguous.
- For destructive/irreversible ops, state blast radius and recovery in the same block.
- Cross-reference, don't repeat: link to the canonical procedure instead of copy-pasting it.

## Phase 5 — Self-review

- [ ] Every command, flag, path, env var, UI label comes from a real source — none invented; unverifiable items marked `[VERIFY: …]`.
- [ ] A reader with only the stated prerequisites can complete each task end to end.
- [ ] Each procedure ends with a verifiable success check.
- [ ] Prerequisites and warnings precede the steps that need them.
- [ ] User and operator content are not interleaved.
- [ ] Numbered = ordered; bullets = unordered.
- [ ] Destructive ops state blast radius and recovery.
- [ ] Spine is tasks, not a feature dump.
- [ ] Terminology is consistent throughout.

## Output

All files live under `docs/guide/` — one `index.md` for a focused guide, or a cross-linked tree rooted there with `index.md` as the entry point (Phase 3). Open with a one-line summary: what you produced, the audience, and the file layout if multi-file. List anything assumed or unverified under a final **Open items** heading — never bury invented detail in confident prose.
