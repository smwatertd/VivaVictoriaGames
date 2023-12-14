from domain.models.answer import Answer
from domain.models.category import Category
from domain.models.field import Field
from domain.models.player import Player
from domain.models.question import Question


class Duel:
    def __init__(
        self,
        id: int,
        attacker: Player,
        defender: Player,
        field: Field,
        category: Category,
        question: Question,
        round_number: int,
    ) -> None:
        self.id = id
        self.round_number = round_number
        self._attacker = attacker
        self._defender = defender
        self._category = category
        self._question = question
        self._field = field

    def __repr__(self) -> str:
        return (
            f'Duel(id={self.id}, round_number={self.round_number}, attacker={self._attacker}, '
            f'defender={self._defender}, category={self._category}, question={self._question}, '
            f'field={self._field})'
        )

    def start(self, attacker: Player, defender: Player, field: Field) -> None:
        self.round_number = 1
        self._attacker = attacker
        self._defender = defender
        self._field = field

    def set_category(self, category: Category) -> None:
        self._category = category

    def set_question(self, question: Question) -> None:
        self._question = question

    def set_player_answer(self, player: Player, answer: Answer) -> None:
        player.set_answer(answer)

    def are_all_players_answered(self) -> bool:
        return self._attacker.is_answered() and self._defender.is_answered()

    def increase_round_number(self, value: int = 1) -> None:
        self.round_number += value
