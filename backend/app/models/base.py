from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Sender(str, PyEnum):
    USER = "user"
    AI = "ai"


class SessionStatus(str, PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class QuizStatus(str, PyEnum):
    PENDING = "pending"
    GENERATED = "generated"
    COMPLETED = "completed"


class UserSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., nullable=False)
    created_at: datetime = Field(default_factory=utc_now)
    last_activity_at: datetime = Field(default_factory=utc_now)
    status: SessionStatus = Field(default=SessionStatus.ACTIVE)
    user_identifier: str = Field(..., nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="session")
    quiz_requests: List["QuizRequest"] = Relationship(back_populates="session")


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(..., foreign_key="usersession.id")
    sender: Sender = Field(...)
    content: str = Field(..., nullable=False)
    created_at: datetime = Field(default_factory=utc_now)
    order: int = Field(..., nullable=False)

    # Relationships
    session: UserSession = Relationship(back_populates="messages")

    @classmethod
    def create(cls, session_id: int, sender: Sender, content: str, order: int) -> "Message":
        return cls(session_id=session_id, sender=sender, content=content, order=order)


class QuizRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(..., foreign_key="usersession.id")
    topic: str = Field(..., nullable=False)
    created_at: datetime = Field(default_factory=utc_now)
    status: QuizStatus = Field(default=QuizStatus.PENDING)

    # Relationships
    session: UserSession = Relationship(back_populates="quiz_requests")
    quiz_items: List["QuizItem"] = Relationship(back_populates="quiz_request")

    @classmethod
    def create(cls, session_id: int, topic: str) -> "QuizRequest":
        return cls(session_id=session_id, topic=topic)


class QuizItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_request_id: int = Field(..., foreign_key="quizrequest.id")
    question_text: str = Field(..., nullable=False)
    answer_options: Optional[dict] = Field(default=None, sa_type=JSON)
    correct_answer: str = Field(..., nullable=False)
    difficulty: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    # Relationships
    quiz_request: QuizRequest = Relationship(back_populates="quiz_items")
    submitted_answers: List["SubmittedAnswer"] = Relationship(back_populates="quiz_item")

    @classmethod
    def create(cls, quiz_request_id: int, question_text: str, correct_answer: str, answer_options: Optional[dict] = None, difficulty: Optional[str] = None) -> "QuizItem":
        return cls(quiz_request_id=quiz_request_id, question_text=question_text, correct_answer=correct_answer, answer_options=answer_options, difficulty=difficulty)


class SubmittedAnswer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_item_id: int = Field(..., foreign_key="quizitem.id")
    user_response: str = Field(..., nullable=False)
    submitted_at: datetime = Field(default_factory=utc_now)

    # Relationships
    quiz_item: QuizItem = Relationship(back_populates="submitted_answers")
    evaluation_result: Optional["EvaluationResult"] = Relationship(back_populates="submitted_answer")

    @classmethod
    def create(cls, quiz_item_id: int, user_response: str) -> "SubmittedAnswer":
        return cls(quiz_item_id=quiz_item_id, user_response=user_response)


class EvaluationResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submitted_answer_id: int = Field(..., foreign_key="submittedanswer.id", unique=True)
    is_correct: bool = Field(..., nullable=False)
    feedback: str = Field(..., nullable=False)
    explanation: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    # Relationships
    submitted_answer: SubmittedAnswer = Relationship(back_populates="evaluation_result")

    @classmethod
    def create(cls, submitted_answer_id: int, is_correct: bool, feedback: str, explanation: Optional[str] = None) -> "EvaluationResult":
        return cls(submitted_answer_id=submitted_answer_id, is_correct=is_correct, feedback=feedback, explanation=explanation)