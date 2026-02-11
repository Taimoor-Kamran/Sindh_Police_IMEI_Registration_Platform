#!/usr/bin/env python3
"""Scaffold a pytest project with uv integration."""

import argparse
import os
from pathlib import Path

PYPROJECT_TOML = '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-xdist>=3.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[tool.pytest.ini_options]
addopts = [
    "--import-mode=importlib",
    "-v",
    "--strict-markers",
]
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]

[tool.ruff]
line-length = 88
indent-width = 4

[tool.ruff.lint]
select = ["E", "W", "F", "I", "C", "B", "UP", "SIM", "ARG", "PT", "PL", "TRY"]
ignore = ["PLR", "PLC0415"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
'''

CONFTEST_PY = '''# Shared pytest fixtures (docstring commented out to avoid quote conflicts)

import pytest


@pytest.fixture
def sample_data():
    # Provide sample test data (commented out to avoid quote conflicts)
    return {"key": "value", "count": 42}


@pytest.fixture(scope="session")
def session_resource():
    # Resource shared across all tests in session (commented out to avoid quote conflicts)
    resource = setup_resource()
    yield resource
    teardown_resource(resource)


def setup_resource():
    # Setup logic for session resource (commented out to avoid quote conflicts)
    return {"initialized": True}


def teardown_resource(resource):
    # Teardown logic for session resource (commented out to avoid quote conflicts)
    pass
'''

TEST_EXAMPLE = '''# Example test module (docstring commented out to avoid quote conflicts)

import pytest


class TestExample:
    # Example test class (commented out to avoid quote conflicts)

    def test_basic(self, sample_data):
        # Test using fixture (commented out to avoid quote conflicts)
        assert sample_data["key"] == "value"
        assert sample_data["count"] == 42

    @pytest.mark.parametrize(
        "input_val,expected",
        [
            (1, 2),
            (2, 4),
            (3, 6),
        ],
    )
    def test_parametrized(self, input_val, expected):
        # Test with parametrized inputs (commented out to avoid quote conflicts)
        assert input_val * 2 == expected

    @pytest.mark.slow
    def test_slow_operation(self):
        # Test marked as slow (commented out to avoid quote conflicts)
        result = sum(range(1000))
        assert result == 499500
'''

GITIGNORE = '''# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
.venv/
venv/
'''


def create_project(name: str, path: Path, description: str = ""):
    """Create pytest project structure with uv."""
    project_path = path / name

    # Create directories
    dirs = [
        project_path / "src" / name.replace("-", "_"),
        project_path / "tests" / "unit",
        project_path / "tests" / "integration",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    init_files = [
        project_path / "src" / name.replace("-", "_") / "__init__.py",
        project_path / "tests" / "__init__.py",
        project_path / "tests" / "unit" / "__init__.py",
        project_path / "tests" / "integration" / "__init__.py",
    ]

    for f in init_files:
        f.write_text('"""Package initialization."""\n')

    # Create main files
    desc = description or f"A Python project: {name}"
    pkg_name = name.replace("-", "_")

    (project_path / "pyproject.toml").write_text(
        PYPROJECT_TOML.format(name=name, description=desc)
    )
    (project_path / "tests" / "conftest.py").write_text(CONFTEST_PY)
    (project_path / "tests" / "unit" / "test_example.py").write_text(TEST_EXAMPLE)
    (project_path / ".gitignore").write_text(GITIGNORE)

    # Create placeholder module
    (project_path / "src" / pkg_name / "main.py").write_text(
        f'"""Main module for {name}."""\n\n\ndef hello() -> str:\n    """Return greeting."""\n    return "Hello, World!"\n'
    )

    print(f"Created pytest project: {project_path}")
    print(f"\nStructure:")
    print(f"  {name}/")
    print(f"  ├── pyproject.toml")
    print(f"  ├── .gitignore")
    print(f"  ├── src/{pkg_name}/")
    print(f"  │   ├── __init__.py")
    print(f"  │   └── main.py")
    print(f"  └── tests/")
    print(f"      ├── conftest.py")
    print(f"      ├── unit/")
    print(f"      │   └── test_example.py")
    print(f"      └── integration/")
    print(f"\nNext steps:")
    print(f"  cd {name}")
    print(f"  pip install -e '.[dev]'  # or: uv pip install -e '.[dev]'")
    print(f"  pytest                    # run tests")
    print(f"  pytest --cov=src          # with coverage")
    print(f"  ruff check src tests      # lint check")
    print(f"  mypy src                  # type check")


def main():
    parser = argparse.ArgumentParser(description="Scaffold pytest project with uv")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    parser.add_argument("--description", default="", help="Project description")

    args = parser.parse_args()
    create_project(args.name, args.path, args.description)


if __name__ == "__main__":
    main()