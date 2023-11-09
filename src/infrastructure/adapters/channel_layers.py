from collections import defaultdict
from typing import Type

from infrastructure.adapters.channels import Channel
from infrastructure.ports.consumers import Consumer
from infrastructure.ports.websocket_connections import WebSocketConnection


class ChannelLayer:
    channels: defaultdict[str, set[Channel]] = defaultdict(set)

    def __init__(self, consumer_factory: Type[Consumer]) -> None:
        self._consumer_factory = consumer_factory

    async def group_add(self, group: str, websocket: WebSocketConnection) -> None:
        channel = Channel(websocket, self._consumer_factory())
        self._add_channel(group, channel)
        await channel.subscribe(group)
        await channel.wait_for_message()

    async def group_discard(self, group: str, websocket: WebSocketConnection) -> None:
        channel = self._get_channel(group, websocket)
        await channel.unsubscribe(group)
        self._remove_channel(group, channel)

    def _add_channel(self, group: str, channel: Channel) -> None:
        self.channels[group].add(channel)

    def _remove_channel(self, group: str, channel: Channel) -> None:
        self.channels[group].remove(channel)

    def _get_channel(self, group: str, websocket: WebSocketConnection) -> Channel:
        for channel in self.channels[group]:
            if channel._websocket == websocket:
                return channel
