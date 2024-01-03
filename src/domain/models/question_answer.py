from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class QuestionAnswer:
    id: int
    body: str
