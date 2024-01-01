from typing import Any

from core.container import container

from domain import enums, models
from domain.events import Event

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, MetaData, Table, event, func
from sqlalchemy.orm import registry, relationship


metadata = MetaData()
mapper = registry()

games = Table(
    'games',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('state', Enum(enums.GameState), default=enums.GameState.PLAYERS_WAITING, nullable=False),
    Column('creator_id', Integer, default=None, server_default=None),
)

preparations = Table(
    'preparations',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('round_number', Integer, default=0, server_default='0'),
    Column('game_id', Integer, ForeignKey('games.id')),
)

captures = Table(
    'captures',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('round_number', Integer, default=0, server_default='0'),
    Column('correct_answer_id', Integer, nullable=True, default=None, server_default=None),
    Column('game_id', Integer, ForeignKey('games.id')),
)

battles = Table(
    'battles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('round_number', Integer, default=0, server_default='0'),
    Column('game_id', Integer, ForeignKey('games.id')),
)

duels = Table(
    'duels',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('round_number', Integer, default=0, server_default='0'),
    Column('category_id', Integer, nullable=True, default=None, server_default=None),
    Column('correct_answer_id', Integer, nullable=True, default=None, server_default=None),
    Column('battle_id', Integer, ForeignKey('battles.id')),
    Column('attacker_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
    Column('defender_id', Integer, ForeignKey('players.id'), nullable=True, default=None, server_default=None),
    Column('field_id', Integer, ForeignKey('captured_fields.id'), nullable=True, default=None, server_default=None),
)

players = Table(
    'players',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('connected_at', DateTime, default=func.now(), server_default=func.now()),
    Column('answer_id', Integer, nullable=True, default=None, server_default=None),
    Column('answered_at', DateTime, default=None, server_default=None),
    Column('game_id', Integer, ForeignKey('games.id'), nullable=True),
    Column('game_order_id', Integer, ForeignKey('games.id'), nullable=True, default=None, server_default=None),
    Column(
        'marked_field_id',
        Integer,
        ForeignKey('marked_fields.id'),
        nullable=True,
        default=None,
        server_default=None,
    ),
)

fields = Table(
    'fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('value', Integer, default=0, server_default='0'),
    Column('game_id', Integer, ForeignKey('games.id')),
)

marked_fields = Table(
    'marked_fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('field_id', Integer, ForeignKey('fields.id')),
    Column('capture_id', Integer, ForeignKey('captures.id')),
)

captured_fields = Table(
    'captured_fields',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('is_base', Boolean, default=False),
    Column('field_id', Integer, ForeignKey('fields.id')),
    Column('owner_id', Integer, ForeignKey('players.id')),
)


def start_mappers() -> None:
    mapper.dispose()
    mapper.map_imperatively(
        models.Game,
        games,
        properties={
            '_id': games.c.id,
            '_state': games.c.state,
            '_creator_id': games.c.creator_id,
            '_preparation': relationship(
                models.Preparation,
                back_populates='_game',
                uselist=False,
                foreign_keys=[preparations.c.game_id],
            ),
            '_capture': relationship(
                models.Capture,
                back_populates='_game',
                uselist=False,
                foreign_keys=[captures.c.game_id],
            ),
            '_battle': relationship(
                models.Battle,
                back_populates='_game',
                uselist=False,
                foreign_keys=[battles.c.game_id],
            ),
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
                foreign_keys=[fields.c.game_id],
            ),
        },
    )

    mapper.map_imperatively(
        models.Preparation,
        preparations,
        properties={
            '_id': preparations.c.id,
            '_round_number': preparations.c.round_number,
            '_game': relationship(
                models.Game,
                back_populates='_preparation',
                uselist=False,
                foreign_keys=[preparations.c.game_id],
            ),
        },
    )

    mapper.map_imperatively(
        models.Capture,
        captures,
        properties={
            '_id': captures.c.id,
            '_round_number': captures.c.round_number,
            '_correct_answer_id': captures.c.correct_answer_id,
            '_game': relationship(
                models.Game,
                back_populates='_capture',
                uselist=False,
                foreign_keys=[captures.c.game_id],
            ),
            '_marked_fields': relationship(
                models.MarkField,
                back_populates='_capture',
                foreign_keys=[marked_fields.c.capture_id],
                cascade='all, delete-orphan',
            ),
        },
    )

    mapper.map_imperatively(
        models.Battle,
        battles,
        properties={
            '_id': battles.c.id,
            '_round_number': battles.c.round_number,
            '_game': relationship(
                models.Game,
                back_populates='_battle',
                uselist=False,
                foreign_keys=[battles.c.game_id],
            ),
            '_duel': relationship(
                models.Duel,
                back_populates='_battle',
                uselist=False,
                foreign_keys=[duels.c.battle_id],
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
            '_correct_answer_id': duels.c.correct_answer_id,
            '_battle': relationship(
                models.Battle,
                back_populates='_duel',
                uselist=False,
                foreign_keys=[duels.c.battle_id],
            ),
            '_attacker': relationship(
                models.Player,
                back_populates='_duel_as_attacker',
                uselist=False,
                foreign_keys=[duels.c.attacker_id],
            ),
            '_defender': relationship(
                models.Player,
                back_populates='_duel_as_defender',
                uselist=False,
                foreign_keys=[duels.c.defender_id],
            ),
            '_field': relationship(
                models.CapturedField,
                back_populates='_duel',
                uselist=False,
                foreign_keys=[duels.c.field_id],
            ),
        },
    )

    mapper.map_imperatively(
        models.Player,
        players,
        properties={
            '_id': players.c.id,
            '_connected_at': players.c.connected_at,
            '_answer_id': players.c.answer_id,
            '_answered_at': players.c.answered_at,
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
                models.CapturedField,
                back_populates='_owner',
                foreign_keys=[captured_fields.c.owner_id],
            ),
            '_marked_field': relationship(
                models.MarkField,
                back_populates='_players',
                uselist=False,
                foreign_keys=[players.c.marked_field_id],
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
            '_marked_field': relationship(
                models.MarkField,
                back_populates='_field',
                uselist=False,
                foreign_keys=[marked_fields.c.field_id],
            ),
            '_captured': relationship(
                models.CapturedField,
                back_populates='_field',
                uselist=False,
                foreign_keys=[captured_fields.c.field_id],
            ),
        },
    )

    mapper.map_imperatively(
        models.MarkField,
        marked_fields,
        properties={
            '_field': relationship(
                models.Field,
                back_populates='_marked_field',
                uselist=False,
                foreign_keys=[marked_fields.c.field_id],
            ),
            '_capture': relationship(
                models.Capture,
                back_populates='_marked_fields',
                uselist=False,
                foreign_keys=[marked_fields.c.capture_id],
            ),
            '_players': relationship(
                models.Player,
                back_populates='_marked_field',
                foreign_keys=[players.c.marked_field_id],
            ),
        },
    )

    mapper.map_imperatively(
        models.CapturedField,
        captured_fields,
        properties={
            '_is_base': captured_fields.c.is_base,
            '_field': relationship(
                models.Field,
                back_populates='_captured',
                uselist=False,
                foreign_keys=[captured_fields.c.field_id],
            ),
            '_owner': relationship(
                models.Player,
                back_populates='_fields',
                uselist=False,
                foreign_keys=[captured_fields.c.owner_id],
            ),
            '_duel': relationship(
                models.Duel,
                back_populates='_field',
                uselist=False,
                foreign_keys=[duels.c.field_id],
            ),
        },
    )


def stop_mappers() -> None:
    mapper.dispose()


@event.listens_for(models.Game, 'load')
def on_game_load(game: models.Game, _: Any) -> None:
    game._events: list[Event] = []  # type: ignore
    game._player_turn_selector = container.player_turn_selector()


@event.listens_for(models.Capture, 'load')
def on_capture_load(capture: models.Capture, _: Any) -> None:
    capture._conflict_resolver = container.conflict_resolver()
