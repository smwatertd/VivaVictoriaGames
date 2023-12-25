from domain.events import Event

from infrastructure.adapters.messages import Message, MessageType
from infrastructure.ports.factory import Factory

from services.commands import Command
from services.exceptions import InvalidMessageType


class MessageSerializer:
    def __init__(self, event_factory: Factory, command_factory: Factory) -> None:
        self._event_factory = event_factory
        self._command_factory = command_factory

    def serialize(self, message: Event | Command) -> Message:
        if not isinstance(message, (Event, Command)):
            raise InvalidMessageType(type(message))
        return Message(
            type=MessageType.EVENT if isinstance(message, Event) else MessageType.COMMAND,
            payload_type=message.__class__.__name__,
            payload=message.model_dump(),
        )

    def deserialize(self, message: Message) -> Event | Command:
        if not isinstance(message, Message):
            raise InvalidMessageType(type(message))
        factory = self._event_factory if message.type == MessageType.EVENT else self._command_factory
        return factory.create(message.payload_type, **message.payload)
