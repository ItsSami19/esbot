from datetime import datetime

from app.repositories.session_repository import SessionRepository
from app.models.base import UserSession, Message, Sender


class TestSessionRepository:
    def test_create_and_find_session_by_id(self, session):
        repo = SessionRepository(session)

        created = repo.create_session(
            title="My first session",
            user_identifier="user-123",
        )

        assert created.id is not None
        assert created.title == "My first session"
        assert created.user_identifier == "user-123"

        found = repo.find_session_by_id(created.id)

        assert found is not None
        assert isinstance(found, UserSession)
        assert found.id == created.id
        assert found.title == "My first session"
        assert found.user_identifier == "user-123"

    def test_find_sessions_by_user_returns_all_in_order(self, session):
        repo = SessionRepository(session)

        s1 = repo.create_session("S1", "user-abc")
        s2 = repo.create_session("S2", "user-abc")
        _other = repo.create_session("Other", "other-user")

        sessions_for_user = repo.find_sessions_by_user("user-abc")

        assert [s.id for s in sessions_for_user] == [s1.id, s2.id]

    def test_append_message_and_get_history(self, session):
        repo = SessionRepository(session)
        user_session = repo.create_session("Chat", "user-1")

        m1 = repo.append_message(
            session_id=user_session.id,
            sender=Sender.USER,
            content="Hello",
        )
        m2 = repo.append_message(
            session_id=user_session.id,
            sender=Sender.AI,
            content="Hi there",
        )

        assert m1.id is not None
        assert m1.order == 1
        assert m2.order == 2

        history = repo.get_message_history(user_session.id)

        assert len(history) == 2
        assert [m.content for m in history] == ["Hello", "Hi there"]
        assert [m.order for m in history] == [1, 2]

    def test_append_message_raises_for_unknown_session(self, session):
        repo = SessionRepository(session)

        try:
            repo.append_message(
                session_id=9999,
                sender=Sender.USER,
                content="Should fail",
            )
            raised = False
        except ValueError:
            raised = True

        assert raised is True

    def test_update_session_metadata_changes_title_and_timestamp(self, session):
        repo = SessionRepository(session)
        user_session = repo.create_session("Old title", "user-1")

        old_last_activity = user_session.last_activity_at
        updated = repo.update_session_metadata(
            session_id=user_session.id,
            title="New title",
        )

        assert updated is not None
        assert updated.title == "New title"
        assert isinstance(updated.last_activity_at, datetime)
        assert updated.last_activity_at >= old_last_activity

    def test_update_session_metadata_returns_none_for_unknown_session(self, session):
        repo = SessionRepository(session)

        result = repo.update_session_metadata(session_id=9999, title="Does not matter")

        assert result is None

    def test_delete_session_removes_session_and_messages(self, session):
        repo = SessionRepository(session)
        user_session = repo.create_session("To delete", "user-1")

        repo.append_message(user_session.id, Sender.USER, "Hello")
        repo.append_message(user_session.id, Sender.AI, "Hi")

        deleted = repo.delete_session(user_session.id)
        assert deleted is True

        assert repo.find_session_by_id(user_session.id) is None
        history = repo.get_message_history(user_session.id)
        assert history == []

    def test_delete_session_returns_false_for_unknown_session(self, session):
        repo = SessionRepository(session)

        deleted = repo.delete_session(9999)

        assert deleted is False