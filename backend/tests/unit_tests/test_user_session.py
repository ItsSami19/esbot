from datetime import datetime

from app.models.base import SessionStatus, UserSession


class TestUserSession:
    def test_can_create_with_valid_data(self):
        session = UserSession(title="Learning Session", user_identifier="student-42")

        assert session.id is None
        assert session.title == "Learning Session"
        assert session.user_identifier == "student-42"
        assert isinstance(session.created_at, datetime)
        assert isinstance(session.last_activity_at, datetime)
        assert session.status == SessionStatus.ACTIVE
        assert session.messages == []
        assert session.quiz_requests == []

    def test_title_is_required_and_non_nullable(self):
        title_field = UserSession.model_fields["title"]

        assert title_field.is_required()
        assert title_field.nullable is False
