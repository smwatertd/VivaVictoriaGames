from domain import value_objects
from domain.models.duel import Duel
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

    def start_duel(self, attacker: Player, defender: Player, field: Field, category: value_objects.Category) -> None:
        self._duel.start(attacker, defender, field.get_captured_field(), category)

    def get_duel_round(self) -> int:
        return self._duel.get_round_number()

    def start_duel_round(self) -> None:
        self._duel.start_round()

    def finish_duel_round(self) -> None:
        self._duel.finish_round()

    def get_duel_category(self) -> value_objects.Category:
        return self._duel.get_category()

    def set_duel_correct_answer(self, answer: value_objects.Answer) -> None:
        self._duel.set_correct_answer(answer)

    def are_all_duel_players_answered(self) -> bool:
        return self._duel.are_all_players_answered()

    def is_duel_continuing(self) -> bool:
        return self._duel.is_continuing()

    def stop_duel(self) -> value_objects.DuelResult:
        return self._duel.stop()

    def get_duel_players(self) -> list[Player]:
        return self._duel.get_players()

    def get_duel_correct_answer(self) -> value_objects.Answer:
        return self._duel.get_correct_answer()
