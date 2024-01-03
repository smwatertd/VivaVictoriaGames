from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Category:
    id: int
    name: str
