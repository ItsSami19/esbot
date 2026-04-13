from datetime import datetime

from app.models.base import QuizItem, SubmittedAnswer, UserSession


class TestSubmittedAnswer:
    def test_create_helper_builds_submitted_answer(self):
        answer = SubmittedAnswer.create(quiz_item_id=1, user_response="Paris")

        assert answer.quiz_item_id == 1
        assert answer.user_response == "Paris"
        assert isinstance(answer.submitted_at, datetime)

    def test_user_response_is_required_and_non_nullable(self):
        response_field = SubmittedAnswer.model_fields["user_response"]

        assert response_field.is_required()
        assert response_field.nullable is False

    def test_relationship_with_quiz_item_is_consistent(self):
        item = QuizItem.create(
            quiz_request_id=1,
            question_text="Capital of France?",
            correct_answer="Paris",
        )
        answer = SubmittedAnswer.create(quiz_item_id=1, user_response="Paris")

        answer.quiz_item = item
        item.submitted_answers.append(answer)

        assert answer in item.submitted_answers
        assert answer.quiz_item is item
