from domain.events import Event

from entrypoints.commands import Command

from infrastructure.adapters import Message, MessageSerializer, MessageType
from infrastructure.ports import Factory

import pytest

from services.exceptions import InvalidMessageType


class SerializableEvent(Event):
    data: str = 'test'


@pytest.fixture
def event() -> Event:
    return SerializableEvent(data='test')


class SerializableCommand(Command):
    data: str = 'test'


@pytest.fixture
def command() -> Command:
    return SerializableCommand(data='test')


def get_message(message_type: MessageType, payload_type: str, payload: dict) -> Message:
    return Message(
        type=message_type,
        payload_type=payload_type,
        payload=payload,
    )


class MyEventFactory(Factory):
    registry = {
        'SerializableEvent': SerializableEvent,
    }


class MyCommandFactory(Factory):
    registry = {
        'SerializableCommand': SerializableCommand,
    }


@pytest.fixture
def serializer() -> MessageSerializer:
    return MessageSerializer(event_factory=MyEventFactory(), command_factory=MyCommandFactory())


class TestMessageSerializer:
    def test_serialize_event_message_type_is_event(self, serializer: MessageSerializer, event: Event) -> None:
        message = serializer.serialize(event)

        assert MessageType.EVENT == message.type

    def test_serialize_comamnd_message_type_is_command(
        self,
        serializer: MessageSerializer,
        command: Command,
    ) -> None:
        message = serializer.serialize(command)

        assert MessageType.COMMAND == message.type

    def test_serialize_raises_invalid_message_type_exception(self, serializer: MessageSerializer) -> None:
        with pytest.raises(InvalidMessageType, match="<class 'NoneType'>"):
            serializer.serialize(None)

    def test_serialize_payload_type_serialized(self, serializer: MessageSerializer, event: Event) -> None:
        message = serializer.serialize(event)

        assert 'SerializableEvent' == message.payload_type

    def test_serialize_payload_serialized(self, serializer: MessageSerializer, event: Event) -> None:
        message = serializer.serialize(event)

        assert {'data': 'test'} == message.payload

    def test_deserialize_event_deserialized(self, serializer: MessageSerializer) -> None:
        message = get_message(MessageType.EVENT, 'SerializableEvent', {'data': 'test'})
        event = serializer.deserialize(message)

        assert isinstance(event, Event)

    def test_deserialize_command_deserialized(self, serializer: MessageSerializer) -> None:
        message = get_message(MessageType.COMMAND, 'SerializableCommand', {'data': 'test'})
        command = serializer.deserialize(message)

        assert isinstance(command, Command)

    def test_deserialize_event_type_deserialized(self, serializer: MessageSerializer) -> None:
        message = get_message(MessageType.EVENT, 'SerializableEvent', {'data': 'test'})
        event = serializer.deserialize(message)

        assert 'SerializableEvent' == event.__class__.__name__

    def test_deserialize_command_type_deserialized(self, serializer: MessageSerializer) -> None:
        message = get_message(MessageType.COMMAND, 'SerializableCommand', {'data': 'test'})
        command = serializer.deserialize(message)

        assert 'SerializableCommand' == command.__class__.__name__

    def test_deserialize_raises_invalid_message_type_exception(self, serializer: MessageSerializer) -> None:
        with pytest.raises(InvalidMessageType, match="<class 'NoneType'>"):
            serializer.deserialize(None)

    def test_deserialize_payload_deserialized(self, serializer: MessageSerializer) -> None:
        message = get_message(MessageType.EVENT, 'SerializableEvent', {'data': 'test'})
        event: SerializableEvent = serializer.deserialize(message)

        assert 'test' == event.data
