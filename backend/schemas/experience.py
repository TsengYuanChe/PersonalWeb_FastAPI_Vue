from typing import Optional

from pydantic import BaseModel

from schemas.common import ApiResponse


class ExperienceItem(BaseModel):
    slug: str
    category: str
    title: str
    organization: str
    role: str
    location: str
    start_date: str
    end_date: Optional[str] = None
    period: str
    summary: str
    logo: str
    skills: list[str]
    description: list[str]
    responsibilities: list[str]
    highlights: list[str]
    projects: list[str]
    technologies: list[str]
    gpa: Optional[str] = None


class ExperienceData(BaseModel):
    experience: list[ExperienceItem]


class ExperienceResponse(ApiResponse):
    data: ExperienceData
