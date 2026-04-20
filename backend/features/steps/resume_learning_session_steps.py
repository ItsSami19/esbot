from behave import given, when, then

from app.models.base import UserSession, Message, Sender
from app.services.resume_learning_session_service import ResumeLearningSessionService


@given('a learning session with the title "{title}" exists')
def step_learning_session_exists(context, title):
    session_entity = UserSession(title=title, user_identifier="student-42")
    context.session.add(session_entity)
    context.session.commit()
    context.session.refresh(session_entity)

    context.session_entity = session_entity
    context.requested_session_title = title


@given('the session contains the previous message "{message_text}"')
def step_session_contains_previous_message(context, message_text):
    existing_messages = getattr(context, "existing_messages", [])
    next_order = len(existing_messages) + 1

    message = Message.create(
        session_id=context.session_entity.id,
        sender=Sender.USER,
        content=message_text,
        order=next_order,
    )
    context.session.add(message)
    context.session.commit()
    context.session.refresh(message)

    existing_messages.append(message)
    context.existing_messages = existing_messages


@given("no learning session exists for the requested session identifier")
def step_no_learning_session_exists(context):
    context.requested_session_title = "Non-existing Session"


@when("the student resumes the learning session")
def step_student_resumes_learning_session(context):
    service = ResumeLearningSessionService(context.session)
    context.result = service.resume_session(title=context.requested_session_title)


@when("the student tries to resume the learning session")
def step_student_tries_to_resume_learning_session(context):
    service = ResumeLearningSessionService(context.session)
    context.result = service.resume_session(title=context.requested_session_title)


@then("ESBot loads the existing learning session")
def step_esbot_loads_existing_learning_session(context):
    assert context.result is not None
    assert context.result["success"] is True
    assert context.result["session"] is not None
    assert context.result["session"].title == context.requested_session_title

@then('the previous message "{message_text}" is available')
def step_previous_message_is_available(context, message_text):
    messages = context.result["messages"]
    message_contents = [message.content for message in messages]

    assert message_text in message_contents


@then("ESBot returns a message that the session could not be found")
def step_session_could_not_be_found(context):
    assert context.result is not None
    assert context.result["success"] is False
    assert context.result["session"] is None
    assert context.result["message"] == "The session could not be found."