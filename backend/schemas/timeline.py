from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, model_validator

from schemas.common import ApiResponse


class PointTimelineEvent(BaseModel):
    id: str
    type: Literal["point"]
    label: str
    date: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")


class DurationTimelineEvent(BaseModel):
    id: str
    type: Literal["duration"]
    label: str
    start_date: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    end_date: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")

    @model_validator(mode="after")
    def validate_date_order(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must not be after end_date")
        return self


TimelineEvent = Annotated[
    Union[PointTimelineEvent, DurationTimelineEvent],
    Field(discriminator="type"),
]


class TimelineEventsData(BaseModel):
    timeline_events: list[TimelineEvent]


class TimelineEventsResponse(ApiResponse):
    data: TimelineEventsData
