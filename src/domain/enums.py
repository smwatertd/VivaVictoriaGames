from enum import Enum


class GameState(Enum):
    PLAYERS_WAITING = 'players_waiting'
    STARTED = 'started'
    ATTACK_WAITING = 'attack_waiting'
