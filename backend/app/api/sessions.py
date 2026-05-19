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
)
from app.models.base import Sender
from app.repositories.session_repository import SessionRepository

router = APIRouter(prefix="/sessions", tags=["sessions"])


def get_session_repository(db: Session) -> SessionRepository:
    return SessionRepository(db)


# 1) Session creation endpoint (POST /sessions)
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


# 2) Session listing endpoint (GET /sessions)
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


# 3) Session history retrieval endpoint (GET /sessions/{session_id}/messages)
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


# 4) Message submission endpoint (POST /sessions/{session_id}/messages)
@router.post(
    "/{session_id}/messages",
    response_model=MessageResponse,
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

    message = repo.append_message(
        session_id=session_id,
        sender=payload.sender,
        content=payload.content,
    )

    return message


# 5) Session deletion endpoint (DELETE /sessions/{session_id})
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