from pydantic import BaseModel


class Event(BaseModel):
    pass


class GameEvent(Event):
    game_id: int


class ConnectedPlayer(BaseModel):
    id: int


class PlayerAdded(GameEvent):
    player_id: int
    connected_players: list[ConnectedPlayer]


class OrderPlayer(BaseModel):
    id: int


class GameField(BaseModel):
    id: int


class GameStarted(GameEvent):
    fields: list[GameField]
    order: list[OrderPlayer]


class PlayerRemoved(Event):
    game_id: int
    player_id: int


class FieldAttacked(Event):
    game_id: int
    attacker_id: int
    defender_id: int
    field_id: int


class FieldCaptured(Event):
    game_id: int
    field_id: int
    capturer_id: int
    new_field_value: int


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


class RoundFinished(Event):
    game_id: int
    round_number: int


class GameEnded(Event):
    game_id: int


class DuelRoundStarted(Event):
    game_id: int
    round_number: int


class CategorySetted(Event):
    game_id: int
    category_id: int


class DuelRoundFinished(Event):
    game_id: int


class FieldDefended(Event):
    game_id: int
    field_id: int
    new_field_value: int


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


class SelectingBaseStageRoundFinished(GameEvent):
    pass


class PlayerSelectedBase(GameEvent):
    pass


class SelectingBaseStageFinished(GameEvent):
    pass
