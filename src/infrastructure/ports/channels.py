from abc import ABC, abstractmethod

from infrastructure.ports.consumers import Consumer
from infrastructure.ports.websocket_connections import WebSocketConnection


class AbstractChannel(ABC):
    def __init__(
        self,
        websocket: WebSocketConnection,
        message_consumer: Consumer,
    ) -> None:
        self._websocket = websocket
        self._message_consumer = message_consumer

    @abstractmethod
    async def wait_for_message(self) -> None:
        pass

    @abstractmethod
    async def subscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, group: str) -> None:
        pass
