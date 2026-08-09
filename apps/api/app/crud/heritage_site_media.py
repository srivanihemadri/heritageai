from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models.heritage_site_media import HeritageSiteMedia
from app.schemas.heritage_site_media import (
    HeritageSiteMediaCreate,
    HeritageSiteMediaUpdate,
)


def get_media_by_id(
    db: Session,
    media_id: str,
) -> HeritageSiteMedia | None:
    return (
        db.query(HeritageSiteMedia)
        .filter(HeritageSiteMedia.id == media_id)
        .first()
    )


def get_media_for_site(
    db: Session,
    site_id: str,
) -> list[HeritageSiteMedia]:
    return (
        db.query(HeritageSiteMedia)
        .filter(
            HeritageSiteMedia.site_id == site_id,
            HeritageSiteMedia.is_active.is_(True),
        )
        .order_by(
            HeritageSiteMedia.display_order.asc(),
            HeritageSiteMedia.created_at.asc(),
        )
        .all()
    )


def create_media(
    db: Session,
    site_id: str,
    data: HeritageSiteMediaCreate,
) -> HeritageSiteMedia:
    db_media = HeritageSiteMedia(
        site_id=site_id,
        **data.model_dump(),
    )

    db.add(db_media)
    db.commit()
    db.refresh(db_media)

    return db_media


def update_media(
    db: Session,
    media: HeritageSiteMedia,
    data: HeritageSiteMediaUpdate,
) -> HeritageSiteMedia:
    updates = data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(media, field, value)

    db.commit()
    db.refresh(media)

    return media


def delete_media(
    db: Session,
    media: HeritageSiteMedia,
) -> None:
    db.delete(media)
    db.commit()


def get_media_or_404(
    db: Session,
    media_id: str,
) -> HeritageSiteMedia:
    media = get_media_by_id(
        db,
        media_id,
    )

    if not media:
        raise ResourceNotFoundException(
            message="Heritage site media not found",
            error_code="HERITAGE_SITE_MEDIA_NOT_FOUND",
        )

    return media
