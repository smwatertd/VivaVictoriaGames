from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PlayerAnswer:
    id: int
