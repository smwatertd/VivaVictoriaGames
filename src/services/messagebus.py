from typing import Callable, Coroutine, Iterable, Type

from domain.commands import Command
from domain.events import Event

from infrastructure.ports import UnitOfWork

from services.exceptions import InvalidMessageType


CommandHandler = Callable[[Command, UnitOfWork], Coroutine]
EventHandler = Callable[[Event, UnitOfWork], Coroutine]


class MessageBus:
    # TODO: Fix type annotations
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        command_handlers: dict[Type, CommandHandler],
        event_handlers: dict[Type, Iterable[EventHandler]],
    ) -> None:
        self._unit_of_work = unit_of_work
        self._command_handlers = command_handlers
        self._event_handlers = event_handlers

    async def handle(self, message: Command | Event) -> None:
        if isinstance(message, Command):
            await self._handle_command(message)
        elif isinstance(message, Event):
            await self._handle_event(message)
        else:
            raise InvalidMessageType(type(message))

    async def _handle_command(self, command: Command) -> None:
        handler = self._command_handlers.get(type(command))
        if handler is not None:
            await handler(command, self._unit_of_work)
            await self._unit_of_work.publish_events()

    async def _handle_event(self, event: Event) -> None:
        # TODO: Fix async
        for handler in self._event_handlers.get(type(event), []):
            await handler(event, self._unit_of_work)
            await self._unit_of_work.publish_events()
