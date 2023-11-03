from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    pk: int
