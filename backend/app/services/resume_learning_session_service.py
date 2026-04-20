from typing import Optional

from sqlmodel import Session, select

from app.models.base import UserSession, Message


class ResumeLearningSessionService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def resume_session(self, title: Optional[str] = None, session_id: Optional[int] = None) -> dict:
        statement = None

        if session_id is not None:
            statement = select(UserSession).where(UserSession.id == session_id)
        elif title is not None:
            statement = select(UserSession).where(UserSession.title == title)
        else:
            return {
                "success": False,
                "message": "No session identifier was provided.",
                "session": None,
                "messages": [],
            }

        session_entity = self.db_session.exec(statement).first()

        if session_entity is None:
            return {
                "success": False,
                "message": "The session could not be found.",
                "session": None,
                "messages": [],
            }

        messages = self.db_session.exec(
            select(Message)
            .where(Message.session_id == session_entity.id)
            .order_by(Message.order)
        ).all()

        return {
            "success": True,
            "message": "The learning session was loaded successfully.",
            "session": session_entity,
            "messages": messages,
        }