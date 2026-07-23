from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import CurrentUser, require_student

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=schemas.StudentOut, status_code=201)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_student),
):
    existing = db.query(models.Student).filter(models.Student.user_id == current.user.id).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Student profile already exists")

    db_student = models.Student(user_id=current.user.id, name=student.name, bio=student.bio)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(models.Student).order_by(models.Student.created_at.desc()).all()


@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
