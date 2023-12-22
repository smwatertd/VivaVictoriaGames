from infrastructure.adapters import Message, MessageSerializer
from infrastructure.ports import UnitOfWork

from services.messagebus import MessageBus


class MessageHandler:
    def __init__(self, messagebus: MessageBus, serializer: MessageSerializer, unit_of_work: UnitOfWork) -> None:
        self._messagebus = messagebus
        self._serializer = serializer
        self._unit_of_work = unit_of_work

    async def handle(self, message: Message) -> None:
        await self._messagebus.handle(self._serializer.deserialize(message), self._unit_of_work)
