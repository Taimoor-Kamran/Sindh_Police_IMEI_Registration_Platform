#!/usr/bin/env python3
"""Scaffold an OpenAI Agents project with uv integration."""

import argparse
from pathlib import Path

PYPROJECT_TOML = '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.9"
dependencies = [
    "openai-agents>=0.0.3",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23.0",
    "python-dotenv>=1.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
voice = [
    "numpy>=1.26.0",
    "sounddevice>=0.4.6",
    "websockets>=12.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
disallow_untyped_defs = true
'''

ENV_EXAMPLE = '''# OpenAI API Configuration
OPENAI_API_KEY=your-api-key-here

# Optional: Organization ID
# OPENAI_ORG_ID=org-xxx

# Optional: Custom base URL
# OPENAI_BASE_URL=https://api.openai.com/v1
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

# Environment
.env
.venv/
venv/

# IDE
.idea/
.vscode/
*.swp

# Agents
*.db
conversations.db
'''

BASIC_AGENT = '''# Basic agent example

import asyncio
from agents import Agent, Runner


# Define your agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be concise and clear in your responses.",
)


async def main():
    # Run a simple conversation
    result = await Runner.run(agent, "Hello! What can you help me with?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
'''

AGENT_WITH_TOOLS = '''# Agent with custom tools example

import asyncio
from agents import Agent, Runner, function_tool


# Define custom tools using the @function_tool decorator
@function_tool
def get_weather(city: str) -> str:
    # Get weather for a city (mock implementation)
    return f"The weather in {city} is sunny, 72F"


@function_tool
def calculate(expression: str) -> str:
    # Safely evaluate a math expression
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Create agent with tools
agent = Agent(
    name="ToolAgent",
    instructions="You are a helpful assistant with access to weather and calculator tools.",
    tools=[get_weather, calculate],
)


async def main():
    result = await Runner.run(
        agent,
        "What is the weather in San Francisco? Also, what is 25 * 4?"
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
'''

MULTI_AGENT = '''# Multi-agent workflow with handoffs

import asyncio
from agents import Agent, Runner


# Define specialized agents
triage_agent = Agent(
    name="Triage",
    instructions="You route user requests to the appropriate specialist. "
                 "For technical questions, handoff to TechSupport. "
                 "For billing questions, handoff to Billing.",
    handoffs=["TechSupport", "Billing"],
)

tech_agent = Agent(
    name="TechSupport",
    instructions="You are a technical support specialist. "
                 "Help users with technical issues and troubleshooting.",
)

billing_agent = Agent(
    name="Billing",
    instructions="You are a billing specialist. "
                 "Help users with billing questions and account issues.",
)

# Register agents for handoffs
triage_agent.handoffs = [tech_agent, billing_agent]


async def main():
    result = await Runner.run(
        triage_agent,
        "I am having trouble connecting to the API"
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
'''

AGENT_WITH_CONTEXT = '''# Agent with context (dependency injection)

import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool


@dataclass
class UserContext:
    # Context object passed to all tools and agents
    user_id: str
    user_name: str
    preferences: dict


@function_tool
def get_user_profile(wrapper: RunContextWrapper[UserContext]) -> str:
    # Access context in tool
    ctx = wrapper.context
    return f"User: {ctx.user_name} (ID: {ctx.user_id})"


@function_tool
def get_preferences(wrapper: RunContextWrapper[UserContext]) -> str:
    # Access user preferences from context
    ctx = wrapper.context
    return f"Preferences: {ctx.preferences}"


agent = Agent(
    name="PersonalAssistant",
    instructions="You are a personal assistant. Use the available tools to help the user.",
    tools=[get_user_profile, get_preferences],
)


async def main():
    # Create context with user data
    context = UserContext(
        user_id="user-123",
        user_name="Alice",
        preferences={"theme": "dark", "language": "en"}
    )

    result = await Runner.run(
        agent,
        "What are my current preferences?",
        context=context
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
'''

CONFTEST = '''# Pytest fixtures for OpenAI Agents testing

import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_openai_response():
    # Mock OpenAI API response
    return {
        "choices": [
            {"message": {"content": "Mocked response"}}
        ]
    }


@pytest.fixture
def mock_runner():
    # Mock the Runner for testing
    with patch("agents.Runner.run", new_callable=AsyncMock) as mock:
        yield mock
'''

TEST_EXAMPLE = '''# Example test for agents

import pytest
from agents import Agent


class TestBasicAgent:
    def test_agent_creation(self):
        agent = Agent(
            name="TestAgent",
            instructions="Test instructions"
        )
        assert agent.name == "TestAgent"

    def test_agent_with_tools(self):
        from agents import function_tool

        @function_tool
        def dummy_tool() -> str:
            return "result"

        agent = Agent(
            name="ToolAgent",
            instructions="Agent with tools",
            tools=[dummy_tool]
        )
        assert len(agent.tools) == 1


class TestAgentIntegration:
    @pytest.mark.asyncio
    async def test_basic_run(self, mock_runner):
        # Test with mocked runner
        mock_runner.return_value.final_output = "Test response"

        agent = Agent(name="Test", instructions="Test")
        result = await mock_runner(agent, "Hello")

        assert result.final_output == "Test response"
'''


def create_project(name: str, path: Path, description: str = ""):
    """Create OpenAI Agents project structure with uv."""
    project_path = path / name
    pkg_name = name.replace("-", "_")

    # Create directories
    dirs = [
        project_path / "src" / pkg_name / "agents",
        project_path / "src" / pkg_name / "tools",
        project_path / "tests",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create __init__.py files
    init_files = [
        project_path / "src" / pkg_name / "__init__.py",
        project_path / "src" / pkg_name / "agents" / "__init__.py",
        project_path / "src" / pkg_name / "tools" / "__init__.py",
        project_path / "tests" / "__init__.py",
    ]

    for f in init_files:
        f.write_text('"""Package initialization."""\n')

    # Create main files
    desc = description or f"An OpenAI Agents project: {name}"

    (project_path / "pyproject.toml").write_text(
        PYPROJECT_TOML.format(name=name, description=desc)
    )
    (project_path / ".env.example").write_text(ENV_EXAMPLE)
    (project_path / ".gitignore").write_text(GITIGNORE)

    # Create example agents
    (project_path / "src" / pkg_name / "agents" / "basic.py").write_text(BASIC_AGENT)
    (project_path / "src" / pkg_name / "agents" / "with_tools.py").write_text(AGENT_WITH_TOOLS)
    (project_path / "src" / pkg_name / "agents" / "multi_agent.py").write_text(MULTI_AGENT)
    (project_path / "src" / pkg_name / "agents" / "with_context.py").write_text(AGENT_WITH_CONTEXT)

    # Create test files
    (project_path / "tests" / "conftest.py").write_text(CONFTEST)
    (project_path / "tests" / "test_agents.py").write_text(TEST_EXAMPLE)

    print(f"Created OpenAI Agents project: {project_path}")
    print(f"\nStructure:")
    print(f"  {name}/")
    print(f"  ├── pyproject.toml")
    print(f"  ├── .env.example")
    print(f"  ├── .gitignore")
    print(f"  ├── src/{pkg_name}/")
    print(f"  │   ├── agents/")
    print(f"  │   │   ├── basic.py")
    print(f"  │   │   ├── with_tools.py")
    print(f"  │   │   ├── multi_agent.py")
    print(f"  │   │   └── with_context.py")
    print(f"  │   └── tools/")
    print(f"  └── tests/")
    print(f"      ├── conftest.py")
    print(f"      └── test_agents.py")
    print(f"\nNext steps:")
    print(f"  cd {name}")
    print(f"  cp .env.example .env      # Add your OPENAI_API_KEY")
    print(f"  uv pip install -e '.[dev]'")
    print(f"  python src/{pkg_name}/agents/basic.py")


def main():
    parser = argparse.ArgumentParser(description="Scaffold OpenAI Agents project with uv")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    parser.add_argument("--description", default="", help="Project description")

    args = parser.parse_args()
    create_project(args.name, args.path, args.description)


if __name__ == "__main__":
    main()
