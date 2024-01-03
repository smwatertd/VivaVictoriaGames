from core.settings import game_settings

from domain import enums, events, exceptions
from domain.models.battle import Battle
from domain.models.capture import Capture
from domain.models.category import Category
from domain.models.field import Field
from domain.models.game_result_line import GameResultLine
from domain.models.model import Model
from domain.models.player import Player
from domain.models.player_answer import PlayerAnswer
from domain.models.preparation import Preparation
from domain.models.question import Question
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

    def check_stage_outcome(self, finished_stage: events.StageType) -> None:
        if finished_stage == events.StageType.PREPARATORY:
            self.start_capturing_stage()
        elif finished_stage == events.StageType.CAPTURING:
            self.start_battlings_stage()
        else:
            self.finish()

    def start_round(self) -> None:
        if self._state == enums.GameState.PREPARATORY_STAGE:
            self.start_preparatory_stage_round()
        elif self._state == enums.GameState.CAPTURING_STAGE:
            self.start_capturing_stage_round()
        elif self._state == enums.GameState.BATTLING_STAGE:
            self.start_battlings_stage_round()
        else:
            raise ValueError(f'Invalid game state: {self._state} in start_round')

    def finish_round(self) -> None:
        if self._state == enums.GameState.PREPARATORY_STAGE:
            self.finish_preparatory_stage_round()
        elif self._state == enums.GameState.CAPTURING_STAGE:
            self.finish_capturing_stage_round()
        elif self._state == enums.GameState.BATTLING_STAGE:
            self.finish_battlings_stage_round()
        else:
            raise ValueError(f'Invalid game state: {self._state} in finish_round')

    def check_round_outcome(self) -> None:
        if self._state == enums.GameState.PREPARATORY_STAGE:
            self.check_preparatory_stage_round_outcome()
        elif self._state == enums.GameState.CAPTURING_STAGE:
            self.check_capturing_stage_round_outcome()
        elif self._state == enums.GameState.BATTLING_STAGE:
            self.check_battlings_stage_round_outcome()
        else:
            raise ValueError('Game is not in process')

    def set_question(self, question: Question) -> None:
        if self._state == enums.GameState.CAPTURING_STAGE:
            self.set_capturing_question(question)
        elif self._state == enums.GameState.DUELING:
            self.set_duel_question(question)
        else:
            raise ValueError('Game is not in process')

    def set_player_answer(self, player: Player, answer: PlayerAnswer) -> None:
        self._set_player_answer(player, answer)

    def finish_battle_round(self) -> None:
        if self._state == enums.GameState.CAPTURING_STAGE:
            self.finish_capturing_battle_round()
        elif self._state == enums.GameState.DUELING:
            self.finish_duel_round()

    def check_battle_round_outcome(self) -> None:
        if self._state == enums.GameState.CAPTURING_STAGE:
            self.finish_capturing_stage_round()
        elif self._state == enums.GameState.DUELING:
            self.check_duel_round_outcome()

    def check_are_all_players_answered(self) -> None:
        if self._state == enums.GameState.CAPTURING_STAGE:
            self._check_are_all_marking_battle_players_answered()
        elif self._state == enums.GameState.DUELING:
            self._check_are_all_duel_players_answered()

    ###########################################################
    # Preparation Stage
    ###########################################################
    def start_preparatory_stage(self) -> None:
        self._preparation.start()
        self._state = enums.GameState.PREPARATORY_STAGE
        self.register_event(
            events.StageStarted(
                game_id=self.get_id(),
                stage_type=events.StageType.PREPARATORY,
                stage_info=events.StageInfo(rounds_count=self._get_preparatory_stage_rounds_count()),
            ),
        )

    def start_preparatory_stage_round(self) -> None:
        self._select_player_order(self._preparation.get_round_number())
        self.register_event(
            events.RoundStarted(
                game_id=self.get_id(),
                round_type=events.RoundType.ORDERED,
                round_number=self._preparation.get_round_number(),
                duration_seconds=self._get_preparatory_stage_round_seconds_duration(),
                player=events.Player(id=self._player_order.get_id()),
            ),
        )

    def select_player_base(self, player: Player, field: Field) -> None:
        self._preparation.set_player_base(player, field)
        self.register_event(
            events.BaseSelected(
                game_id=self.get_id(),
                player=events.Player(id=player.get_id()),
                field=events.Field(id=field.get_id()),
                new_field_value=field.get_value(),
            ),
        )

    def finish_preparatory_stage_round(self) -> None:
        self._preparation.stop_round()
        self.register_event(events.RoundFinished(game_id=self.get_id()))

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
        self.register_event(events.StageStarted(game_id=self.get_id(), stage_type=events.StageType.CAPTURING))

    def start_capturing_stage_round(self) -> None:
        self._capture.start_round()
        self._state = enums.GameState.MARKS_WAITING
        self.register_event(
            events.RoundStarted(
                game_id=self.get_id(),
                round_type=events.RoundType.UNORDERED,
                round_number=self._capture.get_round_number(),
                duration_seconds=self._get_capturing_stage_round_seconds_duration(),
            ),
        )

    def mark_field(self, player: Player, field: Field) -> None:
        self._capture.mark_field(player, field)
        self.register_event(
            events.PlayerImplicitlyMarkedField(
                game_id=self.get_id(),
                player=events.Player(id=player.get_id()),
            ),
        )

    def check_are_all_players_marked_fields(self) -> None:
        if self._are_all_players_marked_fields():
            self._state = enums.GameState.CAPTURING_STAGE
            self.register_event(
                events.AllPlayersMarkedFields(
                    game_id=self.get_id(),
                    marked_fields=[
                        events.MarkedField(
                            player=events.Player(id=player.get_id()),
                            field=events.Field(id=player.get_marked_field().get_id()),
                        )
                        for player in self._players
                    ],
                ),
            )

    def check_marking_conflict(self) -> None:
        if self._capture.has_marking_conflict():
            self._detect_marking_conflict()
        else:
            self._capture_marked_fields()

    def start_marking_battle(self, players: list[Player], field: Field, category: Category) -> None:
        self.register_event(
            events.MarkingBattleStarted(
                game_id=self.get_id(),
                players=[events.Player(id=player.get_id()) for player in players],
                field=events.Field(id=field.get_id()),
                category=events.Category(id=category.id, name=category.name),
            ),
        )

    def set_capturing_question(self, question: Question) -> None:
        self._capture.set_correct_answer(question.correct_answer)
        self.register_event(
            events.QuestionSetted(
                game_id=self.get_id(),
                question=events.Question(
                    body=question.body,
                    answers=[events.Answer(id=answer.id, body=answer.body) for answer in question.answers],
                ),
            ),
        )

    def _check_are_all_marking_battle_players_answered(self) -> None:
        if self._capture.are_all_conflict_players_answered():
            self.register_event(
                events.AllPlayersAnswered(
                    game_id=self.get_id(),
                    answers=[
                        events.PlayerAnswer(
                            player=events.Player(id=player.get_id()),
                            answer=events.ExplicitAnswer(id=player.get_answer().id),
                        )
                        for player in self._players
                    ],
                ),
            )

    def capture_marked_fields(self) -> None:
        self._capture_marked_fields()

    def finish_capturing_battle_round(self) -> None:
        self._stop_marking_battle()

    def finish_capturing_stage_round(self) -> None:
        self.register_event(events.RoundFinished(game_id=self.get_id()))

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
            events.StageStarted(
                game_id=self.get_id(),
                stage_type=events.StageType.BATTLINGS,
                stage_info=events.StageInfo(rounds_count=self._get_battlings_stage_rounds_count()),
            ),
        )

    def start_battlings_stage_round(self) -> None:
        self._select_player_order(self._battle.get_round_number())
        self.register_event(
            events.RoundStarted(
                game_id=self.get_id(),
                round_type=events.RoundType.ORDERED,
                round_number=self._battle.get_round_number(),
                duration_seconds=self._get_battlings_stage_round_seconds_duration(),
                player=events.Player(id=self._player_order.get_id()),
            ),
        )

    def attack_field(self, attacker: Player, field: Field) -> None:
        self.register_event(
            events.FieldAttacked(
                game_id=self.get_id(),
                attacker=events.Player(id=attacker.get_id()),
                defender=events.Player(id=field.get_owner().get_id()),
                field=events.Field(id=field.get_id()),
            ),
        )

    def start_duel(self, attacker: Player, defender: Player, field: Field, category: Category) -> None:
        self._state = enums.GameState.DUELING
        self._battle.start_duel(attacker, defender, field, category)
        self.register_event(
            events.DuelStarted(
                game_id=self.get_id(),
                attacker=events.Player(id=attacker.get_id()),
                defender=events.Player(id=defender.get_id()),
                field=events.Field(id=field.get_id()),
                category=events.Category(id=category.id, name=category.name),
            ),
        )

    def start_duel_round(self) -> None:
        self._battle.start_duel_round()
        self.register_event(
            events.DuelRoundStarted(
                game_id=self.get_id(),
                round_number=self._battle.get_duel_round(),
                duration_seconds=self._get_duel_round_seconds_duration(),
                category=events.Category(
                    id=self._battle.get_duel_category().id,
                    name=self._battle.get_duel_category().name,
                ),
            ),
        )

    def set_duel_question(self, question: Question) -> None:
        self._battle.set_duel_correct_answer(answer=question.correct_answer)
        self.register_event(
            events.QuestionSetted(
                game_id=self.get_id(),
                question=events.Question(
                    body=question.body,
                    answers=[events.Answer(id=answer.id, body=answer.body) for answer in question.answers],
                ),
            ),
        )

    def _check_are_all_duel_players_answered(self) -> None:
        if self._battle.are_all_duel_players_answered():
            self.register_event(
                events.AllPlayersAnswered(
                    game_id=self.get_id(),
                    answers=[
                        events.PlayerAnswer(
                            player=events.Player(id=player.get_id()),
                            answer=events.ExplicitAnswer(id=player.get_answer().id),
                        )
                        for player in self._players
                    ],
                ),
            )

    def finish_duel_round(self) -> None:
        self._battle.finish_duel_round()
        self.register_event(events.DuelRoundFinished(game_id=self.get_id()))

    def check_duel_round_outcome(self) -> None:
        if self._battle.is_duel_continuing():
            self.start_duel_round()
        else:
            self._finish_duel()

    def finish_battlings_stage_round(self) -> None:
        self._battle.finish_round()
        self.register_event(events.RoundFinished(game_id=self.get_id(), result_type=events.ResultType.DEFENDED))

    def check_battlings_stage_round_outcome(self) -> None:
        if self._is_battle_stage_continuing():
            self.start_battlings_stage_round()
        else:
            self._stop_battlings_stage()

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
        player.on_disconnect()
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
        self.register_event(events.StageFinished(game_id=self.get_id(), stage_type=events.StageType.CAPTURING))

    def _get_capturing_stage_round_seconds_duration(self) -> int:
        return game_settings.capturing_stage_round_time_seconds

    def _set_player_answer(self, player: Player, answer: PlayerAnswer) -> None:
        player.set_answer(answer)
        self.register_event(
            events.PlayerAnsweredImplicitly(
                game_id=self.get_id(),
                player=events.Player(id=player.get_id()),
            ),
        )

    def _get_duel_round_seconds_duration(self) -> int:
        return game_settings.duel_round_time_seconds

    def _stop_battlings_stage(self) -> None:
        self._state = enums.GameState.IN_PROCESS
        self.register_event(events.StageFinished(game_id=self.get_id(), stage_type=events.StageType.BATTLINGS))

    def _is_preparatory_stage_continuing(self) -> bool:
        return not self._get_players_count() == self._preparation.get_round_number() - 1

    def _select_player_order(self, round_number: int) -> None:
        self._player_order = self._player_turn_selector.select(round_number, self._players)

    def _is_capturing_stage_continuing(self) -> bool:
        return not all(field.is_captured() for field in self._fields)

    def _are_all_players_marked_fields(self) -> bool:
        return all(player.is_marked_field() for player in self._players)

    def _detect_marking_conflict(self) -> None:
        conflict = self._capture.get_marking_conflict()
        self.register_event(
            events.MarkingConflictDetected(
                game_id=self.get_id(),
                field=events.Field(id=conflict.field.get_id()),
                players=[events.Player(id=player.get_id()) for player in conflict.players],
            ),
        )

    def _stop_marking_battle(self) -> None:
        winner = self._capture.finish_marking_battle()
        self.register_event(
            events.MarkingBattleFinished(
                game_id=self.get_id(),
                winner=events.Player(id=winner.get_id()),
            ),
        )

    def _get_battlings_stage_rounds_count(self) -> int:
        return game_settings.battlings_stage_rounds_count

    def _get_battlings_stage_round_seconds_duration(self) -> int:
        return game_settings.battlings_stage_round_time_seconds

    def _capture_marked_fields(self) -> None:
        captured = self._capture.capture_marked_fields()
        self.register_event(
            events.MarkedFieldsCaptured(
                game_id=self.get_id(),
                fields=[
                    events.FieldCaptured(
                        field=events.Field(id=field.get_id()),
                        player=events.Player(id=field.get_owner().get_id()),
                        new_field_value=field.get_value(),
                    )
                    for field in captured
                ],
            ),
        )

    def _stop_capture_stage_round(self) -> None:
        self._capture.stop_round()
        self.register_event(events.RoundFinished(game_id=self.get_id()))

    def get_duel_category(self) -> int:
        return self._battle._duel._category_id

    def _is_battle_stage_continuing(self) -> bool:
        return not self._battle.get_round_number() == game_settings.duel_max_rounds - 1

    def _finish_duel(self) -> None:
        self._state = enums.GameState.BATTLING_STAGE
        duel_result = self._battle.stop_duel()
        if duel_result.result_type == events.ResultType.CAPTURED:
            result = events.FieldCaptured(
                field=events.Field(id=duel_result.field.get_id()),
                player=events.Player(id=duel_result.field.get_owner().get_id()),
                new_field_value=duel_result.field.get_value(),
            )
        else:
            result = events.FieldDefended(
                field=events.Field(id=duel_result.field.get_id()),
                new_field_value=duel_result.field.get_value(),
            )
        self.register_event(
            events.DuelFinished(
                game_id=self.get_id(),
                result_type=duel_result.result_type,
                result=result,
            ),
        )

    def _calculate_results(self) -> list[GameResultLine]:
        sorted_players = sorted(self._players, key=lambda player: player.calculate_score(), reverse=True)
        return [
            GameResultLine(place=place, player=player, score=player.calculate_score())
            for place, player in enumerate(sorted_players, 1)
        ]

    def finish(self) -> None:
        self._state = enums.GameState.ENDED
        self.register_event(
            events.GameFinished(
                game_id=self.get_id(),
                results=[
                    events.GameResultLine(
                        place=result.place,
                        player=events.Player(id=result.player.get_id()),
                        score=result.score,
                    )
                    for result in self._calculate_results()
                ],
            ),
        )
