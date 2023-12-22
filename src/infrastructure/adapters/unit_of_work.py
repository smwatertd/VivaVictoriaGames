from typing import Any

from core.settings import db_settings

from infrastructure.adapters import clients
from infrastructure.adapters import repositories
from infrastructure.adapters.message_serializer import MessageSerializer
from infrastructure.ports import Producer, UnitOfWork
from infrastructure.ports.clients import HTTPClient

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


SQLALCHEMY_DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(db_settings.url, echo=db_settings.echo),
    class_=AsyncSession,
    expire_on_commit=False,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        events_group: str,
        event_producer: Producer,
        serializer: MessageSerializer,
        http_client: HTTPClient,
        session_factory: async_sessionmaker[AsyncSession] = SQLALCHEMY_DEFAULT_SESSION_FACTORY,
    ) -> None:
        super().__init__(events_group, event_producer, serializer)
        self._http_client = http_client
        self._session_factory = session_factory

    async def __aenter__(self) -> 'SQLAlchemyUnitOfWork':
        self._session = self._session_factory()
        self.games = repositories.SQLAlchemyGamesRepository(self._session)
        self.players = repositories.SQLAlchemyPlayersRepository(self._session)
        self.fields = repositories.SQLAlchemyFieldsRepository(self._session)
        self.questions = clients.QuestionsClient(self._http_client)
        self.categories = clients.CategoriesClient(self._http_client)
        return await super().__aenter__()

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        return await super().__aexit__(*args, **kwargs)

    async def rollback(self) -> None:
        await self._session.rollback()

    async def commit(self) -> None:
        await self._session.commit()
