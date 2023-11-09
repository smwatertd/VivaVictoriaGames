from abc import ABC, abstractmethod


class Producer(ABC):
    @abstractmethod
    async def publish(self, group: str, data: dict[str, str]) -> None:
        pass
