from domain.events import Event

from infrastructure.adapters import Message, MessageSerializer, MessageType
from infrastructure.ports import Factory

import pytest

from services.commands import Command


class SerializableEvent(Event):
    data: str = 'test'


class SerializableCommand(Command):
    data: str = 'test'


class MyEventFactory(Factory):
    registry = {
        'SerializableEvent': SerializableEvent,
    }


class MyCommandFactory(Factory):
    registry = {
        'SerializableCommand': SerializableCommand,
    }


@pytest.fixture
def event() -> Event:
    return SerializableEvent(data='test')


@pytest.fixture
def command() -> Command:
    return SerializableCommand(data='test')


@pytest.fixture
def serializer() -> MessageSerializer:
    return MessageSerializer(event_factory=MyEventFactory(), command_factory=MyCommandFactory())


@pytest.fixture
def event_message() -> Message:
    return Message(type=MessageType.EVENT, payload_type='SerializableEvent', payload={'data': 'test'})


@pytest.fixture
def command_message() -> Message:
    return Message(type=MessageType.COMMAND, payload_type='SerializableCommand', payload={'data': 'test'})
