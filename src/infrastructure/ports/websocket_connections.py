from abc import ABC, abstractmethod
from typing import Any


class WebSocketConnection(ABC):
    def __init__(self, websocket: Any) -> None:
        self.websocket = websocket

    @abstractmethod
    async def send_json(self, data: Any) -> None:
        # TODO: Fix data type annotation
        pass
