"use client";
import { useState, useCallback } from "react";
import { SessionResponse, listSessions, createSession, deleteSession } from "@/app/lib/api";

export const DEFAULT_USER = "esbot-user";

export function useSessions() {
  const [sessions, setSessions] = useState<SessionResponse[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const data = await listSessions(DEFAULT_USER);
      setSessions(data);
    } catch {
      setError("Could not load sessions.");
    }
  }, []);

  const create = useCallback(async (title: string) => {
    try {
      const s = await createSession(title, DEFAULT_USER);
      setSessions((prev) => [...prev, s]);
      return s;
    } catch {
      setError("Could not create session.");
      return null;
    }
  }, []);

  const remove = useCallback(async (id: number) => {
    try {
      await deleteSession(id);
      setSessions((prev) => prev.filter((s) => s.id !== id));
    } catch {
      setError("Could not delete session.");
    }
  }, []);

  return { sessions, error, load, create, remove };
}
