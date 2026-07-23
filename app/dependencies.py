import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class CurrentUser:
    def __init__(self, user: models.User, role: str):
        self.user = user
        self.role = role


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> CurrentUser:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
        role = payload["role"]
    except (jwt.PyJWTError, KeyError, ValueError):
        raise credentials_error

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_error

    return CurrentUser(user=user, role=role)


def require_dancer(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if current.role != "dancer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires logging in with the dancer role",
        )
    return current


def require_student(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if current.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires logging in with the student role",
        )
    return current


def get_own_dancer(db: Session, current: CurrentUser) -> models.Dancer:
    dancer = db.query(models.Dancer).filter(models.Dancer.user_id == current.user.id).first()
    if dancer is None:
        raise HTTPException(status_code=400, detail="Create a dancer profile first")
    return dancer


def get_own_student(db: Session, current: CurrentUser) -> models.Student:
    student = db.query(models.Student).filter(models.Student.user_id == current.user.id).first()
    if student is None:
        raise HTTPException(status_code=400, detail="Create a student profile first")
    return student
