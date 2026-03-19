from typing import Any

from pydantic import BaseModel


class Meta(BaseModel):
    updated_at: str
    version: str


class ApiResponse(BaseModel):
    data: Any
    meta: Meta
