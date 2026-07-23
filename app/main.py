from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import auth, classes, dancers, students, videos

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DanceBridge API")
app.include_router(auth.router)
app.include_router(dancers.router)
app.include_router(students.router)
app.include_router(classes.router)
app.include_router(videos.router)


@app.get("/health")
def health():
    return {"status": "ok"}
