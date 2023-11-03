from abc import ABC, abstractmethod
from typing import Any

from infrastructure.ports.repositories import GamesRepository


class UnitOfWork(ABC):
    def __init__(
        self,
        games: GamesRepository,
    ) -> None:
        self.games = games

    async def __aenter__(self) -> 'UnitOfWork':
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # TODO: Fix type annotations
        await self.rollback()

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def publish_events(self) -> None:
        pass
