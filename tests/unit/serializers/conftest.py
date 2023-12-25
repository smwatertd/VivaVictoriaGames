from domain.events import Event

from infrastructure.adapters import Message, MessageSerializer, MessageType
from infrastructure.ports import Factory

import pytest

from services.commands import Command


class FakeEvent(Event):
    data: str = 'test'


class FakeCommand(Command):
    data: str = 'test'


class FakeEventFactory(Factory):
    registry = {
        'FakeEvent': FakeEvent,
    }


class FakeCommandFactory(Factory):
    registry = {
        'FakeCommand': FakeCommand,
    }


@pytest.fixture
def event() -> Event:
    return FakeEvent(data='test')


@pytest.fixture
def command() -> Command:
    return FakeCommand(data='test')


@pytest.fixture
def serializer() -> MessageSerializer:
    return MessageSerializer(event_factory=FakeEventFactory(), command_factory=FakeCommandFactory())


@pytest.fixture
def event_message() -> Message:
    return Message(type=MessageType.EVENT, payload_type='FakeEvent', payload={'data': 'test'})


@pytest.fixture
def command_message() -> Message:
    return Message(type=MessageType.COMMAND, payload_type='FakeCommand', payload={'data': 'test'})
