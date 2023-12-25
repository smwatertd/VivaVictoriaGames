class AddPlayerError(Exception):
    pass


class GameAlreadyStarted(AddPlayerError):
    def __init__(self) -> None:
        super().__init__('Game already started')


class GameIsFull(AddPlayerError):
    def __init__(self) -> None:
        super().__init__('Game is full')


class AttackError(Exception):
    pass


class NotYourTurn(AttackError):
    pass


class FieldNotFound(AttackError):
    pass


class AlreadyOwned(AttackError):
    pass


class PlayerNotFound(AttackError):
    pass
