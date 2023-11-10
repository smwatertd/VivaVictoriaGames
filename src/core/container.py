from typing import Any

from dependency_injector import containers, providers

from infrastructure.adapters import (
    ChannelLayer,
    MessageDispatcher,
    MessageParser,
    UnitOfWorkAdapter,
)
from infrastructure.adapters import repositories as adapters_repositories
from infrastructure.adapters.consumers import RabbitMQConsumer
from infrastructure.adapters.producers import RabbitMQProducer, RedisProducer
from infrastructure.ports import UnitOfWork
from infrastructure.ports import repositories as ports_repositories

from services.handlers import COMMAND_HANDLERS, EVENT_HANDLERS
from services.messagebus import MessageBus


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    games_repository: ports_repositories.GamesRepository = providers.Factory(
        adapters_repositories.InMemoryGamesRepository,
    )

    players_repository: ports_repositories.PlayersRepository = providers.Factory(
        adapters_repositories.InMemoryPlayersRepository,
    )

    fields_repository: ports_repositories.FieldsRepository = providers.Factory(
        adapters_repositories.InMemoryFieldsRepository,
    )

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
        ChannelLayer,
    )

    message_parser: Any = providers.Singleton(
        MessageParser,
    )

    message_dispatcher: Any = providers.Factory(
        MessageDispatcher,
        consumer=event_consumer,
        parser=message_parser,
        messagebus=messagebus,
    )

    message_producer: Any = providers.Factory(
        RedisProducer,
    )

    unit_of_work: UnitOfWork = providers.Factory(
        UnitOfWorkAdapter,
        games=games_repository,
        players=players_repository,
        fields=fields_repository,
        event_producer=event_producer,
        message_producer=message_producer,
    )


container = Container()
