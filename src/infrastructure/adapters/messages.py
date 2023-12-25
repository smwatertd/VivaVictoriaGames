from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    EVENT = 'event'
    COMMAND = 'command'


@dataclass
class Message:
    type: MessageType
    payload_type: str
    payload: dict
