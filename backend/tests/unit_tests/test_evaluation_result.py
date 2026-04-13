from datetime import datetime

from app.models.base import EvaluationResult, SubmittedAnswer


class TestEvaluationResult:
    def test_create_helper_builds_evaluation_result(self):
        result = EvaluationResult.create(
            submitted_answer_id=1,
            is_correct=True,
            feedback="Correct",
            explanation="This is the expected answer.",
        )

        assert result.submitted_answer_id == 1
        assert result.is_correct is True
        assert result.feedback == "Correct"
        assert result.explanation == "This is the expected answer."
        assert isinstance(result.created_at, datetime)

    def test_feedback_is_required_and_non_nullable(self):
        feedback_field = EvaluationResult.model_fields["feedback"]

        assert feedback_field.is_required()
        assert feedback_field.nullable is False

    def test_relationship_with_submitted_answer_is_consistent(self):
        answer = SubmittedAnswer.create(quiz_item_id=1, user_response="42")
        result = EvaluationResult.create(
            submitted_answer_id=1,
            is_correct=False,
            feedback="Incorrect",
        )

        result.submitted_answer = answer
        answer.evaluation_result = result

        assert answer.evaluation_result is result
        assert result.submitted_answer is answer
