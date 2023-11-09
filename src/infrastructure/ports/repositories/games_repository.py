from abc import ABC, abstractmethod

from domain.models import Game

from infrastructure.ports.repositories.repository import Repository


class GamesRepository(Repository, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.seen: set[Game]

    @abstractmethod
    async def get(self, pk: int) -> Game:
        pass
