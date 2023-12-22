from abc import ABC, abstractmethod
from typing import Callable


class Consumer(ABC):
    @abstractmethod
    async def listen(self, group: str, callback: Callable) -> None:
        pass

    @abstractmethod
    def stop_listen(self) -> None:
        pass
