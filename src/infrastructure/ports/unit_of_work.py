from abc import ABC, abstractmethod
from typing import Any, Generator

from domain.events import Event

from infrastructure.ports import repositories
from infrastructure.ports.producers import Producer


class UnitOfWork(ABC):
    def __init__(
        self,
        games: repositories.GamesRepository,
        players: repositories.PlayersRepository,
        fields: repositories.FieldsRepository,
        event_producer: Producer,
        message_producer: Producer,
    ) -> None:
        self.games = games
        self.players = players
        self.fields = fields
        self._event_producer = event_producer
        self.message_producer = message_producer

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
