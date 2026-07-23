from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import CurrentUser, get_own_dancer, require_dancer

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("", response_model=schemas.VideoOut, status_code=201)
def create_video(
    video: schemas.VideoCreate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_dancer),
):
    dancer = get_own_dancer(db, current)

    db_video = models.Video(dancer_id=dancer.id, instagram_url=video.instagram_url)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


@router.get("", response_model=list[schemas.VideoOut])
def list_videos(dancer_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Video)
    if dancer_id is not None:
        query = query.filter(models.Video.dancer_id == dancer_id)
    return query.order_by(models.Video.created_at.desc()).all()


@router.delete("/{video_id}", status_code=204)
def delete_video(
    video_id: int,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_dancer),
):
    dancer = get_own_dancer(db, current)
    db_video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    if db_video.dancer_id != dancer.id:
        raise HTTPException(status_code=403, detail="You can only delete your own videos")
    db.delete(db_video)
    db.commit()
