"use client";
import { useEffect, useRef, useState } from "react";
import { MessageResponse } from "@/app/lib/api";

interface ChatWindowProps {
  messages: MessageResponse[];
  loading: boolean;
  error: string | null;
  onSend: (content: string) => void;
  sessionTitle: string;
}

function TypingDots() {
  return (
    <div className="typing-dots" data-testid="chat-loading" aria-label="Assistant is typing">
      <span /><span /><span />
    </div>
  );
}

function MessageBubble({ msg }: { msg: MessageResponse }) {
  const isUser = msg.sender === "user";
  return (
    <div className={`message-row ${isUser ? "user-row" : "ai-row"}`}>
      {!isUser && (
        <div className="avatar ai-avatar" aria-hidden>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <rect width="16" height="16" rx="4" fill="#01696f" />
            <text x="2" y="12" fontSize="9" fontWeight="700" fill="white" fontFamily="monospace">AI</text>
          </svg>
        </div>
      )}
      <div
        className={`bubble ${isUser ? "bubble-user" : "bubble-ai"}`}
        data-testid={isUser ? "user-message" : "assistant-message"}
      >
        {msg.content}
      </div>
    </div>
  );
}

export default function ChatWindow({
  messages,
  loading,
  error,
  onSend,
  sessionTitle,
}: ChatWindowProps) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;
    onSend(trimmed);
    setInput("");
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-window">
      {/* Chat Header */}
      <div className="chat-header">
        <span className="chat-header-title">{sessionTitle}</span>
      </div>

      {/* Messages */}
      <div className="message-list" data-testid="message-list">
        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <p>Send a message to start the conversation.</p>
          </div>
        )}
        {messages.map((msg) => (
          <MessageBubble key={msg.id === -1 ? `temp-${msg.order}` : msg.id} msg={msg} />
        ))}
        {loading && (
          <div className="message-row ai-row">
            <div className="avatar ai-avatar" aria-hidden>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <rect width="16" height="16" rx="4" fill="#01696f" />
                <text x="2" y="12" fontSize="9" fontWeight="700" fill="white" fontFamily="monospace">AI</text>
              </svg>
            </div>
            <div className="bubble bubble-ai">
              <TypingDots />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Error */}
      {error && (
        <div className="error-banner" data-testid="error-banner" role="alert">
          {error}
        </div>
      )}

      {/* Input */}
      <div className="chat-input-area">
        <textarea
          ref={inputRef}
          className="chat-input"
          data-testid="message-input"
          placeholder="Message ESBot…"
          value={input}
          rows={1}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          aria-label="Message input"
        />
        <button
          className="send-btn"
          data-testid="send-message-btn"
          onClick={handleSend}
          disabled={loading || !input.trim()}
          aria-label="Send message"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 10L17 3l-7 7 7 7-14-7z" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
      </div>
    </div>
  );
}
