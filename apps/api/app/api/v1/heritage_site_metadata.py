from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.heritage_site_metadata import (
    HeritageSiteMetadataCreate,
    HeritageSiteMetadataListResponse,
    HeritageSiteMetadataResponse,
    HeritageSiteMetadataUpdate,
)
from app.services.heritage_site_metadata import (
    create_site_metadata,
    delete_site_metadata,
    get_site_metadata,
    list_site_metadata,
    update_site_metadata,
)

router = APIRouter(
    prefix="/heritage-sites/{site_id}/metadata",
    tags=["Heritage Site Metadata"],
)


@router.get(
    "",
    response_model=APIResponse[HeritageSiteMetadataListResponse],
)
def list_metadata(
    site_id: str,
    db: Session = Depends(get_db),
):
    metadata = list_site_metadata(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=HeritageSiteMetadataListResponse(
            metadata=metadata,
            total=len(metadata),
        ),
        message="Heritage site metadata retrieved successfully",
    )


@router.get(
    "/{metadata_id}",
    response_model=APIResponse[HeritageSiteMetadataResponse],
)
def get_metadata(
    site_id: str,
    metadata_id: str,
    db: Session = Depends(get_db),
):
    metadata = get_site_metadata(
        db,
        metadata_id,
    )

    if metadata.site_id != site_id:
        from app.core.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException(
            message="Heritage site metadata not found",
            error_code="HERITAGE_SITE_METADATA_NOT_FOUND",
        )

    return APIResponse(
        success=True,
        data=metadata,
        message="Heritage site metadata retrieved successfully",
    )


@router.post(
    "",
    response_model=APIResponse[HeritageSiteMetadataResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_metadata(
    site_id: str,
    data: HeritageSiteMetadataCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    metadata = create_site_metadata(
        db,
        site_id,
        data,
    )

    return APIResponse(
        success=True,
        data=metadata,
        message="Heritage site metadata created successfully",
    )


@router.patch(
    "/{metadata_id}",
    response_model=APIResponse[HeritageSiteMetadataResponse],
)
def update_metadata(
    site_id: str,
    metadata_id: str,
    data: HeritageSiteMetadataUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    metadata = get_site_metadata(
        db,
        metadata_id,
    )

    if metadata.site_id != site_id:
        from app.core.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException(
            message="Heritage site metadata not found",
            error_code="HERITAGE_SITE_METADATA_NOT_FOUND",
        )

    metadata = update_site_metadata(
        db,
        metadata_id,
        data,
    )

    return APIResponse(
        success=True,
        data=metadata,
        message="Heritage site metadata updated successfully",
    )


@router.delete(
    "/{metadata_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_metadata(
    site_id: str,
    metadata_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    metadata = get_site_metadata(
        db,
        metadata_id,
    )

    if metadata.site_id != site_id:
        from app.core.exceptions import ResourceNotFoundException

        raise ResourceNotFoundException(
            message="Heritage site metadata not found",
            error_code="HERITAGE_SITE_METADATA_NOT_FOUND",
        )

    delete_site_metadata(
        db,
        metadata_id,
    )

    return None
