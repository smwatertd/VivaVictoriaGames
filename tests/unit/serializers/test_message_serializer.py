from domain.events import Event

from infrastructure.adapters import Message, MessageSerializer, MessageType

import pytest

from services.commands import Command
from services.exceptions import InvalidMessageType


class TestMessageSerializer:
    def test_serialize_message_type_is_event(self, serializer: MessageSerializer, event: Event) -> None:
        message = serializer.serialize(event)

        assert message.type == MessageType.EVENT

    def test_serialize_message_type_is_command(self, serializer: MessageSerializer, command: Command) -> None:
        message = serializer.serialize(command)

        assert message.type == MessageType.COMMAND

    def test_serialize_raises_invalid_message_type_exception(self, serializer: MessageSerializer) -> None:
        with pytest.raises(InvalidMessageType, match="Invalid message type: <class 'NoneType'>"):
            serializer.serialize(None)

    def test_serialize_payload_type_serialized(self, serializer: MessageSerializer, event: Event) -> None:
        message = serializer.serialize(event)

        assert message.payload_type == 'SerializableEvent'

    def test_serialize_payload_serialized(self, serializer: MessageSerializer, event: Event) -> None:
        message = serializer.serialize(event)

        assert message.payload == {'data': 'test'}

    def test_deserialize_event_deserialized(self, serializer: MessageSerializer, event_message: Message) -> None:
        event = serializer.deserialize(event_message)

        assert isinstance(event, Event)

    def test_deserialize_command_deserialized(self, serializer: MessageSerializer, command_message: Message) -> None:
        command = serializer.deserialize(command_message)

        assert isinstance(command, Command)

    def test_deserialize_raises_invalid_message_type_exception(self, serializer: MessageSerializer) -> None:
        with pytest.raises(InvalidMessageType, match="Invalid message type: <class 'NoneType'>"):
            serializer.deserialize(None)

    def test_deserialize_payload_type_deserialized(self, serializer: MessageSerializer, event_message: Message) -> None:
        event = serializer.deserialize(event_message)

        assert event.__class__.__name__ == 'SerializableEvent'

    def test_deserialize_payload_deserialized(self, serializer: MessageSerializer, event_message: Message) -> None:
        event = serializer.deserialize(event_message)

        assert event.data == 'test'
