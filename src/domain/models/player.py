from dataclasses import dataclass


@dataclass
class Player:
    _id: int
    _username: str

    def __hash__(self) -> int:
        return hash(self._id)
