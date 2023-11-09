from abc import ABC, abstractmethod

from domain.models import Player

from infrastructure.ports.repositories.repository import Repository


class PlayersRepository(Repository, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.seen: set[Player]

    @abstractmethod
    async def get(self, pk: int) -> Player:
        pass
