---
name: openai-agents
description: Scaffold and develop OpenAI Agents SDK projects with uv integration. Use when users want to create multi-agent workflows, build agents with tools, implement handoffs between agents, add guardrails, or follow OpenAI Agents best practices. Triggers on requests like "create an agent", "build multi-agent system", "add tools to agent", or any OpenAI Agents SDK development task.
---

# OpenAI Agents SDK

Scaffold and develop multi-agent AI workflows using the OpenAI Agents SDK.

## Quick Start: New Project

```bash
python scripts/scaffold.py my-agents --path /target/directory
```

Creates:
```
my-agents/
├── pyproject.toml          # openai-agents + dev deps
├── .env.example            # API key template
├── src/my_agents/
│   ├── agents/
│   │   ├── basic.py        # Simple agent example
│   │   ├── with_tools.py   # Agent with custom tools
│   │   ├── multi_agent.py  # Handoff example
│   │   └── with_context.py # Dependency injection
│   └── tools/
└── tests/
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | LLM with instructions, tools, and handoffs |
| **Tools** | Python functions the agent can call |
| **Handoffs** | Transfer control between agents |
| **Context** | Dependency injection for tools |
| **Sessions** | Conversation memory persistence |
| **Guardrails** | Input/output validation |

## Basic Agent

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

result = await Runner.run(agent, "Hello!")
print(result.final_output)
```

## Agent with Tools

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny, 72F"

agent = Agent(
    name="WeatherBot",
    instructions="Help users check weather.",
    tools=[get_weather],
)
```

## Multi-Agent Handoffs

```python
specialist = Agent(name="Specialist", instructions="...")

triage = Agent(
    name="Triage",
    instructions="Route to Specialist for complex issues.",
    handoffs=[specialist],
)
```

## UV Commands

| Task | Command |
|------|---------|
| Install | `uv pip install -e '.[dev]'` |
| Run agent | `python src/my_agents/agents/basic.py` |
| Run tests | `pytest` |
| Lint | `ruff check src` |

## References

- **Patterns**: See [references/patterns.md](references/patterns.md) for tools, handoffs, context, sessions, guardrails
- **API Reference**: See [references/api_reference.md](references/api_reference.md) for classes, events, env vars
