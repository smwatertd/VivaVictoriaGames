from domain import events, exceptions
from domain.models import Game, Player

import pytest

# TODO: Game __init__ None args


class TestGame:
    def test_get_id_id_returned(self, empty_game: Game) -> None:
        game_id = empty_game.get_id()

        assert game_id == empty_game._id

    def test_add_player_player_added(self, empty_game: Game, player: Player) -> None:
        empty_game.add_player(player)

        assert player in empty_game._players

    def test_add_player_player_connected_at_setted(self, empty_game: Game, player: Player) -> None:
        empty_game.add_player(player)

        assert player._connected_at is not None

    def test_add_player_event_registered(self, empty_game: Game, player: Player) -> None:
        empty_game.add_player(player)

        assert (
            events.PlayerAdded(
                game_id=empty_game._id,
                player_id=player._id,
                connected_players=[events.ConnectedPlayer(id=player._id)],
            )
            in empty_game._events
        )

    def test_add_player_game_game_already_started(self, started_game: Game, player: Player) -> None:
        with pytest.raises(exceptions.GameAlreadyStarted, match='Game already started'):
            started_game.add_player(player)

    def test_add_player_game_is_full(self, full_game: Game, player: Player) -> None:
        with pytest.raises(exceptions.GameIsFull, match='Game is full'):
            full_game.add_player(player)

    def test_remove_player_player_removed(self, empty_game: Game, player: Player) -> None:
        empty_game._players.append(player)

        empty_game.remove_player(player)

        assert player not in empty_game._players

    def test_remove_player_event_registered(self, empty_game: Game, player: Player) -> None:
        empty_game._players.append(player)

        empty_game.remove_player(player)

        assert (
            events.PlayerRemoved(
                game_id=empty_game._id,
                player_id=player._id,
            )
            in empty_game._events
        )
