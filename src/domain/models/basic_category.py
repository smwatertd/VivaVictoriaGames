from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BasicCategory:
    id: int
