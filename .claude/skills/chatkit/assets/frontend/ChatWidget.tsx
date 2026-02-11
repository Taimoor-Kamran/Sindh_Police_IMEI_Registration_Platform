"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

interface ChatWidgetProps {
  /** Backend ChatKit endpoint URL */
  apiUrl?: string;
  /** Domain key for multi-tenant apps */
  domainKey?: string;
  /** Container height */
  height?: string;
  /** Custom headers to send with requests */
  headers?: Record<string, string>;
  /** Theme customization */
  theme?: {
    primaryColor?: string;
    backgroundColor?: string;
    textColor?: string;
    fontFamily?: string;
  };
}

export function ChatWidget({
  apiUrl = process.env.NEXT_PUBLIC_CHATKIT_URL || "http://localhost:8000/chatkit",
  domainKey = "default",
  height = "600px",
  headers = {},
  theme = {},
}: ChatWidgetProps) {
  const chatkit = useChatKit({
    api: {
      url: apiUrl,
      domainKey: domainKey,
      headers: headers,
    },
  });

  return (
    <div style={{ height, width: "100%" }}>
      <ChatKit
        control={chatkit.control}
        theme={theme}
      />
    </div>
  );
}
