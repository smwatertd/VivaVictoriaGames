from domain.models.model import Model


class Player(Model):
    def __init__(self, id: int, username: str) -> None:
        super().__init__(id)
        self.username = username

    def __repr__(self) -> str:
        return f'Player(id={self.id}, username={self.username})'

    def __hash__(self) -> int:
        return hash(self.id)
