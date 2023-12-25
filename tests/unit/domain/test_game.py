from domain.models import Game


# TODO: Game __init__ None args


class TestGame:
    def test_get_id_id_returned(self, empty_game: Game) -> None:
        game_id = empty_game.get_id()

        assert game_id == empty_game._id
