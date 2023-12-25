from core.settings import game_settings

from domain.enums import GameState
from domain.models import Game, Player

import pytest


@pytest.fixture
def player() -> Player:
    return Player(id=1, answer_id=None, connected_at=None, fields=[])


@pytest.fixture
def empty_game() -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=1,
        player_order=None,
        players=[],
        fields=[],
        duel=None,
        player_turn_selector=None,
    )


@pytest.fixture
def started_game() -> Game:
    return Game(
        id=1,
        state=GameState.IN_PROCESS,
        round_number=1,
        player_order=None,
        players=[],
        fields=[],
        duel=None,
        player_turn_selector=None,
    )


@pytest.fixture
def full_game(player: Player) -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=1,
        player_order=None,
        players=[player] * game_settings.players_count_to_start,
        fields=[],
        duel=None,
        player_turn_selector=None,
    )
