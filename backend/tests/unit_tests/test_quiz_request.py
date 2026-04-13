from datetime import datetime

from app.models.base import QuizItem, QuizRequest, QuizStatus


class TestQuizRequest:
    def test_create_helper_builds_quiz_request(self):
        request = QuizRequest.create(session_id=1, topic="Python basics")

        assert request.session_id == 1
        assert request.topic == "Python basics"
        assert request.status == QuizStatus.PENDING
        assert isinstance(request.created_at, datetime)
        assert request.quiz_items == []

    def test_topic_is_required_and_non_nullable(self):
        topic_field = QuizRequest.model_fields["topic"]

        assert topic_field.is_required()
        assert topic_field.nullable is False

    def test_relationship_with_quiz_item_is_consistent(self):
        request = QuizRequest.create(session_id=1, topic="Testing")
        item = QuizItem.create(
            quiz_request_id=1,
            question_text="What is unit testing?",
            correct_answer="A way to verify a small piece of code",
        )

        item.quiz_request = request
        request.quiz_items.append(item)

        assert item in request.quiz_items
        assert item.quiz_request is request
