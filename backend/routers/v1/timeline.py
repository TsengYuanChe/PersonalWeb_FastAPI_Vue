from fastapi import APIRouter

from schemas.timeline import TimelineEventsResponse
from services.timeline_service import get_timeline_events_v1

router = APIRouter(prefix="/api/v1", tags=["Timeline"])


@router.get("/timeline-events", response_model=TimelineEventsResponse)
def timeline_events():
    return get_timeline_events_v1()
