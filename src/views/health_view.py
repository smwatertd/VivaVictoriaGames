from fastapi import APIRouter

from schemas import HealthSchema


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
