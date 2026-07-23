from fastapi import FastAPI

app = FastAPI(title="DanceBridge API")


@app.get("/health")
def health():
    return {"status": "ok"}
