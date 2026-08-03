from typing import Literal, Optional

from pydantic import BaseModel

from schemas.common import ApiResponse


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
    technical_highlights: HighlightSection
    challenges: ChallengesSection
    outcome: HighlightSection
    lessons_learned: ListSection
    showcase: list[ShowcaseItem]


class ProjectData(BaseModel):
    projects: list[ProjectItem]


class ProjectsResponse(ApiResponse):
    data: ProjectData
