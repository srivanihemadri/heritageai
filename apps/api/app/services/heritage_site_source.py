from sqlalchemy.orm import Session

from app.crud.heritage_site_source import (
    create_heritage_site_source,
    delete_heritage_site_source,
    get_heritage_site_source_by_id,
    get_heritage_site_sources_by_site_id,
    update_heritage_site_source,
)
from app.core.exceptions import ResourceNotFoundException
from app.models.heritage_site_source import HeritageSiteSource


def create_source(
    db: Session,
    source: HeritageSiteSource,
) -> HeritageSiteSource:
    return create_heritage_site_source(
        db,
        source,
    )


def get_source_or_404(
    db: Session,
    source_id: str,
) -> HeritageSiteSource:
    source = get_heritage_site_source_by_id(
        db,
        source_id,
    )

    if not source:
        raise ResourceNotFoundException(
            message="Heritage site source not found",
            error_code="HERITAGE_SITE_SOURCE_NOT_FOUND",
        )

    return source


def list_sources(
    db: Session,
    site_id: str,
) -> list[HeritageSiteSource]:
    return get_heritage_site_sources_by_site_id(
        db,
        site_id,
    )


def update_source(
    db: Session,
    source: HeritageSiteSource,
) -> HeritageSiteSource:
    return update_heritage_site_source(
        db,
        source,
    )


def delete_source(
    db: Session,
    source_id: str,
) -> None:
    source = get_source_or_404(
        db,
        source_id,
    )

    delete_heritage_site_source(
        db,
        source,
    )
