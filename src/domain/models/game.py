from core.settings import game_settings

from domain import enums, events, exceptions
from domain.models.battle import Battle
from domain.models.capture import Capture
from domain.models.field import Field
from domain.models.model import Model
from domain.models.player import Player
from domain.models.preparation import Preparation
from domain.strategies import PlayerTurnSelector


class Game(Model):
    def __init__(
        self,
        id: int,
        state: enums.GameState,
        preparation: Preparation,
        capture: Capture,
        battle: Battle,
        player_order: Player,
        players: list[Player],
        fields: list[Field],
        player_turn_selector: PlayerTurnSelector,
    ) -> None:
        super().__init__()
        self._id = id
        self._state = state
        self._preparation = preparation
        self._capture = capture
        self._battle = battle
        self._player_order = player_order
        self._players = players
        self._fields = fields
        self._player_turn_selector = player_turn_selector

    def get_id(self) -> int:
        return self._id

    def add_player(self, player: Player) -> None:
        self._ensure_can_add_player()
        self._add_player(player)

    def remove_player(self, player: Player) -> None:
        self._remove_player(player)

    def try_start(self) -> None:
        if self._is_full():
            self._start()

    def start_stage(self) -> None:
        if self._state == enums.GameState.IN_PROCESS:
            self.start_preparatory_stage()
        else:
            raise ValueError('Game is not in process')

    def start_round(self) -> None:
        if self._state == enums.GameState.PREPARATORY_STAGE:
            self.start_preparatory_stage_round()

    def finish_round(self) -> None:
        if self._state == enums.GameState.PREPARATORY_STAGE:
            self.finish_preparatory_stage_round()

    def check_round_outcome(self) -> None:
        if self._state == enums.GameState.PREPARATORY_STAGE:
            self.check_preparatory_stage_round_outcome()

    def check_stage_outcome(self, finished_stage: events.StageType) -> None:
        if finished_stage == events.StageType.PREPARATORY:
            self.start_capturing_stage()
        else:
            raise ValueError('Game is not in process')

    def finish(self) -> None:
        self._state = enums.GameState.ENDED
        self.register_event(events.GameFinished(game_id=self.get_id(), results=[]))

    ###########################################################
    # Preparation Stage
    ###########################################################
    def start_preparatory_stage(self) -> None:
        self._preparation.start()
        self._state = enums.GameState.PREPARATORY_STAGE
        self.register_event(
            events.LimitedByRoundsStageStarted(
                game_id=self.get_id(),
                stage_type=events.StageType.PREPARATORY,
                rounds_count=self._get_preparatory_stage_rounds_count(),
            ),
        )

    def start_preparatory_stage_round(self) -> None:
        self._select_player_order(self._preparation.get_round_number())
        self.register_event(
            events.OrderedRoundStarted(
                game_id=self.get_id(),
                player=events.Player(id=self._player_order.get_id()),
                round_number=self._preparation.get_round_number(),
                duration_seconds=self._get_preparatory_stage_round_seconds_duration(),
            ),
        )

    def select_player_base(self, player: Player, field: Field) -> None:
        self._preparation.set_player_base(player, field)
        self.register_event(
            events.BaseSelected(
                game_id=self.get_id(),
                player=events.Player(id=player.get_id()),
                field=events.Field(id=field.get_id()),
            ),
        )

    def finish_preparatory_stage_round(self) -> None:
        player = self._player_order
        base = player.get_base()
        self._preparation.stop_round()
        self.register_event(
            events.RoundFinished(
                game_id=self.get_id(),
                result_type=events.ResultType.CAPTURED,
                result=events.FieldCaptured(
                    field=events.Field(id=base.get_id()),
                    player=events.Player(id=player.get_id()),
                    new_field_value=base.get_value(),
                ),
            ),
        )

    def check_preparatory_stage_round_outcome(self) -> None:
        if self._is_preparatory_stage_continuing():
            self.start_preparatory_stage_round()
        else:
            self._stop_selection_base_stage()

    ###########################################################
    # Capturing Stage
    ###########################################################
    def start_capturing_stage(self) -> None:
        self._capture.start()
        self._state = enums.GameState.CAPTURING_STAGE
        self.register_event(events.CapturingStageStarted(game_id=self.get_id()))

    def start_capturing_stage_round(self) -> None:
        self._capture.start_round()
        self.register_event(
            events.CapturingStageRoundStarted(
                game_id=self.get_id(),
                duration=game_settings.capturing_stage_round_time_seconds,
                round_number=self._capture.get_round_number(),
            ),
        )

    def mark_field(self, player: Player, field: Field) -> None:
        self._capture.mark_field(player, field)
        self.register_event(events.FieldMarked(game_id=self.get_id(), player_id=player.get_id()))

    def check_are_all_players_marked_fields(self) -> None:
        if self._are_all_players_marked_fields():
            self.register_event(
                events.FieldsMarked(
                    game_id=self.get_id(),
                    marked_fields=[
                        events.PlayerMarkedField(player_id=player.get_id(), field_id=player.get_marked_field().get_id())
                        for player in self._players
                    ],
                ),
            )

    def check_marking_conflict(self) -> None:
        if self._capture.has_marking_conflict():
            self._start_capturing_battle()
        else:
            self._stop_capture_stage_round()

    def set_capturing_category(self, category: int) -> None:
        self.register_event(events.CapturingBattleCategorySetted(game_id=self.get_id(), category_id=category))

    def set_capturing_question(self, question: int) -> None:
        self.register_event(events.CapturingBattleQuestionSetted(game_id=self.get_id(), question_id=question))

    def set_capturing_correct_answer(self, answer: int) -> None:
        self._capture.set_correct_answer(answer)

    def send_marking_conflict_answer(self, player: Player, answer: int) -> None:
        self._capture.set_player_answer(player, answer)
        self.register_event(events.CapturingBattlePlayerAnswered(game_id=self.get_id(), player_id=player.get_id()))

    def check_capturing_battle_outcome(self) -> None:
        if self._capture.are_all_conflict_players_answered():
            self._stop_capturing_battle()
            self._stop_capture_stage_round()

    def check_capturing_stage_round_outcome(self) -> None:
        if self._is_capturing_stage_continuing():
            self.start_capturing_stage_round()
        else:
            self._stop_capturing_stage()

    ###########################################################
    # Battling Stage
    ###########################################################
    def start_battlings_stage(self) -> None:
        self._battle.start()
        self._state = enums.GameState.BATTLING_STAGE
        self.register_event(
            events.BattlingsStageStarted(
                game_id=self.get_id(),
                rounds_count=game_settings.battlings_stage_rounds_count,
            ),
        )

    def start_battlings_stage_round(self) -> None:
        self._select_player_order(self._battle.get_round_number())
        self.register_event(
            events.BattlingsStageRoundStarted(
                game_id=self.get_id(),
                player_id=self._player_order.get_id(),
                round_number=self._battle.get_round_number(),
            ),
        )

    def attack_field(self, attacker: Player, field: Field) -> None:
        self.register_event(
            events.FieldAttacked(
                game_id=self.get_id(),
                attacker_id=attacker.get_id(),
                defender_id=field.get_owner().get_id(),
                field_id=field.get_id(),
            ),
        )

    def start_duel(self, attacker: Player, defender: Player, field: Field) -> None:
        self._state = enums.GameState.DUELING
        self._battle.start_duel(attacker, defender, field)
        self.register_event(
            events.DuelStarted(
                game_id=self.get_id(),
                attacker_id=attacker.get_id(),
                defender_id=defender.get_id(),
                field_id=field.get_id(),
            ),
        )

    def set_duel_category(self, category: int) -> None:
        self._battle.set_duel_category(category)
        self.register_event(events.DuelCategorySetted(game_id=self.get_id(), category_id=category))

    def start_duel_round(self) -> None:
        self._battle.start_duel_round()
        self.register_event(events.DuelRoundStarted(game_id=self.get_id(), round_number=self._battle.get_duel_round()))

    def set_duel_question(self, question: int) -> None:
        self.register_event(events.QuestionSetted(game_id=self.get_id(), question_id=question))

    def set_duel_correct_answer(self, answer: int) -> None:
        self._battle.set_duel_correct_answer(answer)

    def set_player_answer(self, player: Player, answer: int) -> None:
        self._battle.set_player_answer(player, answer)
        self.register_event(events.PlayerAnswered(game_id=self.get_id(), player_id=player.get_id()))

    def check_are_all_players_answered(self) -> None:
        if self._battle.are_all_duel_players_answered():
            self.register_event(events.DuelRoundFinished(game_id=self.get_id()))

    def check_duel_round_outcome(self) -> None:
        if self._battle.is_duel_continuing():
            self.start_duel_round()
        else:
            self._battle.stop_duel()
            self.register_event(events.DuelEnded(game_id=self.get_id()))

    def check_battlings_stage_round_outcome(self) -> None:
        if self._is_battle_stage_continuing():
            self.start_battlings_stage_round()
        else:
            self._stop_battlings_stage()

    def finish_battlings_stage_round(self) -> None:
        self.register_event(events.BattlingsStageEnded(game_id=self.get_id()))

    ###########################################################
    # Private methods
    ###########################################################
    def _ensure_can_add_player(self) -> None:
        if self._state != enums.GameState.PLAYERS_WAITING:
            raise exceptions.GameAlreadyStarted
        if self._is_full():
            raise exceptions.GameIsFull

    def _add_player(self, player: Player) -> None:
        self._players.append(player)
        player.on_connect()
        self.register_event(
            events.PlayerAdded(
                game_id=self.get_id(),
                player=events.Player(id=player.get_id()),
                connected_players=[events.Player(id=player.get_id()) for player in self._players],
            ),
        )

    def _remove_player(self, player: Player) -> None:
        self._players.remove(player)
        self.register_event(events.PlayerRemoved(game_id=self.get_id(), player=events.Player(id=player.get_id())))

    def _is_full(self) -> bool:
        return len(self._players) == game_settings.players_count_to_start

    def _start(self) -> None:
        self._round_number = 1
        self._state = enums.GameState.IN_PROCESS
        sorted_fields = sorted(self._fields, key=lambda x: x.get_id())
        order = self._player_turn_selector.get_order(self._players)
        self.register_event(
            events.GameStarted(
                game_id=self.get_id(),
                fields=[events.Field(id=field.get_id()) for field in sorted_fields],
                order=[events.Player(id=player.get_id()) for player in order],
            ),
        )

    def _get_preparatory_stage_rounds_count(self) -> int:
        return self._get_players_count()

    def _get_preparatory_stage_round_seconds_duration(self) -> int:
        return game_settings.preparatory_stage_round_time_seconds

    def _get_players_count(self) -> int:
        return len(self._players)

    def _stop_selection_base_stage(self) -> None:
        self._state = enums.GameState.IN_PROCESS
        self.register_event(events.StageFinished(game_id=self.get_id(), stage_type=events.StageType.PREPARATORY))

    def _stop_capturing_stage(self) -> None:
        self.register_event(events.CapturingStageFinished(game_id=self.get_id()))

    def _stop_battlings_stage(self) -> None:
        self._state = enums.GameState.IN_PROCESS
        self.register_event(events.BattlingsStageEnded(game_id=self.get_id()))

    def _is_preparatory_stage_continuing(self) -> bool:
        return not self._get_players_count() == self._preparation.get_round_number() - 1

    def _select_player_order(self, round_number: int) -> None:
        self._player_order = self._player_turn_selector.select(round_number, self._players)

    def _is_capturing_stage_continuing(self) -> bool:
        return not all(field.is_captured() for field in self._fields)

    def _are_all_players_marked_fields(self) -> bool:
        return all(player.is_marked_field() for player in self._players)

    def _start_capturing_battle(self) -> None:
        conflict = self._capture.get_marking_conflict()
        self.register_event(
            events.CapturingBattleStarted(
                game_id=self.get_id(),
                players=[events.CaptureBattlePlayer(id=player.get_id()) for player in conflict.players],
                field_id=conflict.field.get_id(),
            ),
        )

    def _detect_marking_conflict(self) -> None:
        conflict = self._capture.get_marking_conflict()
        self.register_event(
            events.MarkingConflictDetected(
                game_id=self.get_id(),
                field_id=conflict.field.get_id(),
                players=[events.MarkingConflictPlayer(id=player.get_id()) for player in conflict.players],
            ),
        )

    def _stop_capturing_battle(self) -> None:
        self._capture.stop_battle()

    def _stop_capture_stage_round(self) -> None:
        round_result = self._capture.stop_round()
        self.register_event(
            events.CapturingStageRoundFinished(
                game_id=self.get_id(),
                captured_fields=[
                    events.CapturedField(
                        field_id=result_line.field_id,
                        player_id=result_line.player_id,
                        new_field_value=result_line.new_field_value,
                    )
                    for result_line in round_result
                ],
            ),
        )

    def get_duel_category(self) -> int:
        return self._battle._duel._category_id

    def _is_battle_stage_continuing(self) -> bool:
        return not self._battle.get_round_number() == game_settings.duel_max_rounds - 1
