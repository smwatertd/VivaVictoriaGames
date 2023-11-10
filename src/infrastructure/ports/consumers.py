from abc import ABC, abstractmethod
from typing import AsyncGenerator

from infrastructure.ports.messages import Message


class Consumer(ABC):
    @abstractmethod
    async def subscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def listen(self) -> AsyncGenerator[Message, None]:
        pass
