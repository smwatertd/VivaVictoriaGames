from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from domain.models.marking_conflict import MarkingConflict
    from domain.models import Player


class ConflictResolver(ABC):
    @abstractmethod
    def get_winner(self, conflict: 'MarkingConflict', correct_answer: int) -> 'Player':
        pass


class AnsweredByConflictResolver(ConflictResolver):
    def get_winner(self, conflict: 'MarkingConflict', correct_answer: int) -> 'Player':
        correct_answered = [player for player in conflict.players if player.get_answer() == correct_answer]

        if correct_answered:
            return sorted(correct_answered, key=lambda player: player.get_answered_at(), reverse=True)[0]
        return sorted(
            conflict.players,
            key=lambda player: (player.is_answered(), player.get_answered_at(), player.get_id()),
            reverse=True,
        )[0]
