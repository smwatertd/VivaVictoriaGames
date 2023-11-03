from domain import value_objects
from domain.models import Game

import pytest

from tests.test_case import TestCase


def generate_players(count: int) -> value_objects.Player:
    return tuple(
        value_objects.Player(i)
        for i in range(1, count + 1)
    )


def generate_game() -> Game:
    return Game(1)


@pytest.fixture
def game() -> Game:
    return generate_game()


class TestGame(TestCase):
    def test_add_player_player_added(self, game: Game) -> None:
        [player] = generate_players(1)

        game.add_player(player)

        assert [player] == list(game._players)
