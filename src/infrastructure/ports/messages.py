from abc import ABC, abstractmethod

from infrastructure.ports.message_types import MessageType


class Message(ABC):
    @abstractmethod
    def get_payload(self) -> dict:
        pass

    @abstractmethod
    def get_message_type(self) -> MessageType:
        pass

    @abstractmethod
    def get_payload_type(self) -> str:
        pass
