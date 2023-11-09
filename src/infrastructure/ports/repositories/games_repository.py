from abc import ABC, abstractmethod

from domain.models import Game


class GamesRepository(ABC):
    def __init__(self) -> None:
        self.seen: set[Game] = set()

    @abstractmethod
    async def get(self, pk: int) -> Game:
        pass
