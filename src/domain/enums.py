from enum import Enum


class GameState(str, Enum):
    PLAYERS_WAITING = 'players_waiting'
    START_WAITING = 'start_waiting'
    STARTED = 'started'
    ATTACK_WAITING = 'attack_waiting'
