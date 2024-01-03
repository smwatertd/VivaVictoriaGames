from domain.models.answer import Answer
from domain.models.category import Category
from domain.models.duel import Duel
from domain.models.duel_result import DuelResult
from domain.models.field import Field
from domain.models.player import Player


class Battle:
    def __init__(self, id: int, round_number: int, duel: Duel) -> None:
        self._id = id
        self._round_number = round_number
        self._duel = duel

    def start(self) -> None:
        self._round_number = 1

    def finish_round(self) -> None:
        self._round_number += 1

    def get_round_number(self) -> int:
        return self._round_number

    def start_duel(self, attacker: Player, defender: Player, field: Field, category: Category) -> None:
        self._duel.start(attacker, defender, field.get_captured_field(), category)

    def get_duel_round(self) -> int:
        return self._duel.get_round_number()

    def start_duel_round(self) -> None:
        self._duel.start_round()

    def finish_duel_round(self) -> None:
        self._duel.finish_round()

    def get_duel_category(self) -> Category:
        return self._duel.get_category()

    def set_duel_correct_answer(self, answer: Answer) -> None:
        self._duel.set_correct_answer(answer)

    def set_player_answer(self, player: Player, answer: int) -> None:
        self._duel.set_player_answer(player, answer)

    def are_all_duel_players_answered(self) -> bool:
        return self._duel.are_all_players_answered()

    def is_duel_continuing(self) -> bool:
        return self._duel.is_continuing()

    def stop_duel(self) -> DuelResult:
        return self._duel.stop()
