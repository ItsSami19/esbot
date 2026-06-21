'use client'
import { useState, useCallback } from 'react'
import { MessageResponse, sendMessage, getMessageHistory } from '@/app/lib/api'

export function useChat(sessionId: number | null) {
  const [messages, setMessages] = useState<MessageResponse[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadHistory = useCallback(async (id: number) => {
    try {
      const data = await getMessageHistory(id)
      setMessages(data.messages)
    } catch {
      setError('Could not load message history.')
    }
  }, [])

  const submitMessage = useCallback(
    async (content: string) => {
      if (!sessionId) return
      setLoading(true)
      setError(null)

      const tempUserMsg: MessageResponse = {
        id: -1,
        session_id: sessionId,
        sender: 'user',
        content,
        created_at: new Date().toISOString(),
        order: messages.length + 1,
      }
      setMessages((prev) => [...prev, tempUserMsg])

      try {
        const res = await sendMessage(sessionId, content)
        setMessages((prev) => [
          ...prev.filter((m) => m.id !== -1),
          res.user_message,
          res.ai_message,
        ])
      } catch {
        setMessages((prev) => prev.filter((m) => m.id !== -1))
        setError('Failed to send message. Please try again.')
      } finally {
        setLoading(false)
      }
    },
    [sessionId, messages.length],
  )

  return { messages, loading, error, loadHistory, submitMessage, setMessages }
}
