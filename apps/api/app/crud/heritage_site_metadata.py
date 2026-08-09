from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.models.heritage_site_metadata import HeritageSiteMetadata
from app.schemas.heritage_site_metadata import (
    HeritageSiteMetadataCreate,
    HeritageSiteMetadataUpdate,
)


def get_metadata_by_id(
    db: Session,
    metadata_id: str,
) -> HeritageSiteMetadata | None:
    return (
        db.query(HeritageSiteMetadata)
        .filter(HeritageSiteMetadata.id == metadata_id)
        .first()
    )


def get_metadata_for_site(
    db: Session,
    site_id: str,
) -> list[HeritageSiteMetadata]:
    return (
        db.query(HeritageSiteMetadata)
        .filter(
            HeritageSiteMetadata.site_id == site_id,
            HeritageSiteMetadata.is_active.is_(True),
        )
        .order_by(
            HeritageSiteMetadata.display_order.asc(),
            HeritageSiteMetadata.created_at.asc(),
        )
        .all()
    )


def create_metadata(
    db: Session,
    site_id: str,
    data: HeritageSiteMetadataCreate,
) -> HeritageSiteMetadata:
    db_metadata = HeritageSiteMetadata(
        site_id=site_id,
        **data.model_dump(),
    )

    db.add(db_metadata)
    db.commit()
    db.refresh(db_metadata)

    return db_metadata


def update_metadata(
    db: Session,
    metadata: HeritageSiteMetadata,
    data: HeritageSiteMetadataUpdate,
) -> HeritageSiteMetadata:
    updates = data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(metadata, field, value)

    db.commit()
    db.refresh(metadata)

    return metadata


def delete_metadata(
    db: Session,
    metadata: HeritageSiteMetadata,
) -> None:
    db.delete(metadata)
    db.commit()


def get_metadata_or_404(
    db: Session,
    metadata_id: str,
) -> HeritageSiteMetadata:
    metadata = get_metadata_by_id(
        db,
        metadata_id,
    )

    if not metadata:
        raise ResourceNotFoundException(
            message="Heritage site metadata not found",
            error_code="HERITAGE_SITE_METADATA_NOT_FOUND",
        )

    return metadata
