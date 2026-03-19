from fastapi import APIRouter
from schemas.content import AboutResponse, ExperienceResponse, ProjectsResponse
from services.content_service import (
    get_about_legacy,
    get_about_v1,
    get_experience_legacy,
    get_experience_v1,
    get_projects_legacy,
    get_projects_v1,
)

router = APIRouter()


@router.get("/api/about")
def about():
    return get_about_legacy()


@router.get("/api/experience")
def experience():
    return get_experience_legacy()


@router.get("/api/projects")
def projects():
    return get_projects_legacy()


@router.get("/api/v1/about", response_model=AboutResponse)
def about_v1():
    return get_about_v1()


@router.get("/api/v1/experience", response_model=ExperienceResponse)
def experience_v1():
    return get_experience_v1()


@router.get("/api/v1/projects", response_model=ProjectsResponse)
def projects_v1():
    return get_projects_v1()
