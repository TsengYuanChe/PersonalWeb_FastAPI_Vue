from fastapi import APIRouter

from schemas.content import ExperienceResponse
from services.experience_service import get_experience_v1

router = APIRouter(prefix="/api/v1", tags=["Experience"])


@router.get("/experience", response_model=ExperienceResponse)
def experience():
    return get_experience_v1()
