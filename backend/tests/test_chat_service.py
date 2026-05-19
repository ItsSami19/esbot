from unittest.mock import Mock

import pytest
from app.models.base import Message, Sender, QuizItem, UserSession
from app.repositories.session_repository import SessionRepository
from app.services.chat_service import ChatService


class TestChatService:

    def test_start_session_creates_new_session(self):
        # Arrange
        session_repository = Mock(spec=SessionRepository)
        session_repository.create_session.return_value = UserSession(
            id=1,
            title="New Session",
            user_identifier="user-1",
        )
        service = ChatService(session_repository, db_session=Mock(), ai_provider=Mock())

        # Act
        session = service.start_session(title="New Session", user_identifier="user-1")

        # Assert
        assert session.id == 1
        assert session.title == "New Session"
        assert session.user_identifier == "user-1"
        session_repository.create_session.assert_called_once_with(
            title="New Session",
            user_identifier="user-1",
        )

    def test_send_message_stores_user_and_ai_messages(self):
        # Arrange
        session_repository = Mock(spec=SessionRepository)
        session_repository.find_session_by_id.return_value = UserSession(id=1, title="Chat", user_identifier="user-1")
        session_repository.append_message.side_effect = [
            Message.create(session_id=1, sender=Sender.USER, content="Hello", order=1),
            Message.create(session_id=1, sender=Sender.AI, content="Hello from AI", order=2),
        ]
        ai_provider = Mock()
        ai_provider.respond.return_value = {"content": "Hello from AI", "type": "response"}
        service = ChatService(session_repository, db_session=Mock(), ai_provider=ai_provider)

        # Act
        result = service.send_message(session_id=1, user_input="Hello")

        # Assert
        assert result["success"] is True
        assert result["response_type"] == "response"
        assert result["ai_message"].content == "Hello from AI"
        assert result["user_message"].content == "Hello"
        session_repository.find_session_by_id.assert_called_once_with(1)
        session_repository.append_message.assert_any_call(
            session_id=1, sender=Sender.USER, content="Hello",
        )
        session_repository.append_message.assert_any_call(
            session_id=1, sender=Sender.AI, content="Hello from AI",
        )

    def test_send_message_returns_fallback_when_ai_provider_fails(self):
        # Arrange: AI provider raises an error to simulate unavailability
        session_repository = Mock(spec=SessionRepository)
        session_repository.find_session_by_id.return_value = UserSession(id=1, title="Chat", user_identifier="user-1")
        session_repository.append_message.side_effect = [
            Message.create(session_id=1, sender=Sender.USER, content="Hello", order=1),
            Message.create(session_id=1, sender=Sender.AI, content="The AI service is currently unavailable. Please try again later.", order=2),
        ]
        ai_provider = Mock()
        ai_provider.respond.side_effect = RuntimeError("Service unavailable")
        service = ChatService(session_repository, db_session=Mock(), ai_provider=ai_provider)

        # Act
        result = service.send_message(session_id=1, user_input="Hello")

        # Assert: service returns a fallback response instead of crashing
        assert result["success"] is False
        assert result["response_type"] == "fallback"
        assert "unavailable" in result["message"]
        session_repository.append_message.assert_called_with(
            session_id=1,
            sender=Sender.AI,
            content="The AI service is currently unavailable. Please try again later.",
        )

    def test_generate_quiz_persists_quiz_request_and_items(self, session):
        # Arrange
        session_repository = Mock(spec=SessionRepository)
        session_repository.find_session_by_id.return_value = UserSession(id=1, title="Quiz", user_identifier="user-1")
        ai_provider = Mock()
        ai_provider.generate_quiz.return_value = {
            "questions": [
                {
                    "question_text": "What is the capital of France?",
                    "correct_answer": "Paris",
                    "answer_options": {"A": "Paris", "B": "Berlin", "C": "Rome"},
                    "difficulty": "easy",
                }
            ]
        }
        service = ChatService(session_repository, db_session=session, ai_provider=ai_provider)

        # Act
        result = service.generate_quiz(session_id=1, topic="European capitals")

        # Assert
        assert result["success"] is True
        assert result["quiz_request"] is not None
        assert result["quiz_items"]
        assert result["quiz_items"][0].question_text == "What is the capital of France?"
        assert result["quiz_items"][0].correct_answer == "Paris"
        ai_provider.generate_quiz.assert_called_once_with(topic="European capitals")

    def test_generate_quiz_returns_failure_when_ai_service_unavailable(self, session):
        # Arrange: AI provider raises an error to simulate a timeout
        session_repository = Mock(spec=SessionRepository)
        session_repository.find_session_by_id.return_value = UserSession(id=1, title="Quiz", user_identifier="user-1")
        ai_provider = Mock()
        ai_provider.generate_quiz.side_effect = RuntimeError("AI timeout")
        service = ChatService(session_repository, db_session=session, ai_provider=ai_provider)

        # Act
        result = service.generate_quiz(session_id=1, topic="European capitals")

        # Assert: no quiz data is returned on failure
        assert result["success"] is False
        assert result["quiz_request"] is None
        assert result["quiz_items"] == []

    def test_evaluate_answer_submits_answer_and_returns_feedback(self, session):
        # Arrange
        ai_provider = Mock()
        ai_provider.evaluate.return_value = {
            "is_correct": True,
            "feedback": "Great work!",
            "explanation": "Paris is the capital of France.",
        }
        quiz_item = QuizItem(
            id=1,
            quiz_request_id=1,
            question_text="What is the capital of France?",
            correct_answer="Paris",
        )
        service = ChatService(Mock(), db_session=session, ai_provider=ai_provider)

        # Act
        result = service.evaluate_answer(quiz_item=quiz_item, answer="Paris")

        # Assert
        assert result["success"] is True
        assert result["evaluation_result"].is_correct is True
        assert result["evaluation_result"].feedback == "Great work!"
        assert result["submitted_answer"].user_response == "Paris"
        ai_provider.evaluate.assert_called_once_with(
            question="What is the capital of France?",
            answer="Paris",
            correct_answer="Paris",
        )

    def test_evaluate_answer_rejects_empty_answer(self):
        # Arrange
        service = ChatService(Mock(), db_session=Mock(), ai_provider=Mock())

        # Act: whitespace-only answer should be treated as empty
        result = service.evaluate_answer(
            quiz_item=QuizItem(
                id=1,
                quiz_request_id=1,
                question_text="Question?",
                correct_answer="Answer",
            ),
            answer="  ",
        )

        # Assert: validation rejects the answer before any persistence
        assert result["success"] is False
        assert result["submitted_answer"] is None
        assert result["evaluation_result"] is None