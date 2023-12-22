from infrastructure.adapters.message_serializer import MessageSerializer
from infrastructure.adapters.messages import Message
from infrastructure.ports import Consumer

from services.messagebus import MessageBus


class MessageHandler:
    def __init__(
        self,
        consumer: Consumer,
        messagebus: MessageBus,
        serializer: MessageSerializer,
    ) -> None:
        self._consumer = consumer
        self._messagebus = messagebus
        self._serializer = serializer

    async def start(self, group: str) -> None:
        await self._consumer.listen(group, self.handle)

    async def handle(self, message: Message) -> None:
        await self._messagebus.handle(self._serializer.deserialize(message))
