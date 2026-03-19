from typing import Optional

from pydantic import BaseModel

from schemas.common import ApiResponse


class AboutData(BaseModel):
    paragraphs: list[str]


class ExperienceItem(BaseModel):
    details: list[str]
    duration: str
    location: str
    position: str
    skills: list[str]
    logo: Optional[str] = None
    gpa: Optional[str] = None


class ExperienceData(BaseModel):
    experience: list[ExperienceItem]


class ProjectItem(BaseModel):
    title: str
    description: str
    languages: list[str]
    tools: list[str]
    url: Optional[str] = None


class ProjectData(BaseModel):
    projects: list[ProjectItem]


class AboutResponse(ApiResponse):
    data: AboutData


class ExperienceResponse(ApiResponse):
    data: ExperienceData


class ProjectsResponse(ApiResponse):
    data: ProjectData
