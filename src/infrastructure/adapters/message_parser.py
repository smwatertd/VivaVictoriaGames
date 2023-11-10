from domain import commands, events

from infrastructure.ports import Message, MessageType


class MessageParser:
    events_factory = {
        'PlayerAdded': events.PlayerAdded,
        'PlayerRemoved': events.PlayerRemoved,
    }
    commands_factory = {
        'AddUser': commands.AddUser,
    }

    def parse(self, message: Message) -> events.Event | commands.Command:
        if message.get_message_type() == MessageType.EVENT:
            return self.events_factory[message.get_payload_type()](**message.get_payload())
        elif message.get_message_type() == MessageType.COMMAND:
            return self.commands_factory[message.get_payload_type()](**message.get_payload())
        else:
            raise ValueError('Unknown message type: ', message.get_message_type())
