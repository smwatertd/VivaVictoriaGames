from abc import ABC, abstractmethod
from typing import Any


class WebSocketConnection(ABC):
    def __init__(self, websocket: Any) -> None:
        self.websocket = websocket

    @abstractmethod
    async def send_bytes(self, data: bytes) -> None:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WebSocketConnection):
            return False
        return self.websocket == other.websocket
