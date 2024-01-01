from typing import Type

from core.settings import game_events_message_broker_settings, game_message_broker_settings

from dependency_injector import containers, providers

from domain.resolvers import AnsweredByConflictResolver, ConflictResolver
from domain.strategies import ConnectionTimeAndIdentityPlayerTurnSelector, PlayerTurnSelector

from infrastructure import adapters, ports
from infrastructure.adapters.clients import HTTPXClient
from infrastructure.ports.clients import HTTPClient

from services.handlers import COMMAND_HANDLERS, EVENT_HANDLERS
from services.messagebus import MessageBus


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    event_factory: Type[adapters.EventFactory] = providers.Factory(
        adapters.EventFactory,
    )  # type: ignore

    command_factory: Type[adapters.CommandFactory] = providers.Factory(
        adapters.CommandFactory,
    )  # type: ignore

    message_serializer: Type[adapters.MessageSerializer] = providers.Factory(
        adapters.MessageSerializer,
        event_factory=event_factory,
        command_factory=command_factory,
    )  # type: ignore

    message_producer: Type[ports.Producer] = providers.Factory(
        adapters.RabbitMQProducer,
        host=game_events_message_broker_settings.host,
        port=game_events_message_broker_settings.port,
        virtual_host=game_events_message_broker_settings.virtual_host,
        exchange=game_events_message_broker_settings.exchange,
    )  # type: ignore

    message_consumer: Type[ports.Consumer] = providers.Factory(
        adapters.RabbitMQConsumer,
        host=game_events_message_broker_settings.host,
        port=game_events_message_broker_settings.port,
        virtual_host=game_events_message_broker_settings.virtual_host,
    )  # type: ignore

    chat_message_consumer: Type[ports.Consumer] = providers.Factory(
        adapters.RedisConsumer,
        host=game_message_broker_settings.host,
        port=game_message_broker_settings.port,
        db=game_message_broker_settings.db,
        encoding=game_message_broker_settings.encoding,
        ignore_subscribe_messages=True,
    )  # type: ignore

    http_client: Type[HTTPClient] = providers.Factory(
        HTTPXClient,
    )  # type: ignore

    unit_of_work: Type[ports.UnitOfWork] = providers.Factory(
        adapters.SQLAlchemyUnitOfWork,
        events_group=game_events_message_broker_settings.games_events_queue,
        event_producer=message_producer,
        serializer=message_serializer,
        http_client=http_client,
    )  # type: ignore

    messagebus: Type[MessageBus] = providers.Factory(
        MessageBus,
        unit_of_work=unit_of_work,
        command_handlers=COMMAND_HANDLERS,
        event_handlers=EVENT_HANDLERS,
    )  # type: ignore

    channel_layer: Type[adapters.ChannelLayer] = providers.Factory(
        adapters.ChannelLayer,
    )  # type: ignore

    message_handler: Type[adapters.MessageHandler] = providers.Factory(
        adapters.MessageHandler,
        events_group=game_events_message_broker_settings.games_events_queue,
        consumer=message_consumer,
        messagebus=messagebus,
        serializer=message_serializer,
    )  # type: ignore

    player_turn_selector: Type[PlayerTurnSelector] = providers.Factory(
        ConnectionTimeAndIdentityPlayerTurnSelector,
    )  # type: ignore

    conflict_resolver: Type[ConflictResolver] = providers.Factory(
        AnsweredByConflictResolver,
    )  # type: ignore


container = Container()
