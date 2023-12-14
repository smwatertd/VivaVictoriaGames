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
    Column('state', Enum(enums.GameState), default=enums.GameState.PLAYERS_WAITING, nullable=False),
    Column('round_number', Integer, default=0, server_default='0'),
)

duels = Table(
    'duels',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('attacker_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
    Column('defender_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
    Column('category_id', Integer, ForeignKey('categories.id'), nullable=True, default=None, server_default=None),
    Column('question_id', Integer, ForeignKey('questions.id'), nullable=True, default=None, server_default=None),
    Column('field_id', Integer, ForeignKey('fields.id'), nullable=True, default=None, server_default=None),
    Column('round_number', Integer, default=0, server_default='0'),
)

players = Table(
    'players',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id'), nullable=True),
    Column('answer_id', Integer, ForeignKey('answers.id'), nullable=True, default=None, server_default=None),
)

fields = Table(
    'fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('owner_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
)

categories = Table(
    'categories',
    metadata,
    Column('id', Integer, primary_key=True),
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
        models.Category,
        categories,
        properties={
            '_duels': relationship(
                models.Duel,
                back_populates='_category',
            ),
        },
    )
    mapper.map_imperatively(
        models.Answer,
        answers,
        properties={
            '_question': relationship(
                models.Question,
                back_populates='_answers',
                uselist=False,
                foreign_keys=[answers.c.question_id],
            ),
            '_player_answers': relationship(
                models.Player,
                back_populates='_answer',
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
            '_duels': relationship(
                models.Duel,
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
                foreign_keys=[fields.c.game_id],
            ),
            '_owner': relationship(
                models.Player,
                back_populates='_fields',
                uselist=False,
                foreign_keys=[fields.c.owner_id],
            ),
            '_duel': relationship(
                models.Duel,
                back_populates='_field',
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
                foreign_keys=[players.c.game_id],
            ),
            '_answer': relationship(
                models.Answer,
                back_populates='_player_answers',
                uselist=False,
                foreign_keys=[players.c.answer_id],
            ),
            '_fields': relationship(
                models.Field,
                back_populates='_owner',
            ),
            '_duel_as_attacker': relationship(
                models.Duel,
                back_populates='_attacker',
                uselist=False,
                foreign_keys=[duels.c.attacker_id],
            ),
            '_duel_as_defender': relationship(
                models.Duel,
                back_populates='_defender',
                uselist=False,
                foreign_keys=[duels.c.defender_id],
            ),
        },
    )
    mapper.map_imperatively(
        models.Game,
        games,
        properties={
            '_players': relationship(
                models.Player,
                back_populates='_game',
            ),
            '_fields': relationship(
                models.Field,
                back_populates='_game',
            ),
            '_duel': relationship(
                models.Duel,
                back_populates='_game',
                uselist=False,
            ),
        },
    )
    mapper.map_imperatively(
        models.Duel,
        duels,
        properties={
            '_game': relationship(
                models.Game,
                uselist=False,
                back_populates='_duel',
                foreign_keys=[duels.c.game_id],
            ),
            '_attacker': relationship(
                models.Player,
                uselist=False,
                back_populates='_duel_as_attacker',
                foreign_keys=[duels.c.attacker_id],
            ),
            '_defender': relationship(
                models.Player,
                uselist=False,
                back_populates='_duel_as_defender',
                foreign_keys=[duels.c.defender_id],
            ),
            '_category': relationship(
                models.Category,
                uselist=False,
                back_populates='_duels',
                foreign_keys=[duels.c.category_id],
            ),
            '_question': relationship(
                models.Question,
                uselist=False,
                back_populates='_duels',
                foreign_keys=[duels.c.question_id],
            ),
            '_field': relationship(
                models.Field,
                uselist=False,
                back_populates='_duel',
                foreign_keys=[duels.c.field_id],
            ),
        },
    )


@event.listens_for(models.Game, 'load')
def on_game_load(game: models.Game, _: Any) -> None:
    game._events: list[Event] = []  # type: ignore
