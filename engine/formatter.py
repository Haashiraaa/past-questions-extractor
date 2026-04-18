

# formatter.py

from engine.aliases import QuestionLike


class QuestionsFormatter:

    @staticmethod
    def format_question(question: QuestionLike) -> str:

        return (
            f"Subject: {question.get('subject')}\n\n"

            f"Question {question.get('number')}:\n"
            f"{question.get('question')}\n\n"

            f"Check answers here -> {question.get('answer_link')}\n"
        )
