from behave import given, when, then

from app.models.base import UserSession
from app.services.contextualized_response_service import ContextualizedResponseService


class ExplanationAIProviderStub:
    def __init__(self, available: bool = True):
        self.available = available

    def explain(self, question: str) -> dict:
        if not self.available:
            raise RuntimeError("Explanation AI provider is unavailable")

        if question == "What is unit testing?":
            return {
                "type": "structured_explanation",
                "topic": "unit testing",
                "content": "Unit testing verifies small isolated parts of code.",
            }

        if question == "Can you explain this?":
            return {
                "type": "clarification",
                "content": "Please provide more context.",
            }

        return {
            "type": "structured_explanation",
            "topic": "unknown",
            "content": "No explanation is available.",
        }


@given("a student has an active learning session")
def step_student_has_active_learning_session(context):
    session_entity = UserSession(
        title="Learning Session",
        user_identifier="student-42",
    )
    context.session.add(session_entity)
    context.session.commit()
    context.session.refresh(session_entity)

    context.session_entity = session_entity


@given("the explanation AI provider is available")
def step_explanation_ai_provider_is_available(context):
    context.ai_provider = ExplanationAIProviderStub(available=True)


@given("the explanation AI provider is unavailable")
def step_explanation_ai_provider_is_unavailable(context):
    context.ai_provider = ExplanationAIProviderStub(available=False)


@when('the student asks the question "{question}"')
def step_student_asks_the_question(context, question):
    service = ContextualizedResponseService(context.session, context.ai_provider)
    context.result = service.ask_question(context.session_entity, question)


@then('ESBot returns a structured explanation about "{topic}"')
def step_esbot_returns_structured_explanation(context, topic):
    assert context.result is not None
    assert context.result["success"] is True
    assert context.result["response_type"] == "structured_explanation"
    assert context.result["topic"] == topic
    assert context.result["answer_message"] is not None


@then('the explanation contains the sentence "{sentence}"')
def step_explanation_contains_sentence(context, sentence):
    assert context.result["answer_message"] is not None
    assert sentence in context.result["answer_message"].content


@then("ESBot returns a clarification response")
def step_esbot_returns_clarification_response(context):
    assert context.result is not None
    assert context.result["success"] is True
    assert context.result["response_type"] == "clarification"
    assert context.result["answer_message"] is not None


@then("the response asks the student to provide more context")
def step_response_asks_for_more_context(context):
    assert context.result["answer_message"] is not None
    assert "Please provide more context." in context.result["answer_message"].content


@then("ESBot returns a fallback message")
def step_esbot_returns_fallback_message(context):
    assert context.result is not None
    assert context.result["success"] is False
    assert context.result["response_type"] == "fallback"
    assert context.result["answer_message"] is not None


@then('the response contains the message "{message}"')
def step_response_contains_message(context, message):
    assert context.result["answer_message"] is not None
    assert context.result["answer_message"].content == message