from domain.enums import GameState
from domain.models import Game

import pytest


@pytest.fixture
def empty_game() -> Game:
    Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=1,
        player_order=None,
        players=[],
        fields=[],
        duel=None,
        player_turn_selector=None,
    )
