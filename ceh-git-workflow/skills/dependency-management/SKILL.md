---
name: "dependency-management"
description: >
  Load this skill when adding, removing, or upgrading a dependency: evaluating whether a package
  is appropriate, deciding on pinning strategy, handling a major version upgrade, or running a
  security audit. Auto-load whenever a new package is being added with uv add or bun add, a
  dependency version is being changed, or a vulnerability is found in an existing package.
---

# Dependency Management

## Evaluation Criteria — Before Adding Any Package

1. **Necessity** — can this be done with < 20 lines of code in-house?
2. **Maintenance** — actively maintained? Last commit < 6 months?
3. **Popularity and trust** — download volume, stars, known maintainers?
4. **License** — compatible? Avoid GPL for proprietary code.
5. **Size** — bundle/install size impact?

If a dependency fails any of these, document why you're adding it anyway.

## Pinning Policy

| Environment | Pin level |
|-------------|-----------|
| Production dependencies | Exact version |
| Dev/test dependencies | Minor version (`^1.2.0`) |
| CI tool versions | Exact version |

Never use `*` or `latest`.

## Security Audits

Run before every release and in CI:
```bash
uv run pip-audit    # Python
bun audit           # TypeScript
```

Address all high-severity findings before release. Document accepted medium-severity exceptions in `docs/adr/DECISIONS.md`.

## Major Version Upgrades

Require:
1. A dedicated PR (not bundled with feature work)
2. A brief ADR entry explaining the upgrade and breaking changes handled
3. Full test suite pass after upgrade
