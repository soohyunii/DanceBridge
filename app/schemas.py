import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, field_validator

INSTAGRAM_URL_PATTERN = re.compile(
    r"^https?://(www\.)?instagram\.com/(reel|p)/[A-Za-z0-9_-]+/?"
)

Role = Literal["dancer", "student"]


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: Role


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role


class VideoCreate(BaseModel):
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


class DancerCreate(BaseModel):
    name: str
    bio: str | None = None


class DancerOut(BaseModel):
    id: int
    name: str
    bio: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    name: str
    bio: str | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    bio: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ClassCreate(BaseModel):
    dancer_id: int
    title: str
    description: str | None = None
    genre: str | None = None
    level: str | None = None
    price: int | None = None


class ClassOut(BaseModel):
    id: int
    dancer_id: int
    title: str
    description: str | None
    genre: str | None
    level: str | None
    price: int | None
    created_at: datetime

    class Config:
        from_attributes = True


EnrollmentStatus = Literal["pending", "approved", "cancelled"]


class EnrollmentCreate(BaseModel):
    class_id: int


class EnrollmentStatusUpdate(BaseModel):
    status: Literal["approved", "cancelled"]


class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    class_id: int
    status: EnrollmentStatus
    created_at: datetime

    class Config:
        from_attributes = True
