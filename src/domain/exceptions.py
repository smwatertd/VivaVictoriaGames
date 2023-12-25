from domain import enums


class AddPlayerError(Exception):
    pass


class GameAlreadyStarted(AddPlayerError):
    def __init__(self) -> None:
        super().__init__('Game already started')


class GameIsFull(AddPlayerError):
    def __init__(self) -> None:
        super().__init__('Game is full')


class AttackFieldError(Exception):
    pass


class GameNotWaitingForAttack(AttackFieldError):
    def __init__(self, game_state: enums.GameState) -> None:
        super().__init__(f'Game not waiting for attack. Game state: {game_state}')


class FieldAlreadyOwned(AttackFieldError):
    def __init__(self, field_id: int) -> None:
        super().__init__(f'Field already owned. Field id: {field_id}')


class NotYourTurn(AttackFieldError):
    pass
