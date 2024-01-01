from core.settings import game_settings

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

    def start(self, attacker: Player, defender: Player, field: CapturedField) -> None:
        self._round_number = 1
        self._attacker = attacker
        self._defender = defender
        self._field = field

    def set_category(self, category_id: int) -> None:
        self._category_id = category_id

    def get_round_number(self) -> int:
        return self._round_number

    def start_round(self) -> None:
        self._correct_answer_id = None
        self._attacker.clear_answer()
        self._defender.clear_answer()

    def set_correct_answer(self, answer: int) -> None:
        self._correct_answer_id = answer

    def set_player_answer(self, player: Player, answer: int) -> None:
        if player == self._attacker:
            self._attacker.set_answer(answer)
        else:
            self._defender.set_answer(answer)

    def are_all_players_answered(self) -> bool:
        return self._attacker.is_answered() and self._defender.is_answered()

    def is_continuing(self) -> bool:
        return not (
            (
                self._attacker.get_answer() == self._correct_answer_id
                and self._defender.get_answer() != self._correct_answer_id
            )
            or self._round_number == game_settings.duel_max_rounds
        )

    def stop(self) -> None:
        if self._attacker.get_answer() == self._correct_answer_id:
            if self._defender.get_answer() != self._correct_answer_id:
                self._field.set_owner(self._attacker)
            else:
                self._field.on_defend()

        self._defender.clear_answer()
        self._attacker.clear_answer()
        self._defender = None
        self._attacker = None
        self._field = None
        self._category_id = None
        self._correct_answer_id = None
        self._round_number = 0
