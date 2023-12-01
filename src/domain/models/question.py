from dataclasses import dataclass

from domain.models.answer import Answer


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    answers: list[Answer]
