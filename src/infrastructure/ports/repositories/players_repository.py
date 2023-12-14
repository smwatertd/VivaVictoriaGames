from abc import ABC, abstractmethod

from domain.models import Player

from infrastructure.ports.repositories.repository import Repository


class PlayersRepository(Repository, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.seen: set[Player]

    @abstractmethod
    async def add(self, player: Player) -> None:
        pass

    @abstractmethod
    async def get(self, id: int) -> Player:
        pass

    @abstractmethod
    async def get_or_create(self, id: int, username: str) -> Player:
        pass
