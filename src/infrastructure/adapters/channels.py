import asyncio

from infrastructure.ports.consumers import Consumer
from infrastructure.ports.websocket_connections import WebSocketConnection


class Channel:
    def __init__(
        self,
        websocket: WebSocketConnection,
        message_consumer: Consumer,
    ) -> None:
        self._websocket = websocket
        self._message_consumer = message_consumer
        self._wait_for_message_task: asyncio.Task | None = None

    async def wait_for_message(self) -> None:
        self._wait_for_message_task = asyncio.ensure_future(self._wait_for_message())

    async def subscribe(self, group: str) -> None:
        await self._message_consumer.subscribe(group)

    async def unsubscribe(self, group: str) -> None:
        assert self._wait_for_message_task, 'wait_for_message must be called first'
        self._wait_for_message_task.cancel()
        await self._message_consumer.unsubscribe(group)

    async def _wait_for_message(self) -> None:
        async for message in self._message_consumer.listen():
            await self._websocket.send_bytes(message['data'])
