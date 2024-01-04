from core.settings import game_settings

from domain import value_objects
from domain.models.captured_field import CapturedField
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

    def start(self, attacker: Player, defender: Player, field: CapturedField, category: value_objects.Category) -> None:
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

    def set_correct_answer(self, answer: value_objects.Answer) -> None:
        self._correct_answer_id = answer.id

    def get_category(self) -> value_objects.BasicCategory:
        return value_objects.BasicCategory(id=self._category_id)

    def are_all_players_answered(self) -> bool:
        return self._attacker.is_answered() and self._defender.is_answered()

    def is_continuing(self) -> bool:
        attacker_answer = self._attacker.get_answer()
        defender_answer = self._defender.get_answer()
        finished_by_round_number = self._round_number - 1 == game_settings.duel_max_rounds
        is_both_lost = attacker_answer.id != self._correct_answer_id and defender_answer.id != self._correct_answer_id
        is_both_won = attacker_answer.id == self._correct_answer_id and defender_answer.id == self._correct_answer_id
        return not finished_by_round_number and (is_both_lost or is_both_won)

    def stop(self) -> value_objects.DuelResult:
        if (
            self._attacker.get_answer().id == self._correct_answer_id
            and self._defender.get_answer().id != self._correct_answer_id
        ):
            self._field.set_owner(self._attacker)
            self._field.on_capture()
            result = value_objects.DuelResult(is_captured=True, field=self._field)
        else:
            self._field.on_defend()
            result = value_objects.DuelResult(is_captured=False, field=self._field)

        self._defender.clear_answer()
        self._attacker.clear_answer()
        self._defender = None
        self._attacker = None
        self._field = None
        self._category_id = None
        self._correct_answer_id = None
        self._round_number = 0

        return result

    def get_players(self) -> list[Player]:
        return [self._attacker, self._defender]

    def get_correct_answer(self) -> value_objects.Answer:
        return value_objects.Answer(id=self._correct_answer_id)
