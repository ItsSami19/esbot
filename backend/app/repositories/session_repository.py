from typing import List, Optional

from sqlmodel import Session, select

from app.models.base import UserSession, Message, Sender


class SessionRepository:

    def __init__(self, session: Session) -> None:
        self._session = session

    # 1) Creating a new session
    def create_session(self, title: str, user_identifier: str) -> UserSession:
        session = UserSession(title=title, user_identifier=user_identifier)
        self._session.add(session)
        self._session.commit()
        self._session.refresh(session)
        return session

    # 2) Finding a session by ID
    def find_session_by_id(self, session_id: int) -> Optional[UserSession]:
        return self._session.get(UserSession, session_id)

    # 3) Finding sessions by user
    def find_sessions_by_user(self, user_identifier: str) -> List[UserSession]:
        statement = (
            select(UserSession)
            .where(UserSession.user_identifier == user_identifier)
            .order_by(UserSession.created_at)
        )
        results = self._session.exec(statement).all()
        return list(results)

    # 4) Appending a message to a session
    def append_message(
        self,
        session_id: int,
        sender: Sender,
        content: str,
    ) -> Message:
        session_obj = self.find_session_by_id(session_id)
        if session_obj is None:
            raise ValueError(f"Session with id {session_id} not found")

        statement = select(Message).where(Message.session_id == session_id)
        existing_messages = self._session.exec(statement).all()
        next_order = len(existing_messages) + 1

        message = Message.create(
            session_id=session_id,
            sender=sender,
            content=content,
            order=next_order,
        )
        self._session.add(message)
        self._session.commit()
        self._session.refresh(message)
        return message

    # 5) Retrieving the full message history of a session
    def get_message_history(self, session_id: int) -> List[Message]:
        statement = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.order)
        )
        results = self._session.exec(statement).all()
        return list(results)

    # 6) Updating session metadata (Titel + last_activity_at)
    def update_session_metadata(
        self,
        session_id: int,
        title: Optional[str] = None,
    ) -> Optional[UserSession]:
        session_obj = self.find_session_by_id(session_id)
        if session_obj is None:
            return None

        if title is not None:
            session_obj.title = title

        from app.models.base import utc_now

        session_obj.last_activity_at = utc_now()

        self._session.add(session_obj)
        self._session.commit()
        self._session.refresh(session_obj)
        return session_obj

    # 7) Deleting a session and all associated messages
    def delete_session(self, session_id: int) -> bool:
        session_obj = self.find_session_by_id(session_id)
        if session_obj is None:
            return False

        msg_stmt = select(Message).where(Message.session_id == session_id)
        messages = self._session.exec(msg_stmt).all()
        for msg in messages:
            self._session.delete(msg)

        self._session.delete(session_obj)
        self._session.commit()
        return True