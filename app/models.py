from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    videos = relationship("Video", back_populates="dancer", cascade="all, delete-orphan")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    dancer_id = Column(Integer, ForeignKey("dancers.id"), index=True, nullable=False)
    instagram_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    dancer = relationship("Dancer", back_populates="videos")
