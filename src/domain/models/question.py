from dataclasses import dataclass

from domain.models.question_answer import QuestionAnswer


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    body: str
    answers: list[QuestionAnswer]
    correct_answer: QuestionAnswer
