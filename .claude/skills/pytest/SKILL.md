---
name: pytest
description: Scaffold and manage pytest projects with uv integration. Use when users want to create new test projects, add test files, configure development environments with uv, run tests with coverage, or follow pytest best practices. Triggers on requests like "create a pytest project", "add tests", "set up uv", "run coverage", or any pytest/uv development task.
---

# Pytest with UV

Scaffold and manage pytest projects using uv for fast package management.

## Quick Start: New Project

```bash
python scripts/scaffold.py my-project --path /target/directory
```

Creates:
```
my-project/
├── pyproject.toml      # pytest + coverage + lint config
├── src/my_project/     # source code (src layout)
└── tests/
    ├── conftest.py     # shared fixtures
    ├── unit/
    └── integration/
```

## UV Commands

| Task | Command |
|------|---------|
| Install dependencies | `uv pip install -e '.[dev]'` |
| Run tests | `pytest` |
| Run with coverage | `pytest --cov=src` |
| Lint check | `ruff check src tests` |
| Format code | `ruff format src tests` |
| Type check | `mypy src` |

## Adding Tests

### Test File Template
```python
import pytest

class TestFeature:
    def test_basic(self, sample_data):
        assert sample_data["key"] == "value"

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
    ])
    def test_parametrized(self, input, expected):
        assert input * 2 == expected
```

### Adding Fixtures (conftest.py)
```python
@pytest.fixture
def api_client():
    client = create_client()
    yield client
    client.close()
```

## Running Tests

```bash
# Basic testing
pytest                          # all tests
pytest tests/unit/              # specific directory
pytest -k "test_name"           # by name pattern
pytest -m "not slow"            # exclude markers
pytest --cov=src                # with coverage
pytest -n auto                  # parallel execution

# With uv
uv run pytest                   # run in uv environment
uv run pytest --cov=src         # coverage in uv environment
```

## References

- **Patterns**: See [references/patterns.md](references/patterns.md) for fixtures, parametrize, mocking, async tests
- **UV Commands**: See [references/tox-config.md](references/tox-config.md) for environment setup, CI integration
