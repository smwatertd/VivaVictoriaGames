from abc import ABC, abstractmethod

from infrastructure.ports.websocket_connections import WebSocketConnection


class AbstractChannel(ABC):
    def __init__(self, id: str, websocket: WebSocketConnection) -> None:
        self._id = id
        self._websocket = websocket

    @abstractmethod
    async def wait_for_message(self) -> None:
        pass

    @abstractmethod
    async def subscribe(self, group: str) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, group: str) -> None:
        pass

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, AbstractChannel):
            return False
        return self._id == __value._id

    def __hash__(self) -> int:
        return hash(self._id)
