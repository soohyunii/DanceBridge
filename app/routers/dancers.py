from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import CurrentUser, require_dancer

router = APIRouter(prefix="/dancers", tags=["dancers"])


@router.post("", response_model=schemas.DancerOut, status_code=201)
def create_dancer(
    dancer: schemas.DancerCreate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_dancer),
):
    existing = db.query(models.Dancer).filter(models.Dancer.user_id == current.user.id).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Dancer profile already exists")

    db_dancer = models.Dancer(user_id=current.user.id, name=dancer.name, bio=dancer.bio)
    db.add(db_dancer)
    db.commit()
    db.refresh(db_dancer)
    return db_dancer


@router.get("", response_model=list[schemas.DancerOut])
def list_dancers(db: Session = Depends(get_db)):
    return db.query(models.Dancer).order_by(models.Dancer.created_at.desc()).all()


@router.get("/{dancer_id}", response_model=schemas.DancerOut)
def get_dancer(dancer_id: int, db: Session = Depends(get_db)):
    db_dancer = db.query(models.Dancer).filter(models.Dancer.id == dancer_id).first()
    if db_dancer is None:
        raise HTTPException(status_code=404, detail="Dancer not found")
    return db_dancer
