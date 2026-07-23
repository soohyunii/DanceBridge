from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    dancer = relationship(
        "Dancer", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    student = relationship(
        "Student", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Dancer(Base):
    __tablename__ = "dancers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="dancer")
    videos = relationship("Video", back_populates="dancer", cascade="all, delete-orphan")
    classes = relationship("Class", back_populates="dancer", cascade="all, delete-orphan")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    dancer_id = Column(Integer, ForeignKey("dancers.id"), index=True, nullable=False)
    instagram_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    dancer = relationship("Dancer", back_populates="videos")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="student")


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    dancer_id = Column(Integer, ForeignKey("dancers.id"), index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String, nullable=True)
    level = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    dancer = relationship("Dancer", back_populates="classes")
