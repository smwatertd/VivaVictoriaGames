from dataclasses import dataclass


@dataclass
class CaptureRoundResult:
    field_id: int
    new_field_value: int
    player_id: int
