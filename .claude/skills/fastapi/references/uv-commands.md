# uv Commands Reference

Quick reference for uv package manager commands in FastAPI projects.

## Project Setup

```bash
# Initialize new project
uv init myproject
cd myproject

# Add dependencies
uv add fastapi uvicorn[standard]
uv add pydantic-settings

# Add dev dependencies
uv add --dev pytest pytest-asyncio httpx ruff
```

## Dependency Management

```bash
# Install all dependencies from pyproject.toml
uv sync

# Install including dev dependencies
uv sync --all-extras

# Update all dependencies
uv sync --upgrade

# Update specific package
uv add fastapi --upgrade

# Remove dependency
uv remove package-name

# Show dependency tree
uv tree
```

## Running Commands

```bash
# Run application
uv run uvicorn app.main:app --reload

# Run with specific host/port
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app

# Run linter
uv run ruff check .

# Run formatter
uv run ruff format .

# Run any script
uv run python scripts/seed.py
```

## Lock File

```bash
# Generate/update lock file
uv lock

# Install from lock file (CI/production)
uv sync --frozen
```

## Virtual Environment

```bash
# uv automatically manages .venv
# To activate manually (optional):
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

## Python Version

```bash
# Set Python version (creates .python-version)
uv python pin 3.11

# Install specific Python version
uv python install 3.11
```
