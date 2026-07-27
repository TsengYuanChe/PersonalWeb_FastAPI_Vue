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


class ParagraphSection(BaseModel):
    title: str
    paragraphs: list[str]


class ListSection(BaseModel):
    title: str
    items: list[str]


class HighlightSection(BaseModel):
    title: str
    paragraphs: list[str]
    highlights: list[str]


class ChallengeItem(BaseModel):
    title: str
    description: str


class ChallengesSection(BaseModel):
    title: str
    items: list[ChallengeItem]


class ShowcaseItem(BaseModel):
    image: str
    image_alt: str
    caption: Optional[str] = None


class ProjectItem(BaseModel):
    slug: str
    title: str
    subtitle: str
    category: str
    summary: str
    cover: str
    cover_alt: str
    cover_ready: bool = False
    period: str
    role: str
    status: Literal["internal", "live"]
    website_url: Optional[str] = None
    source_url: Optional[str] = None
    technologies: list[str]
    overview: ParagraphSection
    responsibilities: ListSection
    architecture: HighlightSection
    challenges: ChallengesSection
    deployment: HighlightSection
    lessons_learned: ListSection
    showcase: list[ShowcaseItem]


class ProjectData(BaseModel):
    projects: list[ProjectItem]


class AboutResponse(ApiResponse):
    data: AboutData


class ExperienceResponse(ApiResponse):
    data: ExperienceData


class ProjectsResponse(ApiResponse):
    data: ProjectData
