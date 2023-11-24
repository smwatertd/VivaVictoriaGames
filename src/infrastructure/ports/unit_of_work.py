from abc import ABC, abstractmethod
from typing import Any, Generator

from domain.events import Event

from infrastructure.ports import repositories
from infrastructure.ports.producers import Producer


class UnitOfWork(ABC):
    games: repositories.GamesRepository
    players: repositories.PlayersRepository
    fields: repositories.FieldsRepository

    def __init__(self, event_producer: Producer) -> None:
        self._event_producer = event_producer

    async def __aenter__(self) -> 'UnitOfWork':
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    async def publish_events(self) -> None:
        for event in self._collect_events():
            await self._event_producer.publish(event)

    def _collect_events(self) -> Generator[Event, None, None]:
        for game in self.games.seen:
            for event in game.collect_events():
                yield event
