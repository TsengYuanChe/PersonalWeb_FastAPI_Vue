from fastapi import APIRouter

from schemas.journey import JourneyResponse
from services.journey_service import get_journey_v1

router = APIRouter(prefix="/api/v1", tags=["Journey"])


@router.get("/journey", response_model=JourneyResponse)
def journey():
    return get_journey_v1()
