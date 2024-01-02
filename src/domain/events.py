from enum import Enum

from pydantic import BaseModel


class Event(BaseModel):
    pass


class GameEvent(Event):
    game_id: int


class Player(BaseModel):
    id: int


class Field(BaseModel):
    id: int


class GameResultLine(BaseModel):
    place: int
    player: Player
    score: int


class StageType(str, Enum):
    PREPARATORY = 'PREPARATORY'
    CAPTURING = 'CAPTURING'
    BATTLINGS = 'BATTLINGS'


class ResultType(str, Enum):
    CAPTURED = 'CAPTURED'
    DEFENDED = 'DEFENDED'


class FieldCaptured(BaseModel):
    field: Field
    player: Player
    new_field_value: int


class FieldDefended(BaseModel):
    field: Field
    new_field_value: int


class PlayerAdded(GameEvent):
    player: Player
    connected_players: list[Player]


class PlayerRemoved(GameEvent):
    player: Player


class GameStarted(GameEvent):
    fields: list[Field]
    order: list[Player]


class GameFinished(GameEvent):
    results: list[GameResultLine]


class LimitedByRoundsStageStarted(GameEvent):
    stage_type: StageType
    rounds_count: int


class OrderedRoundStarted(GameEvent):
    player: Player
    round_number: int
    duration_seconds: int


class RoundFinished(GameEvent):
    result_type: ResultType
    result: FieldDefended | FieldCaptured


class StageFinished(GameEvent):
    stage_type: StageType


class SelectingBaseStageRoundFinished(GameEvent):
    pass


class FieldAttacked(Event):
    game_id: int
    attacker_id: int
    defender_id: int
    field_id: int


class PlayerFieldAttacked(Event):
    game_id: int
    attacker_id: int
    defender_id: int
    field_id: int


class DuelPlayer(BaseModel):
    id: int


class DuelStarted(GameEvent):
    attacker_id: int
    defender_id: int
    field_id: int


class DuelCategorySetted(GameEvent):
    category_id: int


class QuestionSetted(Event):
    game_id: int
    question_id: int


class RoundStarted(Event):
    game_id: int
    round_number: int
    player_order_id: int


class DuelRoundStarted(Event):
    game_id: int
    round_number: int


class CategorySetted(Event):
    game_id: int
    category_id: int


class DuelRoundFinished(Event):
    game_id: int


class DuelEnded(Event):
    game_id: int


class PlayerAnswered(Event):
    game_id: int
    player_id: int


class RoundTimerStarted(Event):
    game_id: int
    round_number: int
    duration: int


class DuelRoundTimerStarted(Event):
    game_id: int
    round_number: int
    duel_round_number: int
    duration: int


class PreparingStageStarted(GameEvent):
    pass


class PreparingStageEnded(GameEvent):
    pass


class PreparatoryStageStarted(GameEvent):
    rounds_count: int


class SelectingBaseStageEnded(GameEvent):
    pass


class SelectingBaseStageRoundStarted(GameEvent):
    player_id: int
    duration: int
    round_number: int


class PlayerSelectedBase(GameEvent):
    pass


class SelectingBaseStageFinished(GameEvent):
    pass


class CapturingStageStarted(GameEvent):
    pass


class CapturingStageFinished(GameEvent):
    pass


class CapturingStageRoundStarted(GameEvent):
    duration: int
    round_number: int


class MarkingConflictPlayer(BaseModel):
    id: int


class MarkingConflictDetected(GameEvent):
    field_id: int
    players: list[MarkingConflictPlayer]


class CaptureBattlePlayer(BaseModel):
    id: int


class CapturingBattleStarted(GameEvent):
    players: list[CaptureBattlePlayer]
    field_id: int


class CapturingBattleCategorySetted(GameEvent):
    category_id: int


class CapturingBattleQuestionSetted(GameEvent):
    question_id: int


class CapturingBattlePlayerAnswered(GameEvent):
    player_id: int


class CapturedField(BaseModel):
    field_id: int
    new_field_value: int
    player_id: int


class CapturingStageRoundFinished(GameEvent):
    captured_fields: list[CapturedField]


class BaseSelected(GameEvent):
    player: Player
    field: Field


class FieldMarked(GameEvent):
    player_id: int


class PlayerMarkedField(BaseModel):
    player_id: int
    field_id: int


class FieldsMarked(GameEvent):
    marked_fields: list[PlayerMarkedField]


class AllPlayersMarkedFields(GameEvent):
    pass


class BattlingsStageStarted(GameEvent):
    rounds_count: int


class BattlingsStageEnded(GameEvent):
    pass


class BattlingsStageRoundStarted(GameEvent):
    player_id: int
    round_number: int


class BattlingsStageRoundEnded(GameEvent):
    pass


class CaptureConflictPlayerAnswered(GameEvent):
    player_id: int
