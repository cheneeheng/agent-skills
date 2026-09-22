---
name: write-api-reference
description: >-
  Load this skill when writing or completing a project's user-facing reference documentation in
  Markdown — every public function, class, HTTP endpoint, CLI command and flag, configuration key,
  environment variable, and error — so an experienced user can look up any item, see when it was
  added, and follow a link to why it behaves as it does. Trigger on "write the API reference",
  "document every endpoint", "document all the CLI flags", "reference docs for this library",
  "document the config options", or when ceh-documentation:write-project-docs delegates its
  reference step. Counts the public surface first and reports coverage against it. Not for guides
  or tutorials (use user-operator-guide), explanations of design (use write-concept-docs), or the
  README (use update-readme).
compatibility: >-
  Reads source files of the target project. Uses the git CLI on PATH for "Added in" markers
  (`git tag`, `git diff <tag>..<tag>`); without git or tags the markers are omitted and everything
  else still runs.
---

# Write API Reference

The reference is the **only exhaustive page type** in a docs set. Every other page is allowed to be
selective because this one is not: a guide shows the three options a task needs and links here for
the other twenty. A reference entry that is missing sends the reader to the source; a reference
entry that teaches crowds out the lookup.

Work against `<root>` — the project path handed over by the caller, or the current working
directory. Write under `<root>/docs/reference/`.

## Step 1 — Is a generator already wired up?

Check for `mkdocstrings` (`::: ` directives, `plugins:` in `mkdocs.yml`), Sphinx `autodoc`
(`conf.py` extensions), TypeDoc (`typedoc.json`), or a committed or served OpenAPI spec.

- **Configured:** do not hand-write signatures a generator already renders — they drift. Write the
  reference index and one stub page per module holding the generator directive, and spend the
  effort on the docstrings the generator will render: list public items with a missing or one-word
  docstring as open items.
- **Not configured:** hand-write the Markdown below, and name the fitting generator in the report
  so the reference can later be kept in sync by the build instead of by hand.

## Step 2 — Count the public surface

Enumerate before writing. The surface is **what a user can reach without importing a private
path**.

| Project kind | The surface is |
|--------------|----------------|
| Python library | Names in `__all__`, else the non-underscore names re-exported from the package `__init__.py`; the classes' public methods and attributes |
| TypeScript / JS library | The `exports` / `main` / `types` entries in `package.json` and everything their index files re-export |
| HTTP API | Every route in the router files or the OpenAPI spec: method, path, auth, request, response, status codes |
| CLI | Every command, subcommand, flag, and positional from the argparse / click / typer / commander definitions — cross-check against `--help` output when the CLI runs |
| Every kind | Configuration: env vars read (`os.environ`, `getenv`, `process.env`, settings classes), config file keys, their defaults. Errors: exception classes and error codes a user can receive |

Record the total per kind. That count is the coverage target; the report states `N of M documented`.

## Step 3 — Lay out the pages

```
docs/reference/
├── index.md            # every page, one line each: what it covers
├── <module>.md         # one page per public module / resource / command group
├── cli.md              # when there is a CLI
├── configuration.md    # every env var and config key
└── errors.md           # every exception / error code
```

Reference pages are **named after the code**, not by the `<PREFIX>-<NN>` reading-order scheme the
guide pages use: nobody reads a reference in order, they arrive by name, and a filename that
mirrors the module is the one they guess. Each page gets a breadcrumb under its H1 —
`[← Reference](index.md)` — and no prev/next footer.

Within a page, group by kind (classes, then functions, then constants; or resources, then
endpoints) and sort **alphabetically inside each group**, so a lookup never depends on knowing the
source order.

## Step 4 — Write each entry

````markdown
### `Client.stream(prompt, *, model=None, timeout=60.0)`

Stream a completion token by token. *Added in v2.3.*

```python
def stream(self, prompt: str, *, model: str | None = None, timeout: float = 60.0) -> Iterator[Chunk]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | `str` | required | The input text. |
| `model` | `str \| None` | `None` | Model id; `None` uses the client default. |
| `timeout` | `float` | `60.0` | Seconds before `TimeoutError`, measured per chunk, not per call. |

**Returns** `Iterator[Chunk]` — yields as tokens arrive.
**Raises** [`RateLimitError`](errors.md#ratelimiterror) when the quota is exhausted.
**Why per-chunk timeout:** see [Streaming](../concepts/CO-03-streaming.md#why-it-works-this-way).
````

- **Signature, types, and defaults come from the code**, copied, never retyped from memory.
- **The description comes from the docstring.** Where there is none, describe only behavior the
  code makes plain; otherwise write `[VERIFY: purpose of X]`.
- **Show an example only when usage is not obvious from the signature** — the guides carry the
  worked usage.
- **Surprising behavior gets a "Why" link** to the concept page that explains it. The reference
  states *what*; the concept states *why*. Never inline the rationale here.
- **Deprecated items** say so on the first line, name the replacement, and the version it goes away.
- HTTP endpoints swap the signature for method + path + auth, and the parameter table for request
  fields, response fields, and status codes.
- `errors.md` entries: when it is raised, what the user did to cause it, how to fix it. The guide
  troubleshooting page links here by error name.

## Step 5 — "Added in" markers

Experienced users open the reference to find what is new. Mark items **added in the last three
releases**; older items carry no marker, since "Added in v0.4" helps nobody.

```bash
git -C <root> tag --sort=-creatordate | head -4          # newest tags
git -C <root> diff <older-tag>..<newer-tag> -- <public source paths>
```

A public name that first appears in a range's diff is *Added in `<newer-tag>`*. When
`CHANGELOG.md` names the addition, prefer its version. With no tags, omit the markers.

## Self-review

- [ ] Coverage count done per kind; every counted item has an entry or an open item.
- [ ] No signature, type, or default was retyped; each was copied from source.
- [ ] Entries sorted alphabetically within kind groups.
- [ ] No rationale inlined — it lives behind a "Why" link.
- [ ] Every error a user can hit has an `errors.md` entry.
- [ ] Every relative link and `#anchor` resolves.

## Output

Report pages written, the coverage line `N of M public items documented` per kind, the generator
recommendation when none is configured, and **Open items**: every `[VERIFY: …]` and every
undocumented surface item.
