

# aliases.py

from typing import List, TypedDict, Optional


class QuestionLike(TypedDict):
    exam_year: Optional[str]
    subject: Optional[str]
    number: Optional[str]
    question: Optional[str]
    images: List[Optional[str]]
    answer_link: Optional[str]
