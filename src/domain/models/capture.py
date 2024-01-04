from typing import Iterable

from domain import value_objects
from domain.models.field import Field
from domain.models.marked_field import MarkField
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

    def set_correct_answer(self, answer: value_objects.Answer) -> None:
        self._correct_answer_id = answer.id

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

    def stop_round(self) -> None:
        self._round_number += 1

    def get_marking_conflict(self) -> value_objects.MarkingConflict:
        marked_field = [marked_field for marked_field in self._marked_fields if len(marked_field.get_players()) > 1][0]
        return value_objects.MarkingConflict(players=tuple(marked_field.get_players()), field=marked_field.get_field())

    def are_all_conflict_players_answered(self) -> bool:
        conflict = self.get_marking_conflict()
        return all(player.is_answered() for player in conflict.players)

    def capture_marked_fields(self) -> list[Field]:
        captured = []
        for marked_field in self._marked_fields:
            player = marked_field.get_single_player()
            player.capture(marked_field.get_field())
            captured.append(marked_field.get_field())
        return captured

    def finish_marking_battle(self) -> Player:
        conflict = self.get_marking_conflict()
        winner = self._conflict_resolver.get_winner(conflict, self._correct_answer_id)
        self._clear_marked_field_for_players(set(conflict.players) - {winner})
        self._clear_players_answer(conflict.players)
        return winner

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

    def _clear_players_answer(self, players: Iterable[Player]) -> None:
        for player in players:
            player.clear_answer()

    def _clear_marked_field_for_players(self, players: Iterable[Player]) -> None:
        for player in players:
            player.clear_marked_field()
