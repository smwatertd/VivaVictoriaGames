from abc import ABC, abstractmethod

from infrastructure.adapters.messages import Message


class Producer(ABC):
    @abstractmethod
    async def publish(self, group: str, message: Message) -> None:
        pass
