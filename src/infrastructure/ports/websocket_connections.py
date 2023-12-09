from abc import ABC, abstractmethod
from typing import Any


class WebSocketConnection(ABC):
    def __init__(self, websocket: Any) -> None:
        self.websocket = websocket

    @abstractmethod
    async def send(self, data: dict) -> None:
        pass
