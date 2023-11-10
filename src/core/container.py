from typing import Any

from dependency_injector import containers, providers

from infrastructure.adapters import ChannelLayer
from infrastructure.adapters import UnitOfWorkAdapter
from infrastructure.adapters import repositories as adapters_repositories
from infrastructure.adapters.consumers import RabbitMQConsumer
from infrastructure.adapters.producers import RabbitMQProducer
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

    unit_of_work: UnitOfWork = providers.Factory(
        UnitOfWorkAdapter,
        games=games_repository,
        players=players_repository,
        event_producer=event_producer,
    )


container = Container()
