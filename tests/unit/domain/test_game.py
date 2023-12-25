from domain import events, exceptions
from domain.enums import GameState
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

    def test_try_start_game_doesnt_started(self, empty_game: Game) -> None:
        empty_game.try_start()

        assert empty_game._state == GameState.PLAYERS_WAITING

    def test_try_start_game_started(self, ready_to_start_game: Game) -> None:
        ready_to_start_game.try_start()

        assert ready_to_start_game._state == GameState.IN_PROCESS

    def test_try_start_round_number_setted(self, ready_to_start_game: Game) -> None:
        ready_to_start_game.try_start()

        assert ready_to_start_game._round_number == 1

    def test_try_start_event_registered(self, ready_to_start_game: Game) -> None:
        ready_to_start_game.try_start()

        order = [events.OrderPlayer(id=player._id) for player in self._get_game_order(ready_to_start_game)]
        assert events.GameStarted(game_id=ready_to_start_game._id, order=order) in ready_to_start_game._events

    def test_start_round_state_setted(self, started_game: Game) -> None:
        started_game.start_round()

        assert started_game._state == GameState.ATTACK_WAITING

    def test_start_round_event_registered(self, started_game: Game) -> None:
        started_game.start_round()

        player_order = self._get_game_player_order(started_game)
        assert (
            events.RoundStarted(
                game_id=started_game._id,
                round_number=started_game._round_number,
                player_order_id=player_order._id,
            )
            in started_game._events
        )

    def _get_game_order(self, game: Game) -> list[Player]:
        return game._player_turn_selector.get_order(game._players)

    def _get_game_player_order(self, game: Game) -> Player:
        return game._player_turn_selector.select(game._round_number, game._players)
