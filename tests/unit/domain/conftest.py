from core.settings import game_settings

from domain.enums import GameState
from domain.models import Field, Game, Player
from domain.strategies import PlayerTurnSelector

import pytest

from tests.unit.domain.fake_player_turn_selector import FakePlayerTurnSelector


@pytest.fixture
def player() -> Player:
    return Player(id=1, answer_id=None, connected_at=None, fields=[])


@pytest.fixture
def players() -> list[Player]:
    return [
        Player(id=i, answer_id=None, connected_at=None, fields=[]) for i in range(game_settings.players_count_to_start)
    ]


@pytest.fixture
def fields() -> list[Field]:
    return [Field(id=i, value=0, owner=None) for i in range(game_settings.fields_count)]


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
def started_game(fields: list[Field], players: list[Player], player_turn_selector: PlayerTurnSelector) -> Game:
    return Game(
        id=1,
        state=GameState.IN_PROCESS,
        round_number=0,
        player_order=None,
        players=players,
        fields=fields,
        duel=None,
        player_turn_selector=player_turn_selector,
    )


@pytest.fixture
def full_game(players: list[Player]) -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=0,
        player_order=None,
        players=players,
        fields=[],
        duel=None,
        player_turn_selector=None,
    )


@pytest.fixture
def ready_to_start_game(players: list[Player], player_turn_selector: PlayerTurnSelector) -> Game:
    return Game(
        id=1,
        state=GameState.PLAYERS_WAITING,
        round_number=0,
        player_order=None,
        players=players,
        fields=[],
        duel=None,
        player_turn_selector=player_turn_selector,
    )


@pytest.fixture
def round_processing_game(players: list[Player], fields: list[Field], player_turn_selector: PlayerTurnSelector) -> Game:
    return Game(
        id=1,
        state=GameState.ATTACK_WAITING,
        round_number=1,
        player_order=players[0],
        players=players,
        fields=fields,
        duel=None,
        player_turn_selector=player_turn_selector,
    )
