from abc import ABC, abstractmethod
from typing import AsyncIterator


class Consumer(ABC):
    @abstractmethod
    async def subscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, group: str) -> None:
        pass

    @abstractmethod
    def listen(self) -> AsyncIterator:
        pass
