from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import CurrentUser, get_current_user, get_own_dancer, get_own_student, require_student

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("", response_model=schemas.EnrollmentOut, status_code=201)
def create_enrollment(
    payload: schemas.EnrollmentCreate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_student),
):
    student = get_own_student(db, current)

    dance_class = db.query(models.Class).filter(models.Class.id == payload.class_id).first()
    if dance_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    db_enrollment = models.Enrollment(student_id=student.id, class_id=dance_class.id)
    db.add(db_enrollment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Already applied to this class")
    db.refresh(db_enrollment)
    return db_enrollment


@router.get("", response_model=list[schemas.EnrollmentOut])
def list_enrollments(
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    if current.role == "student":
        student = get_own_student(db, current)
        query = db.query(models.Enrollment).filter(models.Enrollment.student_id == student.id)
    else:
        dancer = get_own_dancer(db, current)
        query = (
            db.query(models.Enrollment)
            .join(models.Class, models.Enrollment.class_id == models.Class.id)
            .filter(models.Class.dancer_id == dancer.id)
        )
    return query.order_by(models.Enrollment.created_at.desc()).all()


@router.patch("/{enrollment_id}", response_model=schemas.EnrollmentOut)
def update_enrollment_status(
    enrollment_id: int,
    payload: schemas.EnrollmentStatusUpdate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    enrollment = db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    dance_class = db.query(models.Class).filter(models.Class.id == enrollment.class_id).first()

    if current.role == "dancer":
        dancer = get_own_dancer(db, current)
        if dance_class.dancer_id != dancer.id:
            raise HTTPException(status_code=403, detail="Not your class")
    elif current.role == "student":
        student = get_own_student(db, current)
        if enrollment.student_id != student.id or payload.status != "cancelled":
            raise HTTPException(
                status_code=403, detail="Students may only cancel their own enrollment"
            )
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    enrollment.status = payload.status
    db.commit()
    db.refresh(enrollment)
    return enrollment
