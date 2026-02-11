---
name: chatkit
description: Integrate OpenAI ChatKit into projects with Next.js frontend and FastAPI backend. Use when users want to add ChatKit chat UI, connect ChatKit to OpenAI Agents SDK, set up ChatKit server with FastAPI, or build real-time streaming chat interfaces. Triggers on requests like "add ChatKit", "integrate ChatKit", "ChatKit frontend", "ChatKit backend", or connecting ChatKit to existing agents.
---

# ChatKit Integration

Integrate OpenAI ChatKit for real-time chat UI with FastAPI + OpenAI Agents SDK backend.

## Architecture

```
Next.js (ChatKit React) ──POST /chatkit──▶ FastAPI (ChatKit Python) ──▶ OpenAI Agents SDK ──▶ LLM
                         ◀──SSE Stream───
```

**Key insight**: ChatKit Python SDK is a transport layer only - it does NOT call LLMs. Your OpenAI Agents SDK handles all AI logic.

## Workflow Decision Tree

1. **Frontend only?** → Go to [Frontend Setup](#frontend-setup)
2. **Backend only?** → Go to [Backend Setup](#backend-setup)
3. **Full integration?** → Do Backend first, then Frontend

## Frontend Setup

### 1. Install dependencies

```bash
npm install @openai/chatkit-react
```

### 2. Add ChatKit script to layout

In `app/layout.tsx`:

```tsx
import Script from "next/script";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="beforeInteractive"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 3. Copy ChatWidget component

Copy `assets/frontend/ChatWidget.tsx` to your components directory.

### 4. Use in page

```tsx
import { ChatWidget } from "@/components/ChatWidget";

export default function ChatPage() {
  return <ChatWidget apiUrl="http://localhost:8000/chatkit" />;
}
```

**For detailed frontend options**: See [references/frontend.md](references/frontend.md)

## Backend Setup

### 1. Install dependencies

```bash
pip install openai-chatkit openai-agents fastapi uvicorn
```

### 2. Copy server template

Copy `assets/backend/chatkit_server.py` to your FastAPI project.

### 3. Customize the agent

Edit the agent definition with your tools and instructions:

```python
from agents import Agent, function_tool

@function_tool
def your_tool(query: str) -> str:
    """Your tool description."""
    return "result"

agent = Agent(
    name="YourAgent",
    instructions="Your agent instructions.",
    model="gpt-4o",
    tools=[your_tool],
)
```

### 4. Add to existing FastAPI app

If adding to existing app, import the router:

```python
from chatkit_server import chatkit_endpoint

app.add_api_route("/chatkit", chatkit_endpoint, methods=["POST"])
```

### 5. Configure CORS

Update CORS origins for your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For PostgreSQL store and advanced patterns**: See [references/backend.md](references/backend.md)

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_CHATKIT_URL=http://localhost:8000/chatkit
```

### Backend (.env)
```
OPENAI_API_KEY=sk-...
```

## Quick Verification

1. Start backend: `uvicorn chatkit_server:app --reload`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000 and send a message

## Resources

- `assets/frontend/ChatWidget.tsx` - Ready-to-use React component
- `assets/backend/chatkit_server.py` - FastAPI server with OpenAI Agents
- `references/frontend.md` - Detailed frontend configuration
- `references/backend.md` - Backend patterns and PostgreSQL store
