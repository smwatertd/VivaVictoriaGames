from importlib import import_module
from types import ModuleType

from domain import commands, events

from infrastructure.ports import Message, MessageType


events_module = import_module('domain.events')
commands_module = import_module('domain.commands')


class MessageParser:
    def parse(self, message: Message) -> events.Event | commands.Command:
        if message.get_message_type() == MessageType.EVENT:
            return self._parse(message, events_module)
        if message.get_message_type() == MessageType.COMMAND:
            return self._parse(message, commands_module)
        raise ValueError(f'Unknown message type: {message.get_message_type()}')

    def _parse(self, message: Message, module: ModuleType) -> events.Event | commands.Command:
        return getattr(module, message.get_payload_type())(**message.get_payload())
