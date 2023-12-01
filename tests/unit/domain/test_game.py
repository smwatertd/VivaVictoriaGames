from core.settings import game_settings

from domain import enums, events, exceptions, models
from domain.models.strategies import PlayerTurnSelector

import pytest


def get_players(players_count: int) -> list[models.Player]:
    return [models.Player(id=i, username=f'player_{i}') for i in range(1, players_count + 1)]


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


class FakePlayerTurnSelector(PlayerTurnSelector):
    def __init__(self) -> None:
        self.is_called = False

    def select(self, round_number: int, players: list[models.Player]) -> models.Player:
        self.is_called = True
        return players[0]


def get_fields(fieds_count: int) -> list[models.Field]:
    return [models.Field(id=i) for i in range(1, fieds_count + 1)]


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

        assert enums.GameState.STARTED == game.state

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

    def test_select_player_turn_player_turn_changed_event_registered(self) -> None:
        game = get_game()
        player_turn, *rest = get_players(game_settings.players_count_to_start)
        add_game_players(game, [player_turn, *rest])
        selector = FakePlayerTurnSelector()

        game.select_player_turn(selector)

        registered_events = game.collect_events()
        expected_event = events.PlayerTurnChanged(
            game_id=game.id,
            player_id=player_turn.id,
        )
        assert expected_event in registered_events
        assert selector.is_called

    def test_select_player_turn_attack_waiting_state_setted(self) -> None:
        game = get_game()
        player_turn, *rest = get_players(game_settings.players_count_to_start)
        add_game_players(game, [player_turn, *rest])
        selector = FakePlayerTurnSelector()

        game.select_player_turn(selector)

        assert enums.GameState.ATTACK_WAITING == game.state

    def test_attack_field_field_captured(self) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        game = get_game(fields=rest_fields)
        player, *rest_players = get_players(game_settings.players_count_to_start)
        add_game_players(game, [player, *rest_players])
        selector = FakePlayerTurnSelector()
        game.select_player_turn(selector)

        game.attack_field(player, field, selector)

        assert player == field.get_owner()

    def test_attack_field_field_captured_event_registered(self) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        game = get_game(fields=rest_fields)
        player, *rest_players = get_players(game_settings.players_count_to_start)
        add_game_players(game, [player, *rest_players])
        selector = FakePlayerTurnSelector()
        game.select_player_turn(selector)

        game.attack_field(player, field, selector)

        registered_events = game.collect_events()
        expected_event = events.FieldCaptured(
            game_id=game.id,
            field_id=field.id,
            capturer_id=player.id,
        )
        assert expected_event in registered_events

    def test_attack_field_duel_waiting_state_setted(self) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, field_owner, *rest_players = get_players(
            game_settings.players_count_to_start,
        )
        field.set_owner(field_owner)
        game = get_game(fields=rest_fields)
        add_game_players(game, [player, field_owner, *rest_players])
        selector = FakePlayerTurnSelector()
        game.select_player_turn(selector)

        game.attack_field(player, field, selector)

        assert enums.GameState.DUEL_WAITING == game.state

    def test_attack_field_player_field_attacked_events_registered(self) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, field_owner, *rest_players = get_players(
            game_settings.players_count_to_start,
        )
        field.set_owner(field_owner)
        game = get_game(fields=rest_fields)
        add_game_players(game, [player, field_owner, *rest_players])
        selector = FakePlayerTurnSelector()
        game.select_player_turn(selector)

        game.attack_field(player, field, selector)

        registered_events = game.collect_events()
        expected_event = events.PlayerFieldAttacked(
            game_id=game.id,
            attacker_id=player.id,
            defender_id=field_owner.id,
            field_id=field.id,
        )
        assert expected_event in registered_events

    def test_attack_field_invalid_state(
        self,
    ) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, *rest_players = get_players(game_settings.players_count_to_start)
        game = get_game(players=[player, *rest_players], fields=[field, *rest_fields])
        game.state = enums.GameState.DUEL_WAITING
        selector = FakePlayerTurnSelector()

        with pytest.raises(exceptions.GameInvalidState):
            game.attack_field(player, field, selector)

    def test_attack_field_already_owned(
        self,
    ) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, *rest_players = get_players(game_settings.players_count_to_start)
        field.set_owner(player)
        game = get_game(
            state=enums.GameState.ATTACK_WAITING,
            players=[player, *rest_players],
            fields=[field, *rest_fields],
        )
        selector = FakePlayerTurnSelector()

        with pytest.raises(exceptions.AlreadyOwned):
            game.attack_field(player, field, selector)

    def test_attack_field_not_your_turn(
        self,
    ) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, *rest_players = get_players(game_settings.players_count_to_start)
        game = get_game(
            state=enums.GameState.ATTACK_WAITING,
            players=[*rest_players, player],
            fields=[field, *rest_fields],
        )
        selector = FakePlayerTurnSelector()

        with pytest.raises(exceptions.NotYourTurn):
            game.attack_field(player, field, selector)

    def test_start_duel_dueling_state_setted(self) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, field_owner, *rest_players = get_players(
            game_settings.players_count_to_start,
        )
        field.set_owner(field_owner)
        game = get_game(fields=rest_fields)
        add_game_players(game, [player, field_owner, *rest_players])
        selector = FakePlayerTurnSelector()
        game.select_player_turn(selector)

        game.start_duel(player, field, selector)

        assert enums.GameState.DUELING == game.state

    def test_start_duel_duel_started_event_registered(self) -> None:
        field, *rest_fields = get_fields(game_settings.fields_count)
        player, field_owner, *rest_players = get_players(
            game_settings.players_count_to_start,
        )
        field.set_owner(field_owner)
        game = get_game(fields=rest_fields)
        add_game_players(game, [player, field_owner, *rest_players])
        selector = FakePlayerTurnSelector()
        game.select_player_turn(selector)

        game.start_duel(player, field_owner, selector)

        registered_events = game.collect_events()
        expected_event = events.DuelStarted(
            game_id=game.id,
            attacker_id=player.id,
            defender_id=field_owner.id,
            field_id=field.id,
        )
        assert expected_event in registered_events
