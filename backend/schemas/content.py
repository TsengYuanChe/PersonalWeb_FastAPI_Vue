from typing import Literal, Optional

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


class ProjectLinks(BaseModel):
    github: Optional[str] = None
    demo: Optional[str] = None


class ProjectItem(BaseModel):
    title: str
    type: Literal["featured", "normal"]
    category: str
    overview: str
    features: list[str] = []
    engineering: list[str] = []
    architecture: str
    tradeoffs: list[str] = []
    future: list[str] = []
    tech: list[str]
    links: ProjectLinks


class ProjectData(BaseModel):
    projects: list[ProjectItem]


class AboutResponse(ApiResponse):
    data: AboutData


class ExperienceResponse(ApiResponse):
    data: ExperienceData


class ProjectsResponse(ApiResponse):
    data: ProjectData
