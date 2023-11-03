import asyncio
from abc import ABC, abstractmethod

from infrastructure.ports.websocket_connections import WebSocketConnection


class Channel(ABC):
    def __init__(self, websocket: WebSocketConnection) -> None:
        self.websocket = websocket

    async def wait_for_message(self) -> None:
        asyncio.ensure_future(self._wait_for_message())

    @abstractmethod
    async def _wait_for_message(self) -> None:
        pass
