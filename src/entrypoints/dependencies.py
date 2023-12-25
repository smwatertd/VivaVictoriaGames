from core.container import container

from services.messagebus import MessageBus


def get_messagebus() -> MessageBus:
    return container.messagebus()
