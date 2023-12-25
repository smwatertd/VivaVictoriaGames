class InvalidMessageType(Exception):
    def __init__(self, message_type: type) -> None:
        super().__init__(f'Invalid message type: {message_type}')
