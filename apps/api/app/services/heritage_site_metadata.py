from sqlalchemy.orm import Session

from app.crud.heritage_site_metadata import (
    create_metadata,
    delete_metadata,
    get_metadata_or_404,
    get_metadata_for_site,
    update_metadata,
)
from app.models.heritage_site_metadata import HeritageSiteMetadata
from app.schemas.heritage_site_metadata import (
    HeritageSiteMetadataCreate,
    HeritageSiteMetadataUpdate,
)


def create_site_metadata(
    db: Session,
    site_id: str,
    data: HeritageSiteMetadataCreate,
) -> HeritageSiteMetadata:
    return create_metadata(
        db,
        site_id,
        data,
    )


def list_site_metadata(
    db: Session,
    site_id: str,
) -> list[HeritageSiteMetadata]:
    return get_metadata_for_site(
        db,
        site_id,
    )


def get_site_metadata(
    db: Session,
    metadata_id: str,
) -> HeritageSiteMetadata:
    return get_metadata_or_404(
        db,
        metadata_id,
    )


def update_site_metadata(
    db: Session,
    metadata_id: str,
    data: HeritageSiteMetadataUpdate,
) -> HeritageSiteMetadata:
    metadata = get_metadata_or_404(
        db,
        metadata_id,
    )

    return update_metadata(
        db,
        metadata,
        data,
    )


def delete_site_metadata(
    db: Session,
    metadata_id: str,
) -> None:
    metadata = get_metadata_or_404(
        db,
        metadata_id,
    )

    delete_metadata(
        db,
        metadata,
    )
