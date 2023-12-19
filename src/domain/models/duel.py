from core.settings import game_settings

from domain.models.field import Field
from domain.models.player import Player


class Duel:
    def __init__(
        self,
        id: int,
        round_number: int,
        attacker: Player,
        defender: Player,
        field: Field,
        category_id: int,
        question_id: int,
    ) -> None:
        self._id = id
        self._round_number = round_number
        self._attacker = attacker
        self._defender = defender
        self._category_id = category_id
        self._question_id = question_id
        self._field = field

    def __repr__(self) -> str:
        return (
            f'Duel(id={self._id}, round_number={self._round_number}, attacker={self._attacker}, '
            f'defender={self._defender}, category={self._category_id}, question={self._question_id}, '
            f'field={self._field})'
        )

    def start(self, attacker: Player, defender: Player, field: Field) -> None:
        self._round_number = 1
        self._attacker = attacker
        self._defender = defender
        self._field = field
        self._reset_members_answers()

    def set_category(self, category_id: int) -> None:
        self._category_id = category_id

    def set_question(self, question_id: int) -> None:
        self._question_id = question_id

    def set_player_answer(self, player: Player, answer_id: int) -> None:
        player.set_answer(answer_id)

    def are_all_players_answered(self) -> bool:
        return self._attacker.is_answered() and self._defender.is_answered()

    def increase_round_number(self, value: int = 1) -> None:
        self._round_number += value

    def is_attacker_won(self) -> bool:
        return self._field.get_owner() == self._attacker

    def get_attacker(self) -> Player:
        return self._attacker

    def get_field(self) -> Field:
        return self._field

    def get_round_number(self) -> int:
        return self._round_number

    def set_correct_answer_id(self, answer_id: int) -> None:
        self._correct_answer_id = answer_id

    def get_correct_answer_id(self) -> int:
        return self._correct_answer_id

    def check_round_outcome(self) -> bool:
        return (
            self._round_number == game_settings.duel_max_rounds
            or (
                self._attacker._answer_id == self._correct_answer_id
                and self._defender._answer_id != self._correct_answer_id
            )
            or (
                self._defender.get_answer_id() == self._correct_answer_id
                and self._attacker.get_answer_id() != self._correct_answer_id
            )
        )

    def finish_round(self) -> None:
        pass

    def finish(self) -> None:
        if (
            self._attacker.is_answered()
            and self._attacker.get_answer_id() == self._correct_answer_id
            and self._defender.get_answer_id() != self._correct_answer_id
        ):
            self._field.set_owner(self._attacker)
        self._reset_members_answers()

    def start_round(self) -> None:
        self._reset_members_answers()

    def _reset_members_answers(self) -> None:
        self._attacker.reset_answer_id()
        self._defender.reset_answer_id()
