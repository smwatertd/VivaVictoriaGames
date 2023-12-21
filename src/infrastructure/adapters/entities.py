from typing import Any

from core.container import container

from domain import enums, models
from domain.events import Event

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, MetaData, Table, event, func
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
    Column('round_number', Integer, default=0, server_default='0'),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('attacker_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
    Column('defender_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
    Column('category_id', Integer, nullable=True, default=None, server_default=None),
    Column('question_id', Integer, nullable=True, default=None, server_default=None),
    Column('correct_answer_id', Integer, nullable=True, default=None, server_default=None),
    Column('field_id', Integer, ForeignKey('fields.id'), nullable=True, default=None, server_default=None),
)

players = Table(
    'players',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('connected_at', DateTime, default=func.now(), server_default=func.now()),
    Column('game_id', Integer, ForeignKey('games.id'), nullable=True),
    Column('answer_id', Integer, nullable=True, default=None, server_default=None),
    Column('game_order_id', Integer, ForeignKey('games.id'), nullable=True, default=None, server_default=None),
)

fields = Table(
    'fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('value', Integer, default=0, server_default='0'),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('owner_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
)


def start_mappers() -> None:
    mapper.dispose()
    mapper.map_imperatively(
        models.Field,
        fields,
        properties={
            '_id': fields.c.id,
            '_value': fields.c.value,
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
            '_id': players.c.id,
            '_answer_id': players.c.answer_id,
            '_connected_at': players.c.connected_at,
            '_game': relationship(
                models.Game,
                back_populates='_players',
                uselist=False,
                foreign_keys=[players.c.game_id],
            ),
            '_game_order': relationship(
                models.Game,
                back_populates='_player_order',
                uselist=False,
                foreign_keys=[players.c.game_order_id],
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
            '_id': games.c.id,
            '_state': games.c.state,
            '_round_number': games.c.round_number,
            '_players': relationship(
                models.Player,
                back_populates='_game',
                foreign_keys=[players.c.game_id],
            ),
            '_player_order': relationship(
                models.Player,
                back_populates='_game_order',
                uselist=False,
                foreign_keys=[players.c.game_order_id],
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
            '_id': duels.c.id,
            '_round_number': duels.c.round_number,
            '_category_id': duels.c.category_id,
            '_question_id': duels.c.question_id,
            '_correct_answer_id': duels.c.correct_answer_id,
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
    game._player_turn_selector = container.player_turn_selector()
