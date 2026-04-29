# Linting and Type Checking

**ruff** is the single tool for linting and formatting. It replaces flake8, pylint, isort, and Black. Do not introduce those tools separately.

**mypy** handles type checking. It is separate from ruff.

## Required Checks Before Every PR

Use the `Bash` tool to run these checks:

```bash
uv run ruff check .           # Lint
uv run ruff format --check .  # Format check (does not modify)
uv run mypy .                 # Type check
```

Do not use `# type: ignore` without a comment explaining why. Do not downgrade `strict = true` to silence errors — fix the underlying type issue.
