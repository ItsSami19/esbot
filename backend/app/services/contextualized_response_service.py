from sqlmodel import Session, select

from app.models.base import Message, Sender, UserSession


class ContextualizedResponseService:
    def __init__(self, db_session: Session, ai_provider):
        self.db_session = db_session
        self.ai_provider = ai_provider

    def ask_question(self, session_entity: UserSession, question: str) -> dict:
        if session_entity is None:
            return {
                "success": False,
                "message": "No active learning session was found.",
                "question_message": None,
                "answer_message": None,
                "response_type": None,
            }

        existing_messages = self.db_session.exec(
            select(Message).where(Message.session_id == session_entity.id)
        ).all()

        question_message = Message.create(
            session_id=session_entity.id,
            sender=Sender.USER,
            content=question,
            order=len(existing_messages) + 1,
        )
        self.db_session.add(question_message)
        self.db_session.commit()
        self.db_session.refresh(question_message)

        try:
            ai_result = self.ai_provider.explain(question)
        except RuntimeError:
            fallback_text = "The explanation could not be generated at the moment. Please try again later."

            answer_message = Message.create(
                session_id=session_entity.id,
                sender=Sender.AI,
                content=fallback_text,
                order=len(existing_messages) + 2,
            )
            self.db_session.add(answer_message)
            self.db_session.commit()
            self.db_session.refresh(answer_message)

            return {
                "success": False,
                "message": fallback_text,
                "question_message": question_message,
                "answer_message": answer_message,
                "response_type": "fallback",
            }

        answer_message = Message.create(
            session_id=session_entity.id,
            sender=Sender.AI,
            content=ai_result["content"],
            order=len(existing_messages) + 2,
        )
        self.db_session.add(answer_message)
        self.db_session.commit()
        self.db_session.refresh(answer_message)

        return {
            "success": True,
            "message": "Explanation generated successfully.",
            "question_message": question_message,
            "answer_message": answer_message,
            "response_type": ai_result["type"],
            "topic": ai_result.get("topic"),
        }