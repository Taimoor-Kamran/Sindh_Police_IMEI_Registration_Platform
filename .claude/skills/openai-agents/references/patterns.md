# OpenAI Agents Patterns Reference

## Agent Creation

### Basic Agent
```python
from agents import Agent

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)
```

### Agent with Model Selection
```python
agent = Agent(
    name="GPT4Agent",
    instructions="You are an expert analyst.",
    model="gpt-4o",  # or "gpt-4o-mini", "gpt-3.5-turbo"
)
```

## Tools

### Function Tool Decorator
```python
from agents import function_tool

@function_tool
def search_database(query: str, limit: int = 10) -> str:
    # Automatic schema generation from type hints
    results = db.search(query, limit=limit)
    return str(results)
```

### Tool with Pydantic Validation
```python
from pydantic import BaseModel, Field
from agents import function_tool

class SearchParams(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(10, ge=1, le=100)

@function_tool
def search(params: SearchParams) -> str:
    return f"Searching for: {params.query}"
```

### Async Tools
```python
@function_tool
async def fetch_data(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

## Handoffs

### Basic Handoff
```python
specialist = Agent(name="Specialist", instructions="...")

triage = Agent(
    name="Triage",
    instructions="Route to Specialist for complex issues.",
    handoffs=[specialist],
)
```

### Conditional Handoffs
```python
tech_support = Agent(name="TechSupport", instructions="...")
billing = Agent(name="Billing", instructions="...")

triage = Agent(
    name="Triage",
    instructions="""
    Route requests based on topic:
    - Technical issues -> TechSupport
    - Payment/billing -> Billing
    """,
    handoffs=[tech_support, billing],
)
```

## Context (Dependency Injection)

### Define Context Class
```python
from dataclasses import dataclass

@dataclass
class AppContext:
    user_id: str
    session_id: str
    db_connection: Any
```

### Access Context in Tools
```python
from agents import RunContextWrapper

@function_tool
def get_user_data(wrapper: RunContextWrapper[AppContext]) -> str:
    ctx = wrapper.context
    data = ctx.db_connection.get_user(ctx.user_id)
    return str(data)
```

### Pass Context to Runner
```python
context = AppContext(
    user_id="user-123",
    session_id="session-456",
    db_connection=db
)

result = await Runner.run(agent, message, context=context)
```

## Sessions (Memory)

### SQLite Session
```python
from agents.extensions.memory import AdvancedSQLiteSession

session = AdvancedSQLiteSession(
    session_id="conversation_123",
    db_path="conversations.db",
    create_tables=True
)

result = await Runner.run(agent, message, session=session)
await session.store_run_usage(result)
```

### Encrypted Session
```python
from agents.extensions.memory import EncryptedSession, SQLAlchemySession

underlying = SQLAlchemySession.from_url(
    "user-123",
    url="sqlite+aiosqlite:///:memory:",
    create_tables=True
)

session = EncryptedSession(
    session_id="user-123",
    underlying_session=underlying,
    encryption_key="secret-key",
    ttl=600
)
```

## Guardrails

### Input Validation
```python
from agents import Agent, InputGuardrail

def validate_input(message: str) -> bool:
    # Return True if valid, False to block
    if len(message) > 10000:
        return False
    return True

agent = Agent(
    name="SafeAgent",
    instructions="...",
    input_guardrails=[InputGuardrail(validate_input)],
)
```

### Output Validation
```python
from agents import OutputGuardrail

def validate_output(response: str) -> bool:
    # Check for sensitive data patterns
    if "password" in response.lower():
        return False
    return True

agent = Agent(
    name="SafeAgent",
    instructions="...",
    output_guardrails=[OutputGuardrail(validate_output)],
)
```

## Streaming

### Stream Events
```python
async for event in Runner.run_streamed(agent, message):
    if event.type == "agent_start":
        print(f"Agent: {event.agent.name}")
    elif event.type == "tool_start":
        print(f"Tool: {event.tool.name}")
    elif event.type == "tool_end":
        print(f"Result: {event.output}")
    elif event.type == "text_delta":
        print(event.delta, end="", flush=True)
```

## Error Handling

```python
from agents.exceptions import AgentError, ToolError

try:
    result = await Runner.run(agent, message)
except ToolError as e:
    print(f"Tool failed: {e.tool_name} - {e.message}")
except AgentError as e:
    print(f"Agent error: {e}")
```

## Tracing

```python
from agents import Runner, set_tracing_disabled

# Disable tracing (e.g., in production)
set_tracing_disabled(True)

# Or use environment variable
# OPENAI_AGENTS_DISABLE_TRACING=1
```
