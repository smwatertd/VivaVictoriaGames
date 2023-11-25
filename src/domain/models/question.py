from dataclasses import dataclass

from questions import Answer


@dataclass
class Question:
    _id: int
    _answers: list[Answer]
