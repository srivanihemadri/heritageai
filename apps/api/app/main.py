from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router

app = FastAPI(
    title="HeritageAI API",
    description="Production Backend for HeritageAI",
    version="1.0.0",
)

# API Routes
app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "application": "HeritageAI",
        "version": "1.0.0",
        "status": "running",
    }