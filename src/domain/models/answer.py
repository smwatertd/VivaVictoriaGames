from dataclasses import dataclass


@dataclass
class Answer:
    id: int
    is_correct: bool
