from abc import ABC, abstractmethod
from collections import defaultdict

from infrastructure.ports.channels import Channel
from infrastructure.ports.websocket_connections import WebSocketConnection


class ChannelLayer(ABC):
    channels: defaultdict[str, set[Channel]] = defaultdict(set)

    @abstractmethod
    async def group_add(self, group: str, websocket: WebSocketConnection) -> None:
        pass

    @abstractmethod
    async def group_discard(self, group: str, websocket: WebSocketConnection) -> None:
        pass

    @abstractmethod
    async def group_send(self, group: str, message: str) -> None:
        pass
