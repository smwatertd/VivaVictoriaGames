from domain import events, exceptions
from domain.enums import GameState
from domain.models import Duel, Game, Player

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

    def test_start_round_player_order_setted(self, started_game: Game) -> None:
        started_game.start_round()

        player_order = self._get_game_player_order(started_game)
        assert started_game._player_order == player_order

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

    def test_finish_round_state_setted(self, round_processing_game: Game) -> None:
        round_processing_game.finish_round()

        assert round_processing_game._state == GameState.IN_PROCESS

    def test_finish_round_event_registered(self, round_processing_game: Game) -> None:
        round_processing_game.finish_round()

        assert (
            events.RoundFinished(
                game_id=round_processing_game._id,
                round_number=round_processing_game._round_number,
            )
            in round_processing_game._events
        )

    def test_attack_field_event_registered(self, round_processing_game: Game) -> None:
        attacker = round_processing_game._player_order
        field = round_processing_game._fields[0]

        round_processing_game.attack_field(attacker, field)

        assert (
            events.FieldAttacked(
                game_id=round_processing_game._id,
                attacker_id=attacker._id,
                field_id=field._id,
            )
            in round_processing_game._events
        )

    def test_attack_field_invalid_state(self, started_game: Game) -> None:
        attacker = started_game._player_order
        field = started_game._fields[0]

        with pytest.raises(
            exceptions.GameNotWaitingForAttack,
            match=f'Game not waiting for attack. Game state: {started_game._state}',
        ):
            started_game.attack_field(attacker, field)

    def test_attack_field_already_owned(self, round_processing_game: Game) -> None:
        attacker = round_processing_game._player_order
        field = round_processing_game._fields[1]
        field._owner = attacker

        with pytest.raises(exceptions.FieldAlreadyOwned, match=f'Field already owned. Field id: {field._id}'):
            round_processing_game.attack_field(attacker, field)

    def test_attack_field_not_player_order(self, round_processing_game: Game) -> None:
        not_player_order = self._get_not_player_order(round_processing_game)
        field = round_processing_game._fields[0]

        with pytest.raises(exceptions.NotYourTurn):
            round_processing_game.attack_field(not_player_order, field)

    def test_start_duel_state_setted(self, round_processing_game: Game) -> None:
        attacker = round_processing_game._player_order
        defender = self._get_not_player_order(round_processing_game)
        field = round_processing_game._fields[0]

        round_processing_game.start_duel(attacker, defender, field)

        assert round_processing_game._state == GameState.DUELING

    def test_start_duel_event_registered(self, round_processing_game: Game, mock_duel: Duel) -> None:
        attacker = round_processing_game._player_order
        defender = self._get_not_player_order(round_processing_game)
        round_processing_game._duel = mock_duel
        field = round_processing_game._fields[0]

        round_processing_game.start_duel(attacker, defender, field)

        assert (
            events.DuelStarted(
                game_id=round_processing_game._id,
                attacker_id=attacker._id,
                defender_id=defender._id,
                field_id=field._id,
            )
            in round_processing_game._events
        )

    def test_start_duel_duel_started(self, round_processing_game: Game, mock_duel: Duel) -> None:
        attacker = round_processing_game._player_order
        defender = self._get_not_player_order(round_processing_game)
        round_processing_game._duel = mock_duel
        field = round_processing_game._fields[0]

        round_processing_game.start_duel(attacker, defender, field)

        assert mock_duel.start.called_once_with(attacker, defender, field)

    def test_set_duel_category_category_setted(
        self,
        duel_processing_game: Game,
        category: int,
        mock_duel: Duel,
    ) -> None:
        duel_processing_game._duel = mock_duel

        assert mock_duel.set_category.called_once_with(category)

    def test_set_duel_category_event_registered(self, category: int, duel_processing_game: Game) -> None:
        duel_processing_game.set_duel_category(category)

        assert (
            events.CategorySetted(
                game_id=duel_processing_game._id,
                category_id=category,
            )
            in duel_processing_game._events
        )

    def test_set_duel_question_question_setted(
        self,
        duel_processing_game: Game,
        question: int,
        mock_duel: Duel,
    ) -> None:
        duel_processing_game._duel = mock_duel

        assert mock_duel.set_question.called_once_with(question)

    def test_set_duel_question_event_registered(self, question: int, duel_processing_game: Game) -> None:
        duel_processing_game.set_duel_question(question)

        assert (
            events.QuestionSetted(
                game_id=duel_processing_game._id,
                question_id=question,
            )
            in duel_processing_game._events
        )

    def _get_game_order(self, game: Game) -> list[Player]:
        return game._player_turn_selector.get_order(game._players)

    def _get_game_player_order(self, game: Game) -> Player:
        return game._player_turn_selector.select(game._round_number, game._players)

    def _get_not_player_order(self, game: Game) -> Player:
        return next(player for player in game._players if player != game._player_order)
