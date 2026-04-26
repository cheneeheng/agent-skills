# Dependency Management

## Evaluation Criteria — Before Adding Any Package

1. **Necessity** — can this be done with < 20 lines of code in-house?
2. **Maintenance** — actively maintained? Last commit < 6 months?
3. **Popularity and trust** — download volume, stars, known maintainers?
4. **License** — compatible with the project? Avoid GPL for proprietary code.
5. **Size** — what is the bundle/install size impact?

If a dependency fails any of these, document why you're adding it anyway.

## Pinning Policy

| Environment | Pin level |
|-------------|-----------|
| Production dependencies | Exact version |
| Dev/test dependencies | Minor version (e.g. `^1.2.0`) |
| CI tool versions | Exact version |

Never use `*` or `latest` as a version specifier in any environment.

## Security Audits

Run before every release and as part of CI:

```bash
uv run pip-audit          # Python
bun audit                 # TypeScript/JavaScript
```

Address all high-severity findings before release. Document any accepted medium-severity exceptions in `docs/adr/DECISIONS.md`.

## Major Version Upgrades

Any dependency major version bump requires:
1. A dedicated PR (not bundled with feature work)
2. A brief ADR entry explaining the upgrade and breaking changes handled
3. Full test suite pass after upgrade
