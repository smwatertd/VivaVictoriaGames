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
        command_handlers: dict[Type, CommandHandler],
        event_handlers: dict[Type, Iterable[EventHandler]],
    ) -> None:
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

    async def handle(self, message: Command | Event, uow: UnitOfWork) -> None:
        if isinstance(message, Command):
            await self._handle_command(message, uow)
        elif isinstance(message, Event):
            await self._handle_event(message, uow)
        else:
            raise InvalidMessageType
        await uow.publish_events()

    async def _handle_command(self, command: Command, uow: UnitOfWork) -> None:
        return await self.command_handlers[type(command)](command, uow)

    async def _handle_event(self, event: Event, uow: UnitOfWork) -> None:
        # TODO: Fix async
        for handler in self.event_handlers[type(event)]:
            await handler(event, uow)
