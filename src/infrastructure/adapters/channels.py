import asyncio

from infrastructure import ports
from infrastructure.adapters.messages import Message


class Channel:
    def __init__(
        self,
        id: str,
        websocket: ports.WebSocketConnection,
        chat_message_consumer: ports.Consumer,
    ) -> None:
        self._id = id
        self._websocket = websocket
        self._chat_message_consumer = chat_message_consumer
        self._listen_task: asyncio.Task | None = None

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Channel):
            return False
        return self._id == __value._id

    def __hash__(self) -> int:
        return hash(self._id)

    def get_id(self) -> str:
        return self._id

    async def subscribe(self, group: str) -> None:
        await self._chat_message_consumer.listen(group, self.send_message)

    async def unsubscribe(self) -> None:
        await self._chat_message_consumer.stop_listen()

    async def send_message(self, message: Message) -> None:
        await self._websocket.send({
            'type': message.type.value,
            'payload_type': message.payload_type,
            'payload': message.payload,
        })
