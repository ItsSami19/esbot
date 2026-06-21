from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies import get_db_session
from app.api.schemas import (
    SessionCreate,
    SessionResponse,
    MessageCreate,
    MessageResponse,
    MessageListResponse,
    SubmitMessageResponse,
)
from app.models.base import Sender
from app.repositories.session_repository import SessionRepository

router = APIRouter(prefix="/sessions", tags=["sessions"])


def get_session_repository(db: Session) -> SessionRepository:
    return SessionRepository(db)

def generate_ai_reply(user_content: str) -> str:
    return f'Hello, your question was: "{user_content}"'

# 1) POST /api/v1/sessions
@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    payload: SessionCreate,
    db: Session = Depends(get_db_session),
):
    repo = get_session_repository(db)
    session_obj = repo.create_session(
        title=payload.title,
        user_identifier=payload.user_identifier,
    )
    return session_obj


# 2) GET /api/v1/sessions?user_identifier={id}
@router.get(
    "",
    response_model=List[SessionResponse],
)
def list_sessions(
    user_identifier: str,
    db: Session = Depends(get_db_session),
):
    repo = get_session_repository(db)
    sessions = repo.find_sessions_by_user(user_identifier)
    return sessions


# 3) GET /api/v1/sessions/{session_id}
@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db_session),
):
    repo = get_session_repository(db)
    session_obj = repo.find_session_by_id(session_id)
    if session_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return session_obj


# 4) DELETE /api/v1/sessions/{session_id}
@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db_session),
):
    repo = get_session_repository(db)
    deleted = repo.delete_session(session_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return None


# 5) POST /api/v1/sessions/{session_id}/messages
@router.post(
    "/{session_id}/messages",
    response_model=SubmitMessageResponse,   # <-- geändert
    status_code=status.HTTP_201_CREATED,
)
def submit_message(
    session_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db_session),
):
    repo = get_session_repository(db)
    session_obj = repo.find_session_by_id(session_id)
    if session_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    # 1) User-Nachricht speichern
    user_message = repo.append_message(
        session_id=session_id,
        sender=Sender.USER,
        content=payload.content,
    )

    # 2) Deterministische AI-Antwort generieren & speichern
    ai_reply_content = generate_ai_reply(payload.content)
    ai_message = repo.append_message(
        session_id=session_id,
        sender=Sender.AI,
        content=ai_reply_content,
    )

    # 3) Beide zurückgeben
    return SubmitMessageResponse(
        user_message=user_message,
        ai_message=ai_message,
    )


# 6) GET /api/v1/sessions/{session_id}/messages
@router.get(
    "/{session_id}/messages",
    response_model=MessageListResponse,
)
def get_session_history(
    session_id: int,
    db: Session = Depends(get_db_session),
):
    repo = get_session_repository(db)
    session_obj = repo.find_session_by_id(session_id)
    if session_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    history = repo.get_message_history(session_id)
    return MessageListResponse(messages=history)