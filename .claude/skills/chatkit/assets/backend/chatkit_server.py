"""
ChatKit Server implementation with OpenAI Agents SDK integration.

Copy this file to your FastAPI project and customize:
1. Define your agent with tools
2. Implement PostgresStore for production
3. Add to your FastAPI app routes
"""

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from chatkit.server import ChatKitServer, Store
from chatkit.server.types import Thread, ThreadItem
from chatkit.server.agents import simple_to_agent_input

from agents import Agent, Runner, function_tool


# =============================================================================
# Store Implementation (In-Memory for development)
# =============================================================================

class InMemoryStore(Store[dict]):
    """In-memory store for development. Replace with PostgresStore for production."""

    def __init__(self):
        self.threads: dict[str, Thread] = {}

    async def get_thread(self, thread_id: str) -> Thread | None:
        return self.threads.get(thread_id)

    async def save_thread(self, thread: Thread) -> None:
        self.threads[thread.id] = thread

    async def delete_thread(self, thread_id: str) -> None:
        self.threads.pop(thread_id, None)


# =============================================================================
# ChatKit Server with OpenAI Agents
# =============================================================================

class MyChatKitServer(ChatKitServer[dict]):
    """ChatKit server that uses OpenAI Agents SDK for AI logic."""

    def __init__(self, store: Store, agent: Agent):
        super().__init__(store=store)
        self.agent = agent

    async def respond(self, thread: Thread, input_message: ThreadItem, context: dict):
        """
        Called each time user sends a message.
        Yields events to stream back to ChatKit frontend.
        """
        # Convert thread history to agent input format
        agent_input = simple_to_agent_input(thread.items)

        # Run OpenAI Agent with streaming
        runner = Runner(agent=self.agent)

        async for event in runner.run_stream(agent_input):
            if event.type == "text_delta":
                yield {"type": "text", "content": event.delta}
            elif event.type == "tool_call_start":
                yield {"type": "tool_status", "name": event.name, "status": "running"}
            elif event.type == "tool_call_end":
                yield {"type": "tool_status", "name": event.name, "status": "complete"}


# =============================================================================
# Define Your Agent and Tools
# =============================================================================

# Example tool - replace with your own
@function_tool
def get_current_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().isoformat()


# Define your agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    tools=[get_current_time],
)


# =============================================================================
# FastAPI Setup
# =============================================================================

app = FastAPI(title="ChatKit Backend")

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatKit server
store = InMemoryStore()
chatkit_server = MyChatKitServer(store=store, agent=agent)


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    """
    Single ChatKit endpoint.
    Handles both JSON responses and SSE streaming.
    """
    body = await request.body()

    # Extract context from headers
    context = {
        "user_id": request.headers.get("X-User-ID"),
        "session_id": request.headers.get("X-Session-ID"),
    }

    result = await chatkit_server.process(body, context=context)

    # Return streaming response for real-time updates
    if hasattr(result, '__aiter__'):
        return StreamingResponse(result, media_type="text/event-stream")

    # Return JSON for non-streaming responses
    return Response(content=result.json(), media_type="application/json")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
