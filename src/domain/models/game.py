from core.settings import game_settings

from domain import enums, events, exceptions
from domain.models.duel import Duel
from domain.models.field import Field
from domain.models.model import Model
from domain.models.player import Player
from domain.models.strategies import PlayerTurnSelector


class Game(Model):
    def __init__(
        self,
        id: int,
        state: enums.GameState,
        round_number: int,
        player_order: Player,
        players: list[Player],
        fields: list[Field],
        duel: Duel,
    ) -> None:
        super().__init__()
        self._id = id
        self._state = state
        self._round_number = round_number
        self._player_order = player_order
        self._players = players
        self._fields = fields
        self._duel = duel

    def __repr__(self) -> str:
        return """Game(id={}, state={}, round_number={}, player_order={}, players={}, fields={}, duel={})""".format(
            self._id,
            self._state,
            self._round_number,
            self._player_order,
            self._players,
            self._fields,
            self._duel,
        )

    def add_player(self, player: Player) -> None:
        self._ensure_can_add_player(player)
        self._add_player(player)

    def remove_player(self, player: Player) -> None:
        self._remove_player(player)

    def try_start(self) -> None:
        if self.is_full():
            self.start()

    def start(self) -> None:
        self._round_number = 1
        self._state = enums.GameState.IN_PROCESS
        self.register_event(events.GameStarted(game_id=self._id))

    def start_round(self, player_turn_selector: PlayerTurnSelector) -> None:
        self._state = enums.GameState.ATTACK_WAITING
        self._player_order = player_turn_selector.select(self._round_number, self._players)
        self.register_event(
            events.RoundStarted(
                game_id=self._id,
                round_number=self._round_number,
                player_order_id=self._player_order.get_id(),
            ),
        )

    def attack_field(self, player: Player, field: Field) -> None:
        self._ensure_can_attack_field(player, field)
        self._attack_field(player, field)

    def finish_round(self) -> None:
        self._state = enums.GameState.IN_PROCESS
        self.register_event(events.RoundFinished(game_id=self._id, round_number=self._round_number))

    def start_duel(self, attacker: Player, defender: Player, field: Field) -> None:
        self._state = enums.GameState.DUELING
        self._duel.start(attacker, defender, field)
        self.register_event(
            events.DuelStarted(
                game_id=self._id,
                attacker_id=attacker.get_id(),
                defender_id=defender.get_id(),
                field_id=field.get_id(),
            ),
        )

    def set_duel_category(self, category_id: int) -> None:
        self._duel.set_category(category_id)
        self.register_event(events.CategorySetted(game_id=self._id, category_id=category_id))

    def set_duel_question(self, question_id: int) -> None:
        self._duel.set_question(question_id)
        self.register_event(events.QuestionSetted(game_id=self._id, question_id=question_id))

    def set_player_answer(self, player: Player, answer_id: int) -> None:
        self._duel.set_player_answer(player, answer_id)
        self.register_event(events.PlayerAnswered(game_id=self._id, player_id=player.get_id()))

    def are_all_players_answered(self) -> bool:
        return self._duel.are_all_players_answered()

    def finish_duel(self) -> None:
        self._state = enums.GameState.IN_PROCESS
        self._duel.finish()
        self.register_event(events.DuelEnded(game_id=self._id))

    def start_duel_round(self) -> None:
        self._duel.start_round()
        self.register_event(
            events.DuelRoundStarted(
                game_id=self._id,
                round_number=self._duel.get_round_number(),
                category_id=self._duel.get_category_id(),
            ),
        )

    def finish(self) -> None:
        self._state = enums.GameState.ENDED
        self.register_event(events.GameEnded(game_id=self._id))

    def try_finish_duel_round(self) -> None:
        if self.are_all_players_answered():
            self.finish_duel_round()

    def set_duel_correct_answer(self, answer_id: int) -> None:
        self._duel.set_correct_answer_id(answer_id)

    def finish_duel_round(self) -> None:
        self._duel.finish_round()
        self.register_event(
            events.DuelRoundFinished(
                game_id=self._id,
                round_number=self._duel.get_round_number(),
                correct_answer_id=self._duel.get_correct_answer_id(),
            ),
        )

    def check_duel_results(self) -> None:
        field = self._duel.get_field()
        if self._duel.is_attacker_won():
            attacker = self._duel.get_attacker()
            self.register_event(
                events.FieldCaptured(
                    game_id=self._id,
                    field_id=field.get_id(),
                    capturer_id=attacker.get_id(),
                ),
            )
        else:
            self.register_event(events.FieldDefended(game_id=self._id, field_id=field.get_id()))

    def check_round_outcome(self, player_turn_selector: PlayerTurnSelector) -> None:
        if self._round_number == game_settings.max_rounds:
            self.finish()
        else:
            self._increase_round_number(1)
            self.start_round(player_turn_selector)

    def check_duel_round_outcome(self) -> None:
        if self._duel.check_round_outcome():
            self.finish_duel()
        else:
            self._increase_duel_round_number(1)
            self.start_duel_round()

    def check_attack_outcome(self, player: Player, field: Field) -> None:
        if field.is_captured():
            self._start_duel(player, field)
        else:
            self._capture_field(player, field)

    def get_duel_category(self) -> int:
        return self._duel.get_category_id()

    def _increase_round_number(self, value: int = 1) -> None:
        self._round_number += value

    def _increase_duel_round_number(self, value: int = 1) -> None:
        self._duel.increase_round_number(value)

    def _ensure_can_add_player(self, player: Player) -> None:
        if self._state != enums.GameState.PLAYERS_WAITING:
            raise exceptions.GameInvalidState(self._state)
        if self.is_full():
            raise exceptions.GameIsFull()
        # if player in self._players:
        #     raise exceptions.PlayerAlreadyAdded()

    def _add_player(self, player: Player) -> None:
        self._players.append(player)
        self.register_event(events.PlayerAdded(game_id=self._id, player_id=player.get_id()))

    def _remove_player(self, player: Player) -> None:
        if player not in self._players:
            return
        self._players.remove(player)
        self.register_event(events.PlayerRemoved(game_id=self._id, player_id=player.get_id()))

    def _ensure_can_attack_field(self, player: Player, field: Field) -> None:
        if self._state != enums.GameState.ATTACK_WAITING:
            raise exceptions.GameInvalidState(self._state)
        if field.get_owner() == player:
            raise exceptions.AlreadyOwned()
        if self._player_order != player:
            raise exceptions.NotYourTurn()

    def _attack_field(self, player: Player, field: Field) -> None:
        self.register_event(
            events.FieldAttacked(
                game_id=self._id,
                attacker_id=player.get_id(),
                field_id=field.get_id(),
            ),
        )

    def is_full(self) -> bool:
        return len(self._players) == game_settings.players_count_to_start

    def _capture_field(self, capturer: Player, field: Field) -> None:
        field.set_owner(capturer)
        self.register_event(
            events.FieldCaptured(
                game_id=self._id,
                field_id=field.get_id(),
                capturer_id=capturer.get_id(),
            ),
        )

    def _start_duel(self, player: Player, field: Field) -> None:
        self._state = enums.GameState.DUELING
        field_owner = field.get_owner()
        self.register_event(
            events.PlayerFieldAttacked(
                game_id=self._id,
                attacker_id=player.get_id(),
                defender_id=field_owner.get_id(),
                field_id=field.get_id(),
            ),
        )
