from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.crud.heritage_site import get_heritage_site_by_id
from app.crud.heritage_site_media import (
    create_media,
    delete_media,
    get_media_for_site,
    get_media_or_404,
    update_media,
)
from app.models.heritage_site_media import HeritageSiteMedia
from app.schemas.heritage_site_media import (
    HeritageSiteMediaCreate,
    HeritageSiteMediaUpdate,
)


def create_site_media(
    db: Session,
    site_id: str,
    data: HeritageSiteMediaCreate,
) -> HeritageSiteMedia:
    site = get_heritage_site_by_id(
        db,
        site_id,
    )

    if not site:
        raise ResourceNotFoundException(
            message="Heritage site not found",
            error_code="HERITAGE_SITE_NOT_FOUND",
        )

    return create_media(
        db,
        site_id,
        data,
    )


def list_site_media(
    db: Session,
    site_id: str,
) -> list[HeritageSiteMedia]:
    site = get_heritage_site_by_id(
        db,
        site_id,
    )

    if not site:
        raise ResourceNotFoundException(
            message="Heritage site not found",
            error_code="HERITAGE_SITE_NOT_FOUND",
        )

    return get_media_for_site(
        db,
        site_id,
    )


def get_site_media(
    db: Session,
    site_id: str,
    media_id: str,
) -> HeritageSiteMedia:
    media = get_media_or_404(
        db,
        media_id,
    )

    if media.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site media not found",
            error_code="HERITAGE_SITE_MEDIA_NOT_FOUND",
        )

    return media


def update_site_media(
    db: Session,
    site_id: str,
    media_id: str,
    data: HeritageSiteMediaUpdate,
) -> HeritageSiteMedia:
    media = get_site_media(
        db,
        site_id,
        media_id,
    )

    return update_media(
        db,
        media,
        data,
    )


def delete_site_media(
    db: Session,
    site_id: str,
    media_id: str,
) -> None:
    media = get_site_media(
        db,
        site_id,
        media_id,
    )

    delete_media(
        db,
        media,
    )
