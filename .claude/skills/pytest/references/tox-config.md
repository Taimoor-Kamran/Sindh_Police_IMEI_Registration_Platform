# UV Commands Reference

## Project Setup

```bash
# Create virtual environment
uv venv

# Install project dependencies
uv pip install -e '.[dev]'

# Install specific Python version
uv python install 3.12
```

## Testing Commands

| Task | Command |
|------|---------|
| Run all tests | `pytest` |
| Run specific test | `pytest tests/unit/test_example.py` |
| Run with coverage | `pytest --cov=src --cov-report=html` |
| Run specific marker | `pytest -m "not slow"` |
| Run by pattern | `pytest -k "test_name"` |
| Run in parallel | `pytest -n auto` |

## Linting & Formatting

| Task | Command |
|------|---------|
| Lint check | `ruff check src tests` |
| Format code | `ruff format src tests` |
| Fix lint issues | `ruff check --fix src tests` |
| Type check | `mypy src` |

## UV Commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install from uv.lock |
| `uv pip install package` | Install package |
| `uv pip install -e '.[dev]'` | Install editable with dev deps |
| `uv run command` | Run command in environment |
| `uv python install 3.12` | Install Python version |
| `uv venv` | Create virtual environment |

## Configuration

### pyproject.toml (dev dependencies)
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
```

### Pre-commit with UV
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0
    hooks:
      - id: mypy
```
