from dataclasses import dataclass

from infrastructure.adapters.message_types import MessageType


@dataclass
class Message:
    type: MessageType
    payload_type: str
    payload: dict
