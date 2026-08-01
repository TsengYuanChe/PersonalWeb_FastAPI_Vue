from typing import Literal, Optional

from pydantic import BaseModel

from schemas.common import ApiResponse


class AboutData(BaseModel):
    paragraphs: list[str]


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
