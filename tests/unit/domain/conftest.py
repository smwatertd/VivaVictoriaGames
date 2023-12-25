from core.settings import game_settings

from domain.enums import GameState
from domain.models import Game, Player
from domain.strategies import PlayerTurnSelector

import pytest

from tests.unit.domain.fake_player_turn_selector import FakePlayerTurnSelector


@pytest.fixture
def player() -> Player:
    return Player(id=1, answer_id=None, connected_at=None, fields=[])


@pytest.fixture
def player_turn_selector() -> PlayerTurnSelector:
    return FakePlayerTurnSelector()


@pytest.fixture
def empty_game() -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=0,
        player_order=None,
        players=[],
        fields=[],
        duel=None,
        player_turn_selector=None,
    )


@pytest.fixture
def started_game(player_turn_selector: PlayerTurnSelector) -> Game:
    return Game(
        id=1,
        state=GameState.IN_PROCESS,
        round_number=0,
        player_order=None,
        players=_get_players(game_settings.players_count_to_start),
        fields=[],
        duel=None,
        player_turn_selector=player_turn_selector,
    )


@pytest.fixture
def full_game() -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=0,
        player_order=None,
        players=_get_players(game_settings.players_count_to_start),
        fields=[],
        duel=None,
        player_turn_selector=None,
    )


@pytest.fixture
def ready_to_start_game(player_turn_selector: PlayerTurnSelector) -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=0,
        player_order=None,
        players=_get_players(game_settings.players_count_to_start),
        fields=[],
        duel=None,
        player_turn_selector=player_turn_selector,
    )


@pytest.fixture
def round_processing_game(player_turn_selector: PlayerTurnSelector) -> Game:
    return Game(
        id=1,
        state=GameState.ATTACK_WAITING,
        round_number=1,
        player_order=None,
        players=_get_players(game_settings.players_count_to_start),
        fields=[],
        duel=None,
        player_turn_selector=player_turn_selector,
    )


def _get_players(count: int) -> list[Player]:
    return [Player(id=i, answer_id=None, connected_at=None, fields=[]) for i in range(count)]
