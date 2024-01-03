from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from domain.models.marking_conflict import MarkingConflict
    from domain.models import Player
    from domain.models import Answer


class ConflictResolver(ABC):
    @abstractmethod
    def get_winner(self, conflict: 'MarkingConflict', correct_answer: 'Answer') -> 'Player':
        pass


class AnsweredByConflictResolver(ConflictResolver):
    def get_winner(self, conflict: 'MarkingConflict', correct_answer: 'Answer') -> 'Player':
        players = list(conflict.players)
        correct_answered = self._get_correct_answered_players(players, correct_answer)
        if correct_answered:
            return self._get_earliest_answered_player(correct_answered)
        return self._get_earliest_wrong_answered_player(players)

    def _get_correct_answered_players(self, players: list['Player'], correct_answer: 'Answer') -> list['Player']:
        return [player for player in players if player.get_answer() == correct_answer]

    def _get_earliest_answered_player(self, players: list['Player']) -> 'Player':
        return min(players, key=lambda player: player.get_answered_at())

    def _get_earliest_wrong_answered_player(self, players: list['Player']) -> 'Player':
        return min(players, key=lambda player: (player.is_answered(), player.get_answered_at(), player.get_id()))
