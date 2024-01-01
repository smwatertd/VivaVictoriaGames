from typing import Iterable

from domain.models.capture_round_result import CaptureRoundResult
from domain.models.field import Field
from domain.models.marked_field import MarkField
from domain.models.marking_conflict import MarkingConflict
from domain.models.player import Player
from domain.resolvers import ConflictResolver


class Capture:
    def __init__(
        self,
        id: int,
        round_number: int,
        correct_answer_id: int | None,
        marked_fields: list[MarkField],
        conflict_resolver: ConflictResolver,
    ) -> None:
        self._id = id
        self._round_number = round_number
        self._correct_answer_id = correct_answer_id
        self._marked_fields = marked_fields
        self._conflict_resolver = conflict_resolver

    def get_round_number(self) -> int:
        return self._round_number

    def set_correct_answer(self, answer: int) -> None:
        self._correct_answer_id = answer

    def start(self) -> None:
        self._round_number = 1

    def start_round(self) -> None:
        self._marked_fields = []
        self._correct_answer_id = None

    def mark_field(self, player: Player, field: Field) -> None:
        if self._is_field_already_marked(field):
            self._get_marked_field(field).add_player(player)
        else:
            self._add_new_marked_field(player, field)

    def has_marking_conflict(self) -> bool:
        return any(len(marked_field.get_players()) > 1 for marked_field in self._marked_fields)

    def stop_round(self) -> list[CaptureRoundResult]:
        self._round_number += 1
        return self._capture_marked_fields()

    def get_marking_conflict(self) -> MarkingConflict:
        marked_field = [marked_field for marked_field in self._marked_fields if len(marked_field.get_players()) > 1][0]
        return MarkingConflict(marked_field.get_players(), marked_field.get_field())

    def set_player_answer(self, player: Player, answer: int) -> None:
        player.set_answer(answer)

    def are_all_conflict_players_answered(self) -> bool:
        conflict = self.get_marking_conflict()
        return all(player.is_answered() for player in conflict.players)

    def stop_battle(self) -> None:
        conflict = self.get_marking_conflict()
        players = list(conflict.players)
        self._resolve_conflict(conflict)
        self._clear_players_answer(players)

    def _capture_marked_fields(self) -> list[CaptureRoundResult]:
        captured_fields = []
        for marked_field in self._marked_fields:
            # marked_field.capture()
            player = marked_field.get_single_player()
            player.capture(marked_field.get_field())
            player.clear_marked_field()
            captured_fields.append(
                CaptureRoundResult(
                    field_id=marked_field.get_field().get_id(),
                    new_field_value=marked_field.get_field().get_value(),
                    player_id=player.get_id(),
                ),
            )
        return captured_fields

    def _is_field_already_marked(self, field: Field) -> bool:
        try:
            self._get_marked_field(field)
            return True
        except ValueError:
            return False

    def _get_marked_field(self, field: Field) -> MarkField:
        for marked_field in self._marked_fields:
            if marked_field.get_field() == field:
                return marked_field
        raise ValueError('Field is not marked')

    def _add_new_marked_field(self, player: Player, field: Field) -> None:
        marked_field = MarkField(field, [player])
        self._marked_fields.append(marked_field)

    def _resolve_conflict(self, conflict: MarkingConflict) -> None:
        winner = self._conflict_resolver.get_winner(conflict, self._correct_answer_id)
        self._clear_marked_field_for_players(set(conflict.players) - {winner})

    def _clear_players_answer(self, players: Iterable[Player]) -> None:
        for player in players:
            player.clear_answer()

    def _clear_marked_field_for_players(self, players: Iterable[Player]) -> None:
        for player in players:
            player.clear_marked_field()
