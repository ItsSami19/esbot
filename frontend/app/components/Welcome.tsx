"use client";

interface WelcomeProps {
  onNew: () => void;
}

export default function Welcome({ onNew }: WelcomeProps) {
  return (
    <div className="welcome">
      <div className="welcome-inner">
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none" aria-label="ESBot logo large">
          <rect width="56" height="56" rx="14" fill="#01696f" />
          <text x="8" y="38" fontSize="26" fontWeight="700" fill="white" fontFamily="monospace">ES</text>
        </svg>
        <h1 className="welcome-title">ESBot</h1>
        <p className="welcome-sub">Your AI learning assistant. Select a session or create a new one.</p>
        <button className="btn-primary welcome-btn" onClick={onNew} data-testid="new-session-btn">
          New Session
        </button>
      </div>
    </div>
  );
}
