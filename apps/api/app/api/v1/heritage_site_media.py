from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.heritage_site_media import (
    HeritageSiteMediaCreate,
    HeritageSiteMediaListResponse,
    HeritageSiteMediaResponse,
    HeritageSiteMediaUpdate,
)
from app.services.heritage_site_media import (
    create_site_media,
    delete_site_media,
    get_site_media,
    list_site_media,
    update_site_media,
)


router = APIRouter(
    prefix="/heritage-sites/{site_id}/media",
    tags=["Heritage Site Media"],
)


@router.get(
    "",
    response_model=APIResponse[HeritageSiteMediaListResponse],
)
def list_media(
    site_id: str,
    db: Session = Depends(get_db),
):
    media = list_site_media(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=HeritageSiteMediaListResponse(
            media=media,
            total=len(media),
        ),
        message="Heritage site media retrieved successfully",
    )


@router.get(
    "/{media_id}",
    response_model=APIResponse[HeritageSiteMediaResponse],
)
def get_media(
    site_id: str,
    media_id: str,
    db: Session = Depends(get_db),
):
    media = get_site_media(
        db,
        site_id,
        media_id,
    )

    return APIResponse(
        success=True,
        data=media,
        message="Heritage site media retrieved successfully",
    )


@router.post(
    "",
    response_model=APIResponse[HeritageSiteMediaResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_media(
    site_id: str,
    data: HeritageSiteMediaCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    media = create_site_media(
        db,
        site_id,
        data,
    )

    return APIResponse(
        success=True,
        data=media,
        message="Heritage site media created successfully",
    )


@router.patch(
    "/{media_id}",
    response_model=APIResponse[HeritageSiteMediaResponse],
)
def update_media(
    site_id: str,
    media_id: str,
    data: HeritageSiteMediaUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    media = update_site_media(
        db,
        site_id,
        media_id,
        data,
    )

    return APIResponse(
        success=True,
        data=media,
        message="Heritage site media updated successfully",
    )


@router.delete(
    "/{media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_media(
    site_id: str,
    media_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    delete_site_media(
        db,
        site_id,
        media_id,
    )

    return None
