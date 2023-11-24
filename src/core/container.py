from typing import Any

from dependency_injector import containers, providers

from infrastructure import adapters
from infrastructure.adapters.consumers import RabbitMQConsumer
from infrastructure.adapters.producers import RabbitMQProducer
from infrastructure.ports import UnitOfWork

from services.handlers import COMMAND_HANDLERS, EVENT_HANDLERS
from services.messagebus import MessageBus


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_producer: Any = providers.Factory(
        RabbitMQProducer,
    )

    event_consumer: Any = providers.Factory(
        RabbitMQConsumer,
    )

    messagebus: Any = providers.Singleton(
        MessageBus,
        command_handlers=COMMAND_HANDLERS,
        event_handlers=EVENT_HANDLERS,
    )

    channel_layer: Any = providers.Singleton(
        adapters.ChannelLayer,
    )

    message_parser: Any = providers.Singleton(
        adapters.MessageParser,
    )

    message_dispatcher: Any = providers.Factory(
        adapters.MessageDispatcher,
        consumer=event_consumer,
        parser=message_parser,
        messagebus=messagebus,
    )

    unit_of_work: UnitOfWork = providers.Factory(
        adapters.SQLAlchemyUnitOfWork,
        event_producer=event_producer,
    )


container = Container()
