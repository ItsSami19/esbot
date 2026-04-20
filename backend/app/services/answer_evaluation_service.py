from sqlmodel import Session

from app.models.base import SubmittedAnswer, EvaluationResult, QuizItem


class AnswerEvaluationService:
    def __init__(self, db_session: Session, ai_provider):
        self.db_session = db_session
        self.ai_provider = ai_provider

    def submit_answer(self, quiz_item: QuizItem, answer: str) -> dict:
        if answer is None or not answer.strip():
            return {
                "success": False,
                "message": "Please provide an answer.",
                "submitted_answer": None,
                "evaluation_result": None,
            }

        submitted_answer = SubmittedAnswer.create(
            quiz_item_id=quiz_item.id,
            user_response=answer,
        )
        self.db_session.add(submitted_answer)
        self.db_session.commit()
        self.db_session.refresh(submitted_answer)

        evaluation = self.ai_provider.evaluate(
            question=quiz_item.question_text,
            answer=answer,
            correct_answer=quiz_item.correct_answer,
        )

        evaluation_result = EvaluationResult.create(
            submitted_answer_id=submitted_answer.id,
            is_correct=evaluation["is_correct"],
            feedback=evaluation["feedback"],
            explanation=evaluation["explanation"],
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