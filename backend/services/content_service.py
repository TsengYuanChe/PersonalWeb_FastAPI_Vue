from fastapi import HTTPException

from repositories.content_repository import (
    read_experiences_with_timestamps,
    read_json_with_timestamp,
    read_project_with_timestamp,
    read_projects_with_timestamps,
)
from schemas.content import ExperienceItem, ProjectItem


def get_legacy_content(filename):
    data, updated_at = read_json_with_timestamp(filename)
    data["updated_at"] = updated_at
    return data


def get_v1_content(filename):
    data, updated_at = read_json_with_timestamp(filename)
    return {
        "data": data,
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }


def get_about_legacy():
    return get_legacy_content("profile/about.json")


def get_experience_legacy():
    experiences, updated_at = _get_validated_experiences()
    return {
        "experience": experiences,
        "updated_at": updated_at,
    }


def get_projects_legacy():
    projects, updated_at = _get_validated_projects()
    return {
        "projects": projects,
        "updated_at": updated_at,
    }


def get_about_v1():
    return get_v1_content("profile/about.json")


def get_experience_v1():
    experiences, updated_at = _get_validated_experiences()
    return {
        "data": {"experience": experiences},
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }


def get_projects_v1():
    projects, updated_at = _get_validated_projects()
    return {
        "data": {"projects": projects},
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


def _get_validated_projects():
    projects, updated_at = read_projects_with_timestamps()
    validated = [_validate_project(project).model_dump(mode="json") for project in projects]
    return validated, updated_at


def _validate_project(project):
    return ProjectItem.model_validate(project)


def _get_validated_experiences():
    experiences, updated_at = read_experiences_with_timestamps()
    validated = [
        ExperienceItem.model_validate(experience).model_dump(mode="json")
        for experience in experiences
    ]
    return validated, updated_at
