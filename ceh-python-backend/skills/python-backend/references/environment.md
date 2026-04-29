# Environment

- Python: **3.12**
- Package manager: **uv** (not pip, not poetry)
- Virtual environment: `.venv/` (managed by uv — do not create manually)
- Project manifest: `pyproject.toml`
- Lockfile: `uv.lock` (authoritative — never edit manually)

Use the `Bash` tool to execute all commands in this table.

| Action | Command |
|--------|---------|
| Install all dependencies | `uv sync` |
| Add a production dependency | `uv add <package>` |
| Add a dev dependency | `uv add --dev <package>` |
| Run any command | `uv run <command>` |
| Start development server | `uv run uvicorn app.main:app --reload` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |

**Never edit `uv.lock` manually. Never commit `.env`.**

## pyproject.toml Configuration

```toml
[project]
name = "your-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic-settings",
    "asyncpg",
    "alembic",
    "structlog",
]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "N",   # pep8-naming
    "B",   # flake8-bugbear
]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.mypy]
strict = true
python_version = "3.12"
ignore_missing_imports = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
```
