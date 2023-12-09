import asyncio

from infrastructure import ports


class Channel(ports.AbstractChannel):
    def __init__(
        self,
        id: str,
        websocket: ports.WebSocketConnection,
        chat_message_consumer: ports.ChatMessageConsumer,
    ) -> None:
        super().__init__(id, websocket)
        self._chat_message_consumer = chat_message_consumer
        self._wait_for_message_task: asyncio.Task | None = None

    async def wait_for_message(self) -> None:
        self._wait_for_message_task = asyncio.ensure_future(self._wait_for_message())

    async def subscribe(self, group: str) -> None:
        await self._chat_message_consumer.subscribe(group)

    async def unsubscribe(self, group: str) -> None:
        if self._wait_for_message_task is None:
            raise ValueError('Channel is not subscribed')
        self._wait_for_message_task.cancel()
        await self._chat_message_consumer.unsubscribe(group)

    async def _wait_for_message(self) -> None:
        async for message in self._chat_message_consumer.listen():
            await self._websocket.send({
                'type': message.type.value,
                'payload_type': message.payload_type,
                'payload': message.payload,
            })
