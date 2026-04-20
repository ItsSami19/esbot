from behave import given, when, then

from app.models.base import UserSession, QuizRequest, QuizItem
from app.services.answer_evaluation_service import AnswerEvaluationService


class FakeAIProvider:
    def __init__(self, available: bool = True):
        self.available = available

    def evaluate(self, question: str, answer: str, correct_answer: str) -> dict:
        if not self.available:
            raise RuntimeError("AI provider is unavailable")

        if answer == correct_answer:
            return {
                "is_correct": True,
                "feedback": "Correct",
                "explanation": "2 + 2 equals 4.",
            }

        return {
            "is_correct": False,
            "feedback": "Incorrect",
            "explanation": "2 + 2 equals 4.",
        }


@given('a quiz question "{question}" with the correct answer "{correct_answer}" exists')
def step_quiz_question_exists(context, question, correct_answer):
    session_entity = UserSession(title="Quiz Session", user_identifier="student-42")
    context.session.add(session_entity)
    context.session.commit()
    context.session.refresh(session_entity)

    quiz_request = QuizRequest.create(session_id=session_entity.id, topic="Math")
    context.session.add(quiz_request)
    context.session.commit()
    context.session.refresh(quiz_request)

    quiz_item = QuizItem.create(
        quiz_request_id=quiz_request.id,
        question_text=question,
        correct_answer=correct_answer,
    )
    context.session.add(quiz_item)
    context.session.commit()
    context.session.refresh(quiz_item)

    context.session_entity = session_entity
    context.quiz_item = quiz_item


@given("the AI provider is available")
def step_ai_provider_is_available(context):
    context.ai_provider = FakeAIProvider(available=True)


@when('the student submits the answer "{answer}"')
def step_student_submits_answer(context, answer):
    service = AnswerEvaluationService(context.session, context.ai_provider)
    context.result = service.submit_answer(context.quiz_item, answer)


@when("the student submits an empty answer")
def step_student_submits_empty_answer(context):
    service = AnswerEvaluationService(context.session, context.ai_provider)
    context.result = service.submit_answer(context.quiz_item, "")


@then("ESBot marks the answer as correct")
def step_esbot_marks_answer_as_correct(context):
    assert context.result is not None
    assert context.result["success"] is True
    assert context.result["evaluation_result"] is not None
    assert context.result["evaluation_result"].is_correct is True


@then("ESBot marks the answer as incorrect")
def step_esbot_marks_answer_as_incorrect(context):
    assert context.result is not None
    assert context.result["success"] is True
    assert context.result["evaluation_result"] is not None
    assert context.result["evaluation_result"].is_correct is False


@then('ESBot returns the feedback "{feedback}"')
def step_esbot_returns_feedback(context, feedback):
    assert context.result["evaluation_result"] is not None
    assert context.result["evaluation_result"].feedback == feedback


@then('ESBot returns the explanation "{explanation}"')
def step_esbot_returns_explanation(context, explanation):
    assert context.result["evaluation_result"] is not None
    assert context.result["evaluation_result"].explanation == explanation


@then("ESBot returns a validation message asking for an answer")
def step_esbot_returns_validation_message_for_answer(context):
    assert context.result is not None
    assert context.result["success"] is False
    assert context.result["submitted_answer"] is None
    assert context.result["evaluation_result"] is None
    assert context.result["message"] == "Please provide an answer."