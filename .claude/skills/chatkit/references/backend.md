# ChatKit Backend Setup (FastAPI + OpenAI Agents)

## Table of Contents
1. [Installation](#installation)
2. [ChatKitServer Implementation](#chatkitserver-implementation)
3. [Store Implementation](#store-implementation)
4. [OpenAI Agents Integration](#openai-agents-integration)
5. [FastAPI Endpoint](#fastapi-endpoint)
6. [PostgreSQL Store](#postgresql-store)

## Installation

```bash
pip install openai-chatkit openai-agents fastapi uvicorn
```

## ChatKitServer Implementation

The `ChatKitServer` base class handles protocol between frontend and backend. Implement the `respond` method to process messages:

```python
from chatkit.server import ChatKitServer, Store
from chatkit.server.types import Thread, ThreadItem
from chatkit.server.agents import simple_to_agent_input

class MyChatKitServer(ChatKitServer[dict]):
    def __init__(self, store: Store, agent):
        super().__init__(store=store)
        self.agent = agent

    async def respond(self, thread: Thread, input_message: ThreadItem, context: dict):
        """Called each time user sends a message. Yields events to stream back."""
        # Convert thread to agent input
        agent_input = simple_to_agent_input(thread.items)

        # Run agent and stream responses
        from agents import Runner
        runner = Runner(agent=self.agent)

        async for event in runner.run_stream(agent_input):
            if event.type == "text_delta":
                yield {"type": "text", "content": event.delta}
            elif event.type == "tool_call_start":
                yield {"type": "tool_status", "name": event.name, "status": "running"}
            elif event.type == "tool_call_end":
                yield {"type": "tool_status", "name": event.name, "status": "complete"}
```

## Store Implementation

### In-Memory Store (Development)

```python
from chatkit.server import Store
from chatkit.server.types import Thread

class InMemoryStore(Store[dict]):
    def __init__(self):
        self.threads: dict[str, Thread] = {}

    async def get_thread(self, thread_id: str) -> Thread | None:
        return self.threads.get(thread_id)

    async def save_thread(self, thread: Thread) -> None:
        self.threads[thread.id] = thread

    async def delete_thread(self, thread_id: str) -> None:
        self.threads.pop(thread_id, None)
```

## OpenAI Agents Integration

Define your agent with tools:

```python
from agents import Agent, function_tool

@function_tool
def search_database(query: str) -> str:
    """Search the database for information."""
    # Your database logic
    return f"Results for: {query}"

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    tools=[search_database],
)
```

## FastAPI Endpoint

Single endpoint handling both JSON and SSE streaming:

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = InMemoryStore()
chatkit_server = MyChatKitServer(store=store, agent=agent)

@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    body = await request.body()

    # Extract custom headers for context
    context = {
        "user_id": request.headers.get("X-User-ID"),
        "session_id": request.headers.get("X-Session-ID"),
    }

    result = await chatkit_server.process(body, context=context)

    # Streaming response
    if hasattr(result, '__aiter__'):
        return StreamingResponse(result, media_type="text/event-stream")

    # JSON response
    return Response(content=result.json(), media_type="application/json")
```

## PostgreSQL Store

Production store using SQLAlchemy:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from chatkit.server import Store
from chatkit.server.types import Thread
from app.models import ThreadModel  # Your SQLModel/SQLAlchemy model

class PostgresStore(Store[dict]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_thread(self, thread_id: str) -> Thread | None:
        result = await self.db.execute(
            select(ThreadModel).where(ThreadModel.id == thread_id)
        )
        row = result.scalar_one_or_none()
        if row:
            return Thread(id=row.id, items=row.items)
        return None

    async def save_thread(self, thread: Thread) -> None:
        existing = await self.get_thread(thread.id)
        if existing:
            await self.db.execute(
                update(ThreadModel)
                .where(ThreadModel.id == thread.id)
                .values(items=thread.items)
            )
        else:
            self.db.add(ThreadModel(id=thread.id, items=thread.items))
        await self.db.commit()
```

### Thread Model (SQLModel)

```python
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class ThreadModel(SQLModel, table=True):
    __tablename__ = "chatkit_threads"

    id: str = Field(primary_key=True)
    items: list = Field(sa_column=Column(JSON))
    user_id: str | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```
