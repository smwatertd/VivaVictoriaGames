from domain import enums, models

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class GameEntity(Base):
    __tablename__ = 'games'

    pk: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(server_default='players_waiting')
    round_number: Mapped[int] = mapped_column(default=0)
    question_id: Mapped[int | None] = mapped_column(ForeignKey('questions.pk'))

    question: Mapped['QuestionEntity'] = relationship(
        'QuestionEntity',
        uselist=False,
        back_populates='game',
    )
    players: Mapped[list['PlayerEntity']] = relationship(
        'PlayerEntity',
        back_populates='game',
    )
    fields: Mapped[list['FieldEntity']] = relationship(
        'FieldEntity',
        back_populates='game',
    )

    def __repr__(self) -> str:
        return f'Game({self.pk=}, {self.state=}, {self.round_number=})'

    def to_model(self) -> models.Game:
        return models.Game(
            pk=self.pk,
            players=[player.to_model() for player in self.players],
            state=enums.GameState[self.state],
            fields=[field.to_model() for field in self.fields],
            question=self.question.to_model() if self.question else None,
        )


class PlayerEntity(Base):
    __tablename__ = 'players'

    pk: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    game_id: Mapped[int] = mapped_column(ForeignKey('games.pk'))

    game: Mapped['GameEntity'] = relationship(
        'GameEntity',
        uselist=False,
        back_populates='players',
    )
    fields: Mapped[list['FieldEntity']] = relationship(
        'FieldEntity',
        back_populates='owner',
    )

    def __repr__(self) -> str:
        return f'Player(pk={self.pk}, username={self.username})'

    def to_model(self) -> models.Player:
        return models.Player(pk=self.pk, username=self.username)


class FieldEntity(Base):
    __tablename__ = 'fields'

    pk: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey('games.pk'))
    owner_id: Mapped[int | None] = mapped_column(ForeignKey('players.pk'))

    owner: Mapped['PlayerEntity'] = relationship(
        'PlayerEntity',
        uselist=False,
        back_populates='fields',
    )
    game: Mapped['GameEntity'] = relationship(
        'GameEntity',
        uselist=False,
        back_populates='fields',
    )

    def __repr__(self) -> str:
        return f'Field(pk={self.pk}, owner={self.owner})'

    def to_model(self) -> models.Field:
        return models.Field(pk=self.pk, owner=self.owner.to_model())


class QuestionEntity(Base):
    __tablename__ = 'questions'

    pk: Mapped[int] = mapped_column(primary_key=True)

    answers: Mapped[list['AnswerEntity']] = relationship(
        'AnswerEntity',
        back_populates='question',
    )

    def __repr__(self) -> str:
        return f'Question(pk={self.pk}'

    def to_model(self) -> models.Question:
        return models.Question(pk=self.pk, answers=[answer.to_model() for answer in self.answers])


class AnswerEntity(Base):
    __tablename__ = 'answers'

    pk: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.pk'))
    is_correct: Mapped[bool] = mapped_column(default=False)

    question: Mapped['QuestionEntity'] = relationship(
        'QuestionEntity',
        uselist=False,
        back_populates='answers',
    )

    def __repr__(self) -> str:
        return f'Answer(pk={self.pk}, is_correct={self.is_correct})'

    def to_model(self) -> models.Answer:
        return models.Answer(pk=self.pk, is_correct=self.is_correct)
