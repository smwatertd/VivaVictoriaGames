from domain import enums, events, exceptions
from domain.models.field import Field
from domain.models.model import Model
from domain.models.player import Player

from questions import Question, get_random_question


PLAYERS_COUNT = 2


def select_player_order_by_id(
    players: list[Player],
    player_order: Player | None = None,
) -> Player:
    sorted_players = sorted(players, key=lambda player: player._id)
    if player_order:
        player_index = sorted_players.index(player_order)
        for i in range(player_index + 1, len(sorted_players)):
            return sorted_players[i]
    return sorted_players[0]


class Game(Model):
    def __init__(
        self,
        id: int,
        players: list[Player],
        state: enums.GameState,
        fields: list[Field],
        player_order: Player | None = None,
        question: Question | None = None,
    ) -> None:
        super().__init__(id)
        self._players = players
        self._state = state
        self._player_order = player_order
        self._fields = fields
        self._question = question

    def __repr__(self) -> str:
        return """Game(id={}, players={}, state={}, player_order={}, fields={}), question={}""".format(
            self._id,
            self._players,
            self._state,
            self._player_order,
            self._fields,
            self._question,
        )

    def add_player(self, player: Player) -> None:
        self._ensure_can_add_player(player)
        self._add_player(player)
        self._try_start()

    def remove_player(self, player: Player) -> None:
        self._remove_player(player)

    def attack_field(self, attacker: Player, field: Field) -> None:
        self._ensure_can_attack(attacker, field)
        self._attack_field(attacker, field)

    def _ensure_can_add_player(self, player: Player) -> None:
        if player in self._players:
            raise exceptions.PlayerAlreadyAdded
        if len(self._players) == PLAYERS_COUNT:
            raise exceptions.GameIsFull

    def _add_player(self, player: Player) -> None:
        self._players.append(player)
        self._register_event(
            events.PlayerAdded(
                game_id=self._id,
                player_id=player._id,
                username=player._username,
            ),
        )

    def _try_start(self) -> None:
        if self._can_start():
            self._start()

    def _remove_player(self, player: Player) -> None:
        self._players.remove(player)
        self._register_event(
            events.PlayerRemoved(
                game_id=self._id,
                player_id=player._id,
            ),
        )

    def _can_start(self) -> bool:
        return (
            len(self._players) == PLAYERS_COUNT
            and self._state == enums.GameState.PLAYERS_WAITING
        )

    def _start(self) -> None:
        self._set_state(enums.GameState.STARTED)
        self._set_player_order(select_player_order_by_id(self._players))

    def _set_state(self, state: enums.GameState) -> None:
        self._state = state
        if state == enums.GameState.STARTED:
            self._register_event(
                events.GameStarted(
                    game_id=self._id,
                    state=state,
                ),
            )

    def _set_player_order(self, player_order: Player) -> None:
        self._player_order = player_order
        self._set_state(enums.GameState.ATTACK_WAITING)
        self._register_event(
            events.PlayerTurnChanged(
                game_id=self._id,
                player_id=player_order.id,
            ),
        )

    def _ensure_can_attack(self, attacker: Player, field: Field) -> None:
        if self._state != enums.GameState.ATTACK_WAITING:
            raise exceptions.GameInvalidState(self._state)
        if self._player_order != attacker:
            raise exceptions.NotYourTurn
        if field not in self._fields:
            raise exceptions.FieldNotFound(field._id)

    def _attack_field(self, attacker: Player, field: Field) -> None:
        self._register_event(
            events.FieldAttacked(
                game_id=self._id,
                field_id=field._id,
                attacker_id=attacker.id,
            ),
        )
        self._try_capture(attacker, field)

    def _try_capture(self, attacker: Player, field: Field) -> None:
        if field.is_captured():
            field.ensure_can_capture(attacker)
            self._start_duel(attacker, field.get_owner())
        else:
            self._capture(attacker, field)

    def _start_duel(self, attacker: Player, defender: Player) -> None:
        self._set_state(enums.GameState.DUELING)
        self._register_event(
            events.DuelStarted(
                game_id=self._id,
                attacker_id=attacker.id,
                defender_id=defender.id,
            ),
        )
        # TODO: Redo with event consumer
        self._set_question(get_random_question())

    def _capture(self, capturer: Player, field: Field) -> None:
        field.set_owner(capturer)
        self._register_event(
            events.FieldCaptured(
                game_id=self._id,
                field_id=field._id,
                capturer_id=capturer.id,
            ),
        )
        self._set_player_order(
            select_player_order_by_id(self._players, self._player_order),
        )

    def _set_question(self, question: Question) -> None:
        self._question = question
        self._register_event(
            events.QuestionSet(
                game_id=self._id,
                question_id=question.id,
                answers=[(answer.id, answer.body) for answer in question.answers],
            ),
        )
