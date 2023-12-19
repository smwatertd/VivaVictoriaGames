from pydantic import BaseModel


class Event(BaseModel):
    pass


class FieldEvent(Event):
    game_pk: int
    field_pk: int


class PlayerAdded(Event):
    game_id: int
    player_id: int


class GameStarted(Event):
    game_id: int


class GameIsFull(Event):
    game_id: int


class GameStateChanged(Event):
    game_id: int
    state: str


class GameClosed(Event):
    game_id: int


class PlayerTurnChanged(Event):
    game_id: int
    player_id: int


class PlayerRemoved(Event):
    game_id: int
    player_id: int


class FieldAttacked(FieldEvent):
    attacker_pk: int


class FieldCaptured(Event):
    game_id: int
    field_id: int
    capturer_id: int


class PlayerFieldAttacked(Event):
    game_id: int
    attacker_id: int
    defender_id: int
    field_id: int


class DuelStarted(Event):
    game_id: int
    attacker_id: int
    defender_id: int
    field_id: int


class QuestionSetted(Event):
    game_id: int
    question_id: int


class AllPlayersConnected(Event):
    game_id: int


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
    round_number: int
    correct_answer_id: int


class GameInProcess(Event):
    game_id: int


class FieldDefended(Event):
    game_id: int
    field_id: int


class DuelEnded(Event):
    game_id: int


class PlayerAnswered(Event):
    game_id: int
    player_id: int
