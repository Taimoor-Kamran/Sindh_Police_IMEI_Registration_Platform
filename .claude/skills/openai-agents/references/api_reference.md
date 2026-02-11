# OpenAI Agents API Reference

## Installation

```bash
# Basic installation
pip install openai-agents

# With uv
uv pip install openai-agents

# With voice support
uv pip install "openai-agents[voice]"
```

## Core Classes

### Agent

```python
Agent(
    name: str,                      # Agent identifier
    instructions: str,              # System prompt
    model: str = "gpt-4o-mini",    # Model to use
    tools: list = [],              # List of tools
    handoffs: list = [],           # Agents for handoff
    input_guardrails: list = [],   # Input validators
    output_guardrails: list = [],  # Output validators
)
```

### Runner

```python
# Async run
result = await Runner.run(
    agent: Agent,
    input: str,
    context: Any = None,
    session: Session = None,
    max_turns: int = 10,
)

# Streamed run
async for event in Runner.run_streamed(agent, input):
    ...
```

### Result Object

```python
result.final_output      # Final response string
result.messages          # Conversation history
result.tool_calls        # Tools that were called
result.usage            # Token usage statistics
```

## Event Types (Streaming)

| Event Type | Description |
|------------|-------------|
| `agent_start` | Agent begins processing |
| `agent_end` | Agent finishes processing |
| `tool_start` | Tool execution begins |
| `tool_end` | Tool execution completes |
| `text_delta` | Streaming text chunk |
| `handoff` | Control transferred to another agent |
| `error` | Error occurred |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key (required) |
| `OPENAI_ORG_ID` | Organization ID |
| `OPENAI_BASE_URL` | Custom API endpoint |
| `OPENAI_AGENTS_DISABLE_TRACING` | Disable tracing |

## UV Commands

| Task | Command |
|------|---------|
| Install | `uv pip install openai-agents` |
| Install dev | `uv pip install -e '.[dev]'` |
| Run agent | `uv run python src/agents/basic.py` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check src` |
| Type check | `uv run mypy src` |

## Common Patterns

### Multi-turn Conversation
```python
session = AdvancedSQLiteSession(session_id="user-123")

# Turn 1
result1 = await Runner.run(agent, "Hello", session=session)
await session.store_run_usage(result1)

# Turn 2 (remembers context)
result2 = await Runner.run(agent, "What did I say?", session=session)
```

### Parallel Tool Calls
```python
# Agent can call multiple tools simultaneously
agent = Agent(
    name="ParallelAgent",
    instructions="Use multiple tools at once when appropriate.",
    tools=[tool1, tool2, tool3],
    parallel_tool_calls=True,  # Enable parallel execution
)
```

### Custom Model Providers
```python
from agents import Agent, set_default_openai_client
from openai import AsyncOpenAI

# Use custom client
client = AsyncOpenAI(base_url="https://custom-api.example.com")
set_default_openai_client(client)
```
