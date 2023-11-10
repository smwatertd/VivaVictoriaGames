from enum import Enum


class MessageType(Enum):
    EVENT = 'event'
    COMMAND = 'command'
    UNKNOWN = 'unknown'
