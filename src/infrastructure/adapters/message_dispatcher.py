from infrastructure.adapters.message_parser import MessageParser
from infrastructure.ports import Consumer, UnitOfWork

from services.messagebus import MessageBus


class MessageDispatcher:
    def __init__(
        self,
        consumer: Consumer,
        parser: MessageParser,
        messagebus: MessageBus,
    ) -> None:
        self._consumer = consumer
        self._parser = parser
        self._messagebus = messagebus

    async def start(self, unit_of_work: UnitOfWork) -> None:
        async for message in self._consumer.listen():
            result = self._parser.parse(message)
            await self._messagebus.handle(result, unit_of_work)
