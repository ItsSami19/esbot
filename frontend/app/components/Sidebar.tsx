'use client'
import { useState } from 'react'
import { SessionResponse } from '@/app/lib/api'

interface SidebarProps {
  sessions: SessionResponse[]
  activeSessionId: number | null
  onSelect: (id: number) => void
  onCreate: (title: string) => void
  onDelete: (id: number) => void
  healthStatus: 'ok' | 'error' | 'loading'
}

export default function Sidebar({
  sessions,
  activeSessionId,
  onSelect,
  onCreate,
  onDelete,
  healthStatus,
}: SidebarProps) {
  const [newTitle, setNewTitle] = useState('')
  const [creating, setCreating] = useState(false)

  const handleCreate = () => {
    const title = newTitle.trim() || `Session ${sessions.length + 1}`
    onCreate(title)
    setNewTitle('')
    setCreating(false)
  }

  const healthColor =
    healthStatus === 'ok'
      ? '#10b981'
      : healthStatus === 'error'
        ? '#ef4444'
        : '#facc15'

  return (
    <aside className='sidebar'>
      {/* Header */}
      <div className='sidebar-header'>
        <div className='sidebar-logo'>
          <svg
            width='28'
            height='28'
            viewBox='0 0 28 28'
            fill='none'
            aria-label='ESBot logo'
          >
            <rect width='28' height='28' rx='7' fill='#01696f' />
            <text
              x='5'
              y='20'
              fontSize='14'
              fontWeight='700'
              fill='white'
              fontFamily='monospace'
            >
              ES
            </text>
          </svg>
          <span className='sidebar-title'>ESBot</span>
        </div>
        <div
          data-testid='health-status'
          title={`API ${healthStatus}`}
          className='health-dot'
          style={{ backgroundColor: healthColor }}
        />
      </div>

      {/* New Session */}
      <div className='sidebar-new'>
        {creating ? (
          <div className='new-session-form'>
            <input
              className='new-session-input'
              placeholder='Session title…'
              value={newTitle}
              autoFocus
              onChange={(e) => setNewTitle(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleCreate()
                if (e.key === 'Escape') setCreating(false)
              }}
            />
            <button
              className='btn-primary'
              onClick={handleCreate}
              data-testid='new-session-btn'
            >
              Create
            </button>
          </div>
        ) : (
          <button
            className='btn-new-session'
            onClick={() => setCreating(true)}
            data-testid='new-session-btn'
          >
            <svg
              width='16'
              height='16'
              viewBox='0 0 16 16'
              fill='none'
              stroke='currentColor'
              strokeWidth='2'
            >
              <path d='M8 3v10M3 8h10' strokeLinecap='round' />
            </svg>
            New Session
          </button>
        )}
      </div>

      {/* Session List */}
      <nav className='session-list' data-testid='session-list'>
        {sessions.length === 0 && (
          <div className='session-empty'>No sessions yet</div>
        )}
        {sessions.map((s) => (
          <div
            key={s.id}
            data-testid={`session-item-${s.id}`}
            className={`session-item ${activeSessionId === s.id ? 'active' : ''}`}
            onClick={() => onSelect(s.id)}
          >
            <span className='session-item-title'>{s.title}</span>
            <button
              className='session-delete-btn'
              onClick={(e) => {
                e.stopPropagation()
                onDelete(s.id)
              }}
              aria-label={`Delete session ${s.title}`}
              title='Delete'
            >
              <svg
                width='14'
                height='14'
                viewBox='0 0 16 16'
                fill='none'
                stroke='currentColor'
                strokeWidth='2'
              >
                <path d='M3 3l10 10M13 3L3 13' strokeLinecap='round' />
              </svg>
            </button>
          </div>
        ))}
      </nav>
    </aside>
  )
}
