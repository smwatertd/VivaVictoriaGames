from domain import enums, models

import pytest


@pytest.fixture
def empty_duel() -> models.Duel:
    return models.Duel(
        id=1,
        attacker=None,
        defender=None,
        field=None,
        category=None,
        question=None,
        round_number=0,
    )


@pytest.fixture
def empty_game(empty_duel: models.Duel) -> models.Game:
    return models.Game(
        id=1,
        state=enums.GameState.PLAYERS_WAITING,
        round_number=0,
        players=[],
        fields=[],
        duel=empty_duel,
    )


@pytest.fixture
def almost_full_game() -> models.Game:
    return models.Game(
        id=1,
        state=enums.GameState.PLAYERS_WAITING,
        round_number=0,
        players=[],
        fields=[],
        duel=models.Duel(
            id=1,
            attacker=None,
            defender=None,
            field=None,
            category=None,
            question=None,
            round_number=0,
        ),
    )


@pytest.fixture
def player() -> models.Player:
    return models.Player(id=1, answer=None)


class TestGame:
    def test_add_player_player_added(self, empty_game: models.Game, player: models.Player) -> None:
        empty_game.add_player(player)

        assert len(empty_game._players) == 1
        assert player in empty_game._players
