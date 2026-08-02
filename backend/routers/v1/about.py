from fastapi import APIRouter

from schemas.content import AboutResponse
from services.content_service import get_about_v1

router = APIRouter(prefix="/api/v1", tags=["About"])


@router.get("/about", response_model=AboutResponse)
def about():
    return get_about_v1()
