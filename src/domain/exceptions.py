class AddPlayerError(Exception):
    pass


class PlayerAlreadyAdded(AddPlayerError):
    pass


class GameIsFull(AddPlayerError):
    pass


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


# TODO: Add more details
class GameInvalidState(Exception):
    pass
