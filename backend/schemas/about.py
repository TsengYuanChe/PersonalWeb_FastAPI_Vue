from pydantic import BaseModel, Field

from schemas.common import ApiResponse


class AboutSection(BaseModel):
    id: str
    title: str
    paragraphs: list[str]
    items: list[str] = Field(default_factory=list)


class AboutData(BaseModel):
    paragraphs: list[str]
    sections: list[AboutSection]


class AboutResponse(ApiResponse):
    data: AboutData
