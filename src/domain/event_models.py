from pydantic import BaseModel


class BasicCategory(BaseModel):
    id: int


class Category(BaseModel):
    id: int
    name: str


class QuestionAnswer(BaseModel):
    id: int
    body: str


class Question(BaseModel):
    body: str
    answers: list[QuestionAnswer]


class Answer(BaseModel):
    id: int


class Player(BaseModel):
    id: int


class PlayerAnswer(BaseModel):
    player: Player
    answer: Answer


class PlayerResult(BaseModel):
    place: int
    player: Player
    score: int


class Field(BaseModel):
    id: int


class MarkedField(BaseModel):
    player: Player
    field: Field


class CapturedField(BaseModel):
    field: Field
    player: Player
    new_field_value: int


class DefendedField(BaseModel):
    field: Field
    new_field_value: int


class StageInfo(BaseModel):
    rounds_count: int


class Duration(BaseModel):
    seconds: int
