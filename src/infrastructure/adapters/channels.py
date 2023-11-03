from infrastructure.adapters.consumers import RedisConsumer
from infrastructure.ports import Channel, WebSocketConnection


class RedisChannel(Channel):
    def __init__(self, websocket: WebSocketConnection) -> None:
        super().__init__(websocket)
        self.consumer = RedisConsumer(self._wait_for_message)

    async def _wait_for_message(self) -> None:
        async for message in self.consumer.pubsub.listen():
            # TODO: Fix this
            try:
                await self.websocket.send_json(str(message))
            except RuntimeError:
                pass

    async def subscribe(self, group: str) -> None:
        await self.consumer.subscribe(group)

    async def unsubscribe(self, group: str) -> None:
        await self.consumer.unsubscribe(group)
