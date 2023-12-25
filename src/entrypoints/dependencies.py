from core.container import container

from infrastructure.ports import UnitOfWork

from services.messagebus import MessageBus


def get_messagebus() -> MessageBus:
    return container.messagebus()


def get_unit_of_work() -> UnitOfWork:
    return container.unit_of_work()
