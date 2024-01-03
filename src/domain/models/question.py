from dataclasses import dataclass

from domain.models.answer import Answer


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    body: str
    answers: list[Answer]
    correct_answer: Answer
