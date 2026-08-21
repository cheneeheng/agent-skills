# ceh-seo

Claude Code plugin for discoverability — SEO and GEO (generative engine optimization) standards
for anything exposed to the internet: public web pages, repo READMEs, package listings, and
landing copy.

## Scope

Discoverability is one activity applied to many surfaces. The two skills split on surface
mechanics, which is also where their trigger moments and file types are disjoint:

| Skill | Surface | Moment |
|-------|---------|--------|
| `web-discoverability` | HTML pages and routes | Shipping or creating a public web page — meta/OG/canonical, structured data, sitemap/robots, `llms.txt`, rendering strategy |
| `text-discoverability` | Public-facing text | Writing the README first screen, package description/keywords, GitHub topics, marketplace listings, landing copy |

Both carry a GEO layer: content structured so AI engines can extract and cite it — answer-first
sections, standalone quotable facts, question-shaped headings.

## Boundaries

- README **accuracy** after a code change belongs to `ceh-documentation:update-readme`; this
  plugin owns README **findability**.
- Writing the content itself (blog posts, docs) belongs to `ceh-blog` and `ceh-documentation`;
  this plugin governs how that content is found and cited.
- Accessibility always wins conflicts with SEO (see `ceh-web-frontend:accessibility`).

## Skills

| Skill | Description |
|-------|-------------|
| `web-discoverability` | Per-page head checklist, site-level surfaces (sitemap, robots, llms.txt), JSON-LD structured data, SSR/prerender requirements, GEO citation rules |
| `text-discoverability` | The excerpt rule, the canonical one-liner, per-surface checklist (GitHub/PyPI/npm/marketplaces), GEO writing rules, anti-patterns |
