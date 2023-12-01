from dataclasses import dataclass

from questions import Answer


@dataclass(frozen=True, slots=True)
class Question:
    id: int
    answers: list[Answer]
