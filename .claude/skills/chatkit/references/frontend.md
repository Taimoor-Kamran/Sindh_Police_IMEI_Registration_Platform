# ChatKit Frontend Setup (Next.js)

## Table of Contents
1. [Installation](#installation)
2. [Script Setup](#script-setup)
3. [ChatKit Component](#chatkit-component)
4. [Configuration Options](#configuration-options)
5. [Theming](#theming)

## Installation

```bash
npm install @openai/chatkit-react
```

## Script Setup

Add ChatKit script to `app/layout.tsx`:

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

## ChatKit Component

Basic component pointing to FastAPI backend:

```tsx
"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

interface ChatWidgetProps {
  apiUrl?: string;
  domainKey?: string;
  height?: string;
}

export function ChatWidget({
  apiUrl = "http://localhost:8000/chatkit",
  domainKey = "default",
  height = "600px"
}: ChatWidgetProps) {
  const chatkit = useChatKit({
    api: {
      url: apiUrl,
      domainKey: domainKey,
    },
  });

  return (
    <div style={{ height }}>
      <ChatKit control={chatkit.control} />
    </div>
  );
}
```

## Configuration Options

### useChatKit options

| Option | Type | Description |
|--------|------|-------------|
| `api.url` | string | Backend endpoint URL |
| `api.domainKey` | string | Domain identifier for multi-tenant apps |
| `api.headers` | object | Custom headers to send with requests |

### Custom headers for context

```tsx
const chatkit = useChatKit({
  api: {
    url: "/api/chatkit",
    headers: {
      "X-User-ID": userId,
      "X-Session-ID": sessionId,
    },
  },
});
```

## Theming

```tsx
<ChatKit
  control={chatkit.control}
  theme={{
    primaryColor: "#0066cc",
    backgroundColor: "#ffffff",
    fontFamily: "Inter, sans-serif",
  }}
/>
```

### Dark mode support

```tsx
const theme = isDarkMode ? {
  primaryColor: "#60a5fa",
  backgroundColor: "#1f2937",
  textColor: "#f9fafb",
} : {
  primaryColor: "#2563eb",
  backgroundColor: "#ffffff",
  textColor: "#111827",
};
```
