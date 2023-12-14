class Answer:
    def __init__(self, id: int, is_correct: bool) -> None:
        self.id = id
        self.is_correct = is_correct

    def __repr__(self) -> str:
        return f'Answer(id={self.id}, is_correct={self.is_correct})'
