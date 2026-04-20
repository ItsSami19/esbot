from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app import models


def before_scenario(context, scenario):
    # Create a fresh in-memory test database for every scenario so all BDD scenarios remain independent
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(test_engine)

    context.engine = test_engine
    context.session = Session(test_engine)

    # placeholders used by step definitions
    context.ai_provider = None
    context.result = None
    context.response = None
    context.session_entity = None
    context.quiz_item = None
    context.quiz_request = None
    context.submitted_answer = None
    context.evaluation_result = None
    context.existing_messages = []
    context.requested_session_title = None


def after_scenario(context, scenario):
    # Clean up database session and schema after each scenario
    if hasattr(context, "session") and context.session is not None:
        context.session.close()

    if hasattr(context, "engine") and context.engine is not None:
        SQLModel.metadata.drop_all(context.engine)
        context.engine.dispose()