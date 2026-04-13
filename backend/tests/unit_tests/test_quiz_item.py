from datetime import datetime

from app.models.base import QuizItem, QuizRequest, SubmittedAnswer


class TestQuizItem:
    def test_create_helper_builds_quiz_item(self):
        item = QuizItem.create(
            quiz_request_id=1,
            question_text="What is a bot?",
            correct_answer="A software agent",
            answer_options={"A": "Human", "B": "Software agent"},
            difficulty="easy",
        )

        assert item.quiz_request_id == 1
        assert item.question_text == "What is a bot?"
        assert item.correct_answer == "A software agent"
        assert item.answer_options == {"A": "Human", "B": "Software agent"}
        assert item.difficulty == "easy"
        assert isinstance(item.created_at, datetime)
        assert item.submitted_answers == []

    def test_required_fields_are_non_nullable(self):
        text_field = QuizItem.model_fields["question_text"]
        answer_field = QuizItem.model_fields["correct_answer"]

        assert text_field.is_required()
        assert text_field.nullable is False
        assert answer_field.is_required()
        assert answer_field.nullable is False

    def test_relationship_with_submitted_answer_and_quiz_request(self):
        request = QuizRequest.create(session_id=1, topic="Math")
        item = QuizItem.create(
            quiz_request_id=1,
            question_text="2+2?",
            correct_answer="4",
        )
        answer = SubmittedAnswer.create(quiz_item_id=1, user_response="4")

        item.quiz_request = request
        request.quiz_items.append(item)
        answer.quiz_item = item
        item.submitted_answers.append(answer)

        assert item.quiz_request is request
        assert answer in item.submitted_answers
        assert answer.quiz_item is item
