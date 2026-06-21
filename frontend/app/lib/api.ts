const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export interface SessionResponse {
  id: number
  title: string
  created_at: string
  last_activity_at: string
  status: string
  user_identifier: string
}

export interface MessageResponse {
  id: number
  session_id: number
  sender: 'user' | 'ai'
  content: string
  created_at: string
  order: number
}

export interface SubmitMessageResponse {
  user_message: MessageResponse
  ai_message: MessageResponse
}

export interface MessageListResponse {
  messages: MessageResponse[]
}

export async function fetchHealth(): Promise<{ status: string }> {
  const res = await fetch(`${BASE_URL}/api/v1/health`)
  if (!res.ok) throw new Error('Health check failed')
  return res.json()
}

export async function createSession(
  title: string,
  user_identifier: string,
): Promise<SessionResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, user_identifier }),
  })
  if (!res.ok) throw new Error('Failed to create session')
  return res.json()
}

export async function listSessions(
  user_identifier: string,
): Promise<SessionResponse[]> {
  const res = await fetch(
    `${BASE_URL}/api/v1/sessions?user_identifier=${encodeURIComponent(user_identifier)}`,
  )
  if (!res.ok) throw new Error('Failed to list sessions')
  return res.json()
}

export async function getSession(session_id: number): Promise<SessionResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/sessions/${session_id}`)
  if (!res.ok) throw new Error('Session not found')
  return res.json()
}

export async function deleteSession(session_id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/v1/sessions/${session_id}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Failed to delete session')
}

export async function sendMessage(
  session_id: number,
  content: string,
): Promise<SubmitMessageResponse> {
  const res = await fetch(
    `${BASE_URL}/api/v1/sessions/${session_id}/messages`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender: 'user', content }),
    },
  )
  if (!res.ok) throw new Error('Failed to send message')
  return res.json()
}

export async function getMessageHistory(
  session_id: number,
): Promise<MessageListResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/sessions/${session_id}/messages`)
  if (!res.ok) throw new Error('Failed to fetch messages')
  return res.json()
}
