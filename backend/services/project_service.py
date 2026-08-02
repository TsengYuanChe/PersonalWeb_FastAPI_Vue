from fastapi import HTTPException

from repositories.content_repository import (
    read_project_with_timestamp,
    read_projects_with_timestamps,
)
from schemas.content import ProjectItem


def get_projects_v1():
    projects, updated_at = read_projects_with_timestamps()
    validated = [_validate_project(project).model_dump(mode="json") for project in projects]

    return {
        "data": {"projects": validated},
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }


def get_project_by_slug(slug):
    project, _ = read_project_with_timestamp(slug)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project '{slug}' not found")

    return _validate_project(project).model_dump(mode="json")


def _validate_project(project):
    return ProjectItem.model_validate(project)
