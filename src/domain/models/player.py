from dataclasses import dataclass


@dataclass
class Player:
    pk: int
    username: str

    def __hash__(self) -> int:
        return hash(self.pk)
