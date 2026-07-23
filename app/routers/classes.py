from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("", response_model=schemas.ClassOut, status_code=201)
def create_class(class_in: schemas.ClassCreate, db: Session = Depends(get_db)):
    dancer = db.query(models.Dancer).filter(models.Dancer.id == class_in.dancer_id).first()
    if dancer is None:
        raise HTTPException(status_code=404, detail="Dancer not found")

    db_class = models.Class(
        dancer_id=class_in.dancer_id,
        title=class_in.title,
        description=class_in.description,
        genre=class_in.genre,
        level=class_in.level,
        price=class_in.price,
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


@router.get("", response_model=list[schemas.ClassOut])
def list_classes(
    dancer_id: int | None = None,
    genre: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Class)
    if dancer_id is not None:
        query = query.filter(models.Class.dancer_id == dancer_id)
    if genre is not None:
        query = query.filter(models.Class.genre == genre)
    return query.order_by(models.Class.created_at.desc()).all()


@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(class_id: int, db: Session = Depends(get_db)):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class
