from core.settings import game_settings

from domain import enums, events, exceptions, models

import pytest


def get_players(players_count: int) -> list[models.Player]:
    return [
        models.Player(id=i, username=f'player_{i}') for i in range(1, players_count + 1)
    ]


def get_game(
    id: int = 1,
    players: list[models.Player] | None = None,
    state: enums.GameState = enums.GameState.PLAYERS_WAITING,
    fields: list[models.Field] | None = None,
) -> models.Game:
    if players is None:
        players = []
    if fields is None:
        fields = []
    return models.Game(
        id=id,
        players=players,
        state=state,
        fields=fields,
    )


def add_game_players(game: models.Game, players: list[models.Player]) -> None:
    for player in players:
        game.add_player(player)
    game.clear_events()


class TestGame:
    def test_add_player_player_added(self) -> None:
        game = get_game()
        player, *_ = get_players(1)

        game.add_player(player)

        assert len(game._players) == 1
        assert player in game._players

    def test_add_player_player_added_event_registered(self) -> None:
        game = get_game()
        player, *_ = get_players(1)

        game.add_player(player)

        registered_events = game.collect_events()
        expected_event = events.PlayerAdded(
            game_id=game.id,
            player_id=player.id,
            username=player.username,
        )
        assert expected_event in registered_events

    def test_add_player_game_all_players_connected_event_registered(self) -> None:
        game = get_game()
        player, *rest = get_players(game_settings.players_count_to_start)
        add_game_players(game, rest)

        game.add_player(player)

        registered_events = game.collect_events()
        expected_event = events.GameClosed(game_id=game.id)
        assert expected_event in registered_events

    def test_add_player_game_invalid_state(self) -> None:
        game = get_game(state=enums.GameState.START_WAITING)
        player, *_ = get_players(1)

        with pytest.raises(exceptions.GameInvalidState):
            game.add_player(player)

    def test_add_player_player_already_added(self) -> None:
        game = get_game()
        player, *_ = get_players(1)
        game.add_player(player)

        with pytest.raises(exceptions.PlayerAlreadyAdded):
            game.add_player(player)

    def test_add_player_game_closed_event_registered(self) -> None:
        game = get_game()
        player, *rest = get_players(game_settings.players_count_to_start)
        add_game_players(game, rest)

        game.add_player(player)

        registered_events = game.collect_events()
        expected_event = events.GameClosed(game_id=game.id)
        assert expected_event in registered_events

    def test_add_player_start_waiting_state_setted(self) -> None:
        game = get_game()
        player, *rest = get_players(game_settings.players_count_to_start)
        add_game_players(game, rest)

        game.add_player(player)

        assert game.state == enums.GameState.START_WAITING

    def test_remove_player_player_removed(self) -> None:
        game = get_game()
        player, *_ = get_players(1)
        game.add_player(player)

        game.remove_player(player)

        assert len(game._players) == 0

    def test_remove_player_player_removed_event_registered(self) -> None:
        game = get_game()
        player, *_ = get_players(1)
        game.add_player(player)

        game.remove_player(player)

        registered_events = game.collect_events()
        expected_event = events.PlayerRemoved(
            game_id=game.id,
            player_id=player.id,
            username=player.username,
        )
        assert expected_event in registered_events

    def test_start_game_started_state_setted(self) -> None:
        game = get_game()
        players = get_players(game_settings.players_count_to_start)
        add_game_players(game, players)

        game.start()

        assert game.state == enums.GameState.STARTED

    def test_start_game_started_event_registered(self) -> None:
        game = get_game()
        players = get_players(game_settings.players_count_to_start)
        add_game_players(game, players)

        game.start()

        registered_events = game.collect_events()
        expected_event = events.GameStarted(game_id=game.id)
        assert expected_event in registered_events

    def test_start_round_number_one_setted(self) -> None:
        game = get_game()
        players = get_players(game_settings.players_count_to_start)
        add_game_players(game, players)

        game.start()

        assert game.round_number == 1
