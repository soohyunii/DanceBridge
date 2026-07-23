import re
from datetime import datetime

from pydantic import BaseModel, field_validator

INSTAGRAM_URL_PATTERN = re.compile(
    r"^https?://(www\.)?instagram\.com/(reel|p)/[A-Za-z0-9_-]+/?"
)


class VideoCreate(BaseModel):
    dancer_id: int
    instagram_url: str

    @field_validator("instagram_url")
    @classmethod
    def validate_instagram_url(cls, value: str) -> str:
        if not INSTAGRAM_URL_PATTERN.match(value):
            raise ValueError("instagram_url must be a valid Instagram reel or post link")
        return value


class VideoOut(BaseModel):
    id: int
    dancer_id: int
    instagram_url: str
    created_at: datetime

    class Config:
        from_attributes = True
