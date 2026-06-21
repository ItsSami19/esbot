"use client";
import { useEffect, useState, useCallback } from "react";
import Sidebar from "@/app/components/Sidebar";
import ChatWindow from "@/app/components/ChatWindow";
import Welcome from "@/app/components/Welcome";
import { useSessions } from "@/app/hooks/useSessions";
import { useChat } from "@/app/hooks/useChat";
import { fetchHealth, SessionResponse } from "@/app/lib/api";

export default function Home() {
  const [activeSession, setActiveSession] = useState<SessionResponse | null>(null);
  const [health, setHealth] = useState<"ok" | "error" | "loading">("loading");
  const [globalError, setGlobalError] = useState<string | null>(null);
  const [showNewForm, setShowNewForm] = useState(false);

  const { sessions, error: sessionError, load, create, remove } = useSessions();
  const { messages, loading, error: chatError, loadHistory, submitMessage, setMessages } = useChat(
    activeSession?.id ?? null
  );

  // Health check on mount
  useEffect(() => {
    fetchHealth()
      .then(() => setHealth("ok"))
      .catch(() => setHealth("error"));
  }, []);

  // Load sessions on mount
  useEffect(() => {
    load();
  }, [load]);

  // Combine errors
  useEffect(() => {
    setGlobalError(sessionError || null);
  }, [sessionError]);

  const handleSelectSession = useCallback(
    async (id: number) => {
      const s = sessions.find((s) => s.id === id) ?? null;
      setActiveSession(s);
      setMessages([]);
      if (s) await loadHistory(id);
    },
    [sessions, loadHistory, setMessages]
  );

  const handleCreate = useCallback(
    async (title: string) => {
      const s = await create(title);
      if (s) {
        setActiveSession(s);
        setMessages([]);
      }
      setShowNewForm(false);
    },
    [create, setMessages]
  );

  const handleDelete = useCallback(
    async (id: number) => {
      await remove(id);
      if (activeSession?.id === id) {
        setActiveSession(null);
        setMessages([]);
      }
    },
    [remove, activeSession, setMessages]
  );

  return (
    <div className="app-layout">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSession?.id ?? null}
        onSelect={handleSelectSession}
        onCreate={handleCreate}
        onDelete={handleDelete}
        healthStatus={health}
      />

      <main className="main-content">
        {globalError && (
          <div className="error-banner" data-testid="error-banner" role="alert">
            {globalError}
          </div>
        )}
        {activeSession ? (
          <ChatWindow
            messages={messages}
            loading={loading}
            error={chatError}
            onSend={submitMessage}
            sessionTitle={activeSession.title}
          />
        ) : (
          <Welcome onNew={() => setShowNewForm(true)} />
        )}
      </main>

      {/* New session modal triggered from Welcome */}
      {showNewForm && (
        <div className="modal-overlay" onClick={() => setShowNewForm(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2 className="modal-title">New Session</h2>
            <NewSessionModal
              onConfirm={(title) => handleCreate(title)}
              onCancel={() => setShowNewForm(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function NewSessionModal({
  onConfirm,
  onCancel,
}: {
  onConfirm: (title: string) => void;
  onCancel: () => void;
}) {
  const [title, setTitle] = useState("");
  return (
    <>
      <input
        className="new-session-input"
        placeholder="Give your session a title…"
        value={title}
        autoFocus
        onChange={(e) => setTitle(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") onConfirm(title.trim() || "New Session");
          if (e.key === "Escape") onCancel();
        }}
      />
      <div className="modal-actions">
        <button className="btn-ghost" onClick={onCancel}>Cancel</button>
        <button
          className="btn-primary"
          data-testid="new-session-btn"
          onClick={() => onConfirm(title.trim() || "New Session")}
        >
          Create
        </button>
      </div>
    </>
  );
}
