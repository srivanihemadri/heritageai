from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
import app.models  # noqa: F401
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.heritage_sites import router as heritage_sites_router
from app.api.v1.heritage_site_media import router as heritage_site_media_router
from app.api.v1.heritage_site_metadata import router as heritage_site_metadata_router
from app.api.v1.heritage_site_source import router as heritage_site_source_router
from app.api.v1.heritage_site_relation import router as heritage_site_relation_router
from app.api.v1.heritage_site_historical_event import router as heritage_site_historical_event_router
from app.api.v1.users import router as users_router
from app.api.v1.ai import router as ai_router
from app.core.exceptions import (
    HeritageAIException,
    heritageai_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)

app = FastAPI(

    title="HeritageAI API",
    description="Production Backend for HeritageAI",
    version="1.0.0",
)

app.mount(
    "/media",
    StaticFiles(directory=settings.MEDIA_STORAGE_PATH),
    name="media",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HeritageAIException,
    heritageai_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)

app.include_router(
    health_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    heritage_sites_router,
    prefix="/api/v1",
)

app.include_router(
    heritage_site_media_router,
    prefix="/api/v1",
)

app.include_router(
    heritage_site_metadata_router,
    prefix="/api/v1",
)

app.include_router(
    heritage_site_source_router,
    prefix="/api/v1",
)

app.include_router(
    heritage_site_relation_router,
    prefix="/api/v1",
)

app.include_router(
    heritage_site_historical_event_router,
    prefix="/api/v1",
)


app.include_router(
    ai_router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    return {
        "application": "HeritageAI",
        "version": "1.0.0",
        "status": "running",
    }

