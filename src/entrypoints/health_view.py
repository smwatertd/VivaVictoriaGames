from entrypoints.schemas import HealthSchema

from fastapi import APIRouter


router = APIRouter(
    tags=['Health'],
)


@router.get(
    '/health',
    status_code=200,
    response_model=HealthSchema,
)
def check_health() -> HealthSchema:
    return HealthSchema(status='ok')
