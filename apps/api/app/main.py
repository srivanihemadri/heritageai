from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.heritage_sites import router as heritage_sites_router
from app.api.v1.heritage_site_media import router as heritage_site_media_router
from app.api.v1.users import router as users_router
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


@app.get("/")
def root():
    return {
        "application": "HeritageAI",
        "version": "1.0.0",
        "status": "running",
    }
