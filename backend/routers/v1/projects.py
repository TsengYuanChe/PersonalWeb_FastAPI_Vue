from fastapi import APIRouter

from schemas.content import ProjectItem, ProjectsResponse
from services.project_service import get_project_by_slug, get_projects_v1

router = APIRouter(prefix="/api/v1", tags=["Projects"])


@router.get("/projects", response_model=ProjectsResponse)
def projects():
    return get_projects_v1()


@router.get("/projects/{slug}", response_model=ProjectItem)
def project_by_slug(slug: str):
    return get_project_by_slug(slug)
