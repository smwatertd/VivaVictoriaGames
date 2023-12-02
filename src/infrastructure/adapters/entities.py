from typing import Any

from domain import enums, models
from domain.events import Event

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    event,
)
from sqlalchemy.orm import registry, relationship


metadata = MetaData()
mapper = registry()

games = Table(
    'games',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'state',
        Enum(enums.GameState),
        default=enums.GameState.PLAYERS_WAITING,
        nullable=False,
    ),
    Column('round_number', Integer, default=0, server_default='0'),
    Column('question_id', Integer, ForeignKey('questions.id')),
)

players = Table(
    'players',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('game_id', Integer, ForeignKey('games.id'), nullable=True),
)

fields = Table(
    'fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('owner_id', Integer, ForeignKey('players.id')),
)

questions = Table(
    'questions',
    metadata,
    Column('id', Integer, primary_key=True),
)

answers = Table(
    'answers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('is_correct', Boolean, default=False, server_default='false'),
    Column('question_id', Integer, ForeignKey('questions.id')),
)


def start_mappers() -> None:
    mapper.dispose()
    mapper.map_imperatively(
        models.Answer,
        answers,
        properties={
            '_question': relationship(
                models.Question,
                back_populates='_answers',
                uselist=False,
            ),
        },
    )
    mapper.map_imperatively(
        models.Question,
        questions,
        properties={
            '_answers': relationship(
                models.Answer,
                back_populates='_question',
            ),
        },
    )
    mapper.map_imperatively(
        models.Field,
        fields,
        properties={
            '_game': relationship(
                models.Game,
                back_populates='_fields',
                uselist=False,
            ),
            '_owner': relationship(
                models.Player,
                back_populates='_fields',
                uselist=False,
            ),
        },
    )
    mapper.map_imperatively(
        models.Player,
        players,
        properties={
            '_game': relationship(
                models.Game,
                back_populates='_players',
                uselist=False,
            ),
            '_fields': relationship(
                models.Field,
                back_populates='_owner',
            ),
        },
    )
    mapper.map_imperatively(
        models.Game,
        games,
        properties={
            '_question': relationship(
                models.Question,
                uselist=False,
            ),
            '_players': relationship(
                models.Player,
                back_populates='_game',
            ),
            '_fields': relationship(
                models.Field,
                back_populates='_game',
            ),
        },
    )


@event.listens_for(models.Game, 'load')
def on_game_load(game: models.Game, _: Any) -> None:
    game._events: list[Event] = []  # type: ignore
