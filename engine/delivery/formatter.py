

# formatter.py

from typing import cast
from engine.models.aliases import QuestionLike


class QuestionsFormatter:

    @staticmethod
    def format_question(question: QuestionLike) -> str:

        subject = cast(str, question.get("subject")).capitalize()

        return (
            f"Subject: {subject}\n\n"

            f"Question {question.get('number')}:\n"
            f"{question.get('question')}\n\n"

            f"Check answers here -> {question.get('answer_link')}\n"
        )
