from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Answer:
    id: int
