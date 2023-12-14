from abc import ABC, abstractmethod
from typing import AsyncIterator

from infrastructure.adapters.messages import Message


class MessageConsumer(ABC):
    @abstractmethod
    async def listen(self, group: str) -> AsyncIterator[Message]:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass


class ChatMessageConsumer(ABC):
    @abstractmethod
    async def subscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def listen(self) -> AsyncIterator[Message]:
        pass
