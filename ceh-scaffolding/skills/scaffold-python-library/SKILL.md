---
name: scaffold-python-library
description: Load this skill when starting or scaffolding a new distributable Python library: creating the src/ layout, build metadata, type marker, tests, and .gitignore. Trigger when the user says "start/scaffold a Python library", "new Python package/SDK", or sets up a publishable package. For a web service use scaffold-python-service.
---

# Scaffold a Python Library

Use a `src/` layout so tests run against the installed package, not the working tree.

```
your-library/
├── src/
│   └── your_library/
│       ├── __init__.py        # defines the public API (__all__)
│       └── py.typed           # ship type information (PEP 561)
├── tests/
│   ├── unit/
│   └── api/                   # exercise the public API as a consumer
├── pyproject.toml
├── README.md
└── .gitignore
```

## Initial Config

- `pyproject.toml` with an explicit build backend (hatchling), uv, ruff, mypy, pytest config —
  see `ceh-python-library:packaging` and `ceh-python-library:python-library-environment`.
- Keep `dependencies = []` minimal; no web-service deps. Define `__all__` in `__init__.py` from the start.

## .gitignore

```
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
.DS_Store
```
