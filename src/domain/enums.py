from enum import Enum


class GameState(str, Enum):
    PLAYERS_WAITING = 'players_waiting'
    IS_FULL = 'is_full'
    STARTED = 'started'
    IN_PROCESS = 'in_process'
    ATTACK_WAITING = 'attack_waiting'
    DUELING = 'dueling'
    ANSWERS_WAITING = 'answers_waiting'
    ENDED = 'ended'
