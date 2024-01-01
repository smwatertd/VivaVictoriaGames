from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from domain.models.marking_conflict import MarkingConflict
    from domain.models import Player


class ConflictResolver(ABC):
    @abstractmethod
    def get_winner(self, conflict: 'MarkingConflict', correct_answer: int) -> 'Player':
        pass
