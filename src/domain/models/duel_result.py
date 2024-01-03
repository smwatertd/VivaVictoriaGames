from dataclasses import dataclass

from domain.events import ResultType
from domain.models.field import Field


@dataclass(slots=True, frozen=True)
class DuelResult:
    result_type: ResultType
    field: Field
