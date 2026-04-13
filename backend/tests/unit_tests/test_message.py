from datetime import datetime

from app.models.base import Message, Sender, UserSession


class TestMessage:
    def test_create_helper_builds_message(self):
        message = Message.create(session_id=1, sender=Sender.USER, content="Hello", order=1)

        assert message.session_id == 1
        assert message.sender == Sender.USER
        assert message.content == "Hello"
        assert message.order == 1
        assert isinstance(message.created_at, datetime)

    def test_content_is_required_and_non_nullable(self):
        content_field = Message.model_fields["content"]

        assert content_field.is_required()
        assert content_field.nullable is False

    def test_relationship_with_user_session_is_consistent(self):
        user_session = UserSession(title="Chat", user_identifier="student-42")
        message = Message.create(session_id=1, sender=Sender.USER, content="First message", order=1)

        message.session = user_session
        user_session.messages.append(message)

        assert message in user_session.messages
        assert message.session is user_session
