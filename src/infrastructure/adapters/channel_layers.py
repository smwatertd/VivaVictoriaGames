from collections import defaultdict

from infrastructure.adapters.channels import RedisChannel
from infrastructure.adapters.producers import RedisProducer
from infrastructure.ports import ChannelLayer, WebSocketConnection


class RedisChannelLayer(ChannelLayer):
    channels: defaultdict[str, set[RedisChannel]] = defaultdict(set)
    producer: RedisProducer = RedisProducer()

    async def group_add(self, group: str, websocket: WebSocketConnection) -> None:
        channel = RedisChannel(websocket)
        await channel.subscribe(group)
        self.channels[group].add(channel)
        await channel.wait_for_message()

    async def group_discard(self, group: str, websocket: WebSocketConnection) -> None:
        for channel in self.channels[group]:
            if channel.websocket == websocket:
                await channel.unsubscribe(group)
                self.channels[group].remove(channel)
                break

    async def group_send(self, group: str, message: dict) -> None:
        await self.producer.publish(group, str(message))
