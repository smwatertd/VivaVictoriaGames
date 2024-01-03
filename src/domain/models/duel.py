from core.settings import game_settings

from domain.models.answer import Answer
from domain.models.captured_field import CapturedField
from domain.models.category import Category
from domain.models.duel_result import DuelResult, ResultType
from domain.models.player import Player


class Duel:
    def __init__(
        self,
        id: int,
        round_number: int,
        category_id: int | None,
        correct_answer_id: int | None,
        attacker: Player,
        defender: Player,
        field: CapturedField,
    ) -> None:
        self._id = id
        self._round_number = round_number
        self._category_id = category_id
        self._correct_answer_id = correct_answer_id
        self._attacker = attacker
        self._defender = defender
        self._field = field

    def start(self, attacker: Player, defender: Player, field: CapturedField, category: Category) -> None:
        self._round_number = 1
        self._attacker = attacker
        self._defender = defender
        self._field = field
        self._category_id = category.id

    def get_round_number(self) -> int:
        return self._round_number

    def start_round(self) -> None:
        self._correct_answer_id = None
        self._attacker.clear_answer()
        self._defender.clear_answer()

    def finish_round(self) -> None:
        self._round_number += 1

    def set_correct_answer(self, answer: Answer) -> None:
        self._correct_answer_id = answer.id

    def get_category(self) -> Category:
        return Category(id=self._category_id, name='')

    def set_player_answer(self, player: Player, answer: int) -> None:
        if player == self._attacker:
            self._attacker.set_answer(answer)
        else:
            self._defender.set_answer(answer)

    def are_all_players_answered(self) -> bool:
        return self._attacker.is_answered() and self._defender.is_answered()

    def is_continuing(self) -> bool:
        attacker_answer = self._attacker.get_answer()
        defender_answer = self._defender.get_answer()
        finished_by_round_number = self._round_number - 1 == game_settings.duel_max_rounds
        is_both_lost = attacker_answer.id != self._correct_answer_id and defender_answer.id != self._correct_answer_id
        is_both_won = attacker_answer.id == self._correct_answer_id and defender_answer.id == self._correct_answer_id
        return not finished_by_round_number and (is_both_lost or is_both_won)

    def stop(self) -> DuelResult:
        if (
            self._attacker.get_answer().id == self._correct_answer_id
            and self._defender.get_answer().id != self._correct_answer_id
        ):
            self._field.set_owner(self._attacker)
            self._field.on_capture()
            result = DuelResult(result_type=ResultType.CAPTURED, field=self._field)
        else:
            self._field.on_defend()
            result = DuelResult(result_type=ResultType.DEFENDED, field=self._field)

        self._defender.clear_answer()
        self._attacker.clear_answer()
        self._defender = None
        self._attacker = None
        self._field = None
        self._category_id = None
        self._correct_answer_id = None
        self._round_number = 0

        return result
