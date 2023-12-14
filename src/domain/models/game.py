from core.settings import game_settings

from domain import enums, events, exceptions
from domain.models.answer import Answer
from domain.models.category import Category
from domain.models.duel import Duel
from domain.models.field import Field
from domain.models.model import Model
from domain.models.player import Player
from domain.models.question import Question
from domain.models.strategies import IdentityPlayerTurnSelector

selector = IdentityPlayerTurnSelector()


class Game(Model):
    def __init__(
        self,
        id: int,
        state: enums.GameState,
        round_number: int,
        players: list[Player],
        fields: list[Field],
        duel: Duel,
    ) -> None:
        super().__init__()
        self.id = id
        self.state = state
        self.round_number = round_number
        self._players = players
        self._fields = fields
        self._duel = duel

    def __repr__(self) -> str:
        return """Game(id={}, state={}, round_number={}, players={}, fields={}, duel={})""".format(
            self.id,
            self.state,
            self.round_number,
            self._players,
            self._fields,
            self._duel,
        )

    def add_player(self, player: Player) -> None:
        self._ensure_can_add_player(player)
        self._add_player(player)

    def remove_player(self, player: Player) -> None:
        self._remove_player(player)

    def start(self) -> None:
        self.round_number = 1
        self.state = enums.GameState.IN_PROCESS
        self.register_event(events.GameStarted(game_id=self.id))

    def start_round(self) -> None:
        self.state = enums.GameState.ATTACK_WAITING
        player_order = selector.select(self.round_number, self._players)
        self.register_event(
            events.RoundStarted(
                game_id=self.id,
                round_number=self.round_number,
                player_order_id=player_order.id,
            ),
        )

    def attack_field(self, player: Player, field: Field) -> None:
        self._ensure_can_attack_field(player, field)
        self._attack_field(player, field)

    def finish_round(self) -> None:
        self.state = enums.GameState.IN_PROCESS
        self.register_event(events.RoundFinished(game_id=self.id, round_number=self.round_number))

    def start_duel(self, attacker: Player, defender: Player, field: Field) -> None:
        self.state = enums.GameState.DUELING
        self._duel.start(attacker, defender, field)
        self.register_event(
            events.DuelStarted(
                game_id=self.id,
                attacker_id=attacker.id,
                defender_id=defender.id,
                field_id=field.id,
            ),
        )

    def set_duel_category(self, category: Category) -> None:
        self._duel.set_category(category)
        self.register_event(
            events.CategorySetted(
                game_id=self.id,
                category_id=category.id,
            ),
        )

    def set_duel_question(self, question: Question) -> None:
        self._duel.set_question(question)
        self.register_event(events.QuestionSetted(game_id=self.id, question_id=question.id))

    def set_player_answer(self, player: Player, answer: Answer) -> None:
        self._duel.set_player_answer(player, answer)
        self.register_event(
            events.PlayerAnswered(game_id=self.id, player_id=player.id),
        )

    def are_all_players_answered(self) -> bool:
        return self._duel.are_all_players_answered()

    def finish_duel(self) -> None:
        self.register_event(
            events.DuelEnded(
                game_id=self.id,
            ),
        )

    def start_duel_round(self) -> None:
        self.register_event(
            events.DuelRoundStarted(
                game_id=self.id,
                round_number=self._duel.round_number,
            ),
        )

    def finish(self) -> None:
        self.state = enums.GameState.ENDED
        self.register_event(
            events.GameEnded(
                game_id=self.id,
            ),
        )

    def finish_duel_round(self) -> None:
        [correct_answer] = list(filter(lambda answer: answer.is_correct, self._duel._question._answers))
        self.register_event(
            events.DuelRoundFinished(
                game_id=self.id,
                round_number=self._duel.round_number,
                correct_answer_id=correct_answer.id,
            ),
        )

    def increase_round_number(self, value: int = 1) -> None:
        self.round_number += value

    def increase_duel_round_number(self, value: int = 1) -> None:
        self._duel.increase_round_number(value)

    def _ensure_can_add_player(self, player: Player) -> None:
        if self.state != enums.GameState.PLAYERS_WAITING:
            raise exceptions.GameInvalidState(self.state)
        if self.is_full():
            raise exceptions.GameIsFull()
        # if player in self._players:
        #     raise exceptions.PlayerAlreadyAdded()

    def _add_player(self, player: Player) -> None:
        self._players.append(player)
        self.register_event(
            events.PlayerAdded(
                game_id=self.id,
                player_id=player.id,
            ),
        )

    def _remove_player(self, player: Player) -> None:
        if player not in self._players:
            return
        self._players.remove(player)
        self.register_event(
            events.PlayerRemoved(
                game_id=self.id,
                player_id=player.id,
            ),
        )

    def _ensure_can_attack_field(self, player: Player, field: Field) -> None:
        if self.state != enums.GameState.ATTACK_WAITING:
            raise exceptions.GameInvalidState(self.state)
        if field.get_owner() == player:
            raise exceptions.AlreadyOwned()
        if selector.select(self.round_number, self._players) != player:
            raise exceptions.NotYourTurn()

    def _attack_field(self, player: Player, field: Field) -> None:
        if field.is_captured():
            self._start_duel(player, field)
        else:
            self._capture_field(player, field)

    def is_full(self) -> bool:
        return len(self._players) == game_settings.players_count_to_start

    def _capture_field(self, capturer: Player, field: Field) -> None:
        field.set_owner(capturer)
        self.register_event(
            events.FieldCaptured(
                game_id=self.id,
                field_id=field.id,
                capturer_id=capturer.id,
            ),
        )

    def _start_duel(self, player: Player, field: Field) -> None:
        self.state = enums.GameState.DUELING
        field_owner = field.get_owner()
        self.register_event(
            events.PlayerFieldAttacked(
                game_id=self.id,
                attacker_id=player.id,
                defender_id=field_owner.id,
                field_id=field.id,
            ),
        )
