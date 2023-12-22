from abc import ABC, abstractmethod
from typing import Any, Generator

from core.settings import rabbitmq_settings

from domain.events import Event

from infrastructure.adapters.clients import CategoriesClient, QuestionsClient
from infrastructure.adapters.message_serializer import MessageSerializer
from infrastructure.ports import Producer, repositories


class UnitOfWork(ABC):
    games: repositories.GamesRepository
    players: repositories.PlayersRepository
    fields: repositories.FieldsRepository
    categories: CategoriesClient
    questions: QuestionsClient

    def __init__(
        self,
        event_producer: Producer,
        serializer: MessageSerializer,
    ) -> None:
        self._event_producer = event_producer
        self._serializer = serializer

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
            message = self._serializer.serialize(event)
            await self._event_producer.publish(rabbitmq_settings.games_events_queue, message)

    def _collect_events(self) -> Generator[Event, None, None]:
        if not hasattr(self, 'games'):
            return
        for game in self.games.seen:
            for event in game.collect_events():
                yield event
