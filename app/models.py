from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    dancer_id = Column(Integer, index=True, nullable=False)
    instagram_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
