from sqlmodel import Session

from app.models.base import (
    UserSession,
    Message,
    Sender,
    QuizRequest,
    QuizItem,
    SubmittedAnswer,
    EvaluationResult,
)
from app.repositories.session_repository import SessionRepository


class ChatService:
    def __init__(self, session_repository: SessionRepository, db_session: Session, ai_provider):
        # The service uses a repository for session persistence and a
        # separate AI provider for generating responses and quiz data.
        self.session_repository = session_repository
        self.db_session = db_session
        self.ai_provider = ai_provider

    def start_session(self, title: str, user_identifier: str) -> UserSession:
        # Basic validation ensures the user provides a session title and id.
        if title is None or not title.strip():
            raise ValueError("Session title must not be empty.")
        if user_identifier is None or not user_identifier.strip():
            raise ValueError("User identifier must not be empty.")

        return self.session_repository.create_session(
            title=title.strip(),
            user_identifier=user_identifier.strip(),
        )

    def send_message(self, session_id: int, user_input: str) -> dict:
        if user_input is None or not user_input.strip():
            return {
                "success": False,
                "message": "User message cannot be empty.",
                "user_message": None,
                "ai_message": None,
                "response_type": None,
            }

        session_entity = self.session_repository.find_session_by_id(session_id)
        if session_entity is None:
            return {
                "success": False,
                "message": "The requested session was not found.",
                "user_message": None,
                "ai_message": None,
                "response_type": None,
            }

        # Record the user's message before asking the AI.
        user_message = self.session_repository.append_message(
            session_id=session_id,
            sender=Sender.USER,
            content=user_input.strip(),
        )

        # Send the cleaned user prompt to the AI provider and handle failures.
        try:
            ai_result = self.ai_provider.respond(prompt=user_input.strip())
            ai_content = ai_result.get("content", "")
            response_type = ai_result.get("type", "response")
        except RuntimeError:
            ai_content = "The AI service is currently unavailable. Please try again later."
            response_type = "fallback"

        ai_message = self.session_repository.append_message(
            session_id=session_id,
            sender=Sender.AI,
            content=ai_content,
        )

        return {
            "success": response_type != "fallback",
            "message": ai_content,
            "user_message": user_message,
            "ai_message": ai_message,
            "response_type": response_type,
        }

    def generate_quiz(self, session_id: int, topic: str) -> dict:
        if topic is None or not topic.strip():
            return {
                "success": False,
                "message": "Quiz topic cannot be empty.",
                "quiz_request": None,
                "quiz_items": [],
            }

        session_entity = self.session_repository.find_session_by_id(session_id)
        if session_entity is None:
            return {
                "success": False,
                "message": "The requested session was not found.",
                "quiz_request": None,
                "quiz_items": [],
            }

        # Request a quiz from the AI provider. If the provider fails, return a clear failure result but keep the session intact.
        try:
            ai_result = self.ai_provider.generate_quiz(topic=topic.strip())
            questions = ai_result.get("questions", [])
        except RuntimeError:
            return {
                "success": False,
                "message": "Unable to generate quiz at the moment.",
                "quiz_request": None,
                "quiz_items": [],
            }

        quiz_request = QuizRequest.create(session_id=session_id, topic=topic.strip())
        self.db_session.add(quiz_request)
        self.db_session.commit()
        self.db_session.refresh(quiz_request)

        quiz_items = []
        for question_item in questions:
            quiz_item = QuizItem.create(
                quiz_request_id=quiz_request.id,
                question_text=question_item["question_text"],
                correct_answer=question_item["correct_answer"],
                answer_options=question_item.get("answer_options"),
                difficulty=question_item.get("difficulty"),
            )
            self.db_session.add(quiz_item)
            self.db_session.commit()
            self.db_session.refresh(quiz_item)
            quiz_items.append(quiz_item)

        return {
            "success": True,
            "message": "Quiz generated successfully.",
            "quiz_request": quiz_request,
            "quiz_items": quiz_items,
        }

    def evaluate_answer(self, quiz_item: QuizItem, answer: str) -> dict:
        if answer is None or not answer.strip():
            return {
                "success": False,
                "message": "Please provide an answer.",
                "submitted_answer": None,
                "evaluation_result": None,
            }

        # Persist the user's answer before requesting evaluation.
        submitted_answer = SubmittedAnswer.create(
            quiz_item_id=quiz_item.id,
            user_response=answer.strip(),
        )
        self.db_session.add(submitted_answer)
        self.db_session.commit()
        self.db_session.refresh(submitted_answer)

        # Ask the AI provider to evaluate the answer against the correct one.
        evaluation = self.ai_provider.evaluate(
            question=quiz_item.question_text,
            answer=answer.strip(),
            correct_answer=quiz_item.correct_answer,
        )

        evaluation_result = EvaluationResult.create(
            submitted_answer_id=submitted_answer.id,
            is_correct=evaluation["is_correct"],
            feedback=evaluation["feedback"],
            explanation=evaluation.get("explanation"),
        )
        self.db_session.add(evaluation_result)
        self.db_session.commit()
        self.db_session.refresh(evaluation_result)

        return {
            "success": True,
            "message": "Answer evaluated successfully.",
            "submitted_answer": submitted_answer,
            "evaluation_result": evaluation_result,
        }
