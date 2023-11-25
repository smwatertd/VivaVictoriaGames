from domain import enums

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import registry


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
    Column('game_id', Integer, ForeignKey('games.id')),
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
