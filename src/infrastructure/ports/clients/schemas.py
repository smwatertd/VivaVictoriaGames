from pydantic import BaseModel


class AnswerSchema(BaseModel):
    id: int
    body: str
    is_correct: bool


class QuestionSchema(BaseModel):
    id: int
    body: str
    answers: list[AnswerSchema]
