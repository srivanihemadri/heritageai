from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.heritage_site import (
    HeritageSiteCreate,
    HeritageSiteListResponse,
    HeritageSiteResponse,
    HeritageSiteUpdate,
)
from app.services.heritage_site import (
    create_site,
    delete_site,
    get_site,
    list_active_sites,
    update_site,
)

router = APIRouter(
    prefix="/heritage-sites",
    tags=["Heritage Sites"],
)


@router.get(
    "",
    response_model=APIResponse[HeritageSiteListResponse],
)
def list_heritage_sites(
    db: Session = Depends(get_db),
):
    sites = list_active_sites(db)

    return APIResponse(
        success=True,
        data=HeritageSiteListResponse(
            sites=sites,
            total=len(sites),
        ),
        message="Heritage sites retrieved successfully",
    )


@router.get(
    "/{site_id}",
    response_model=APIResponse[HeritageSiteResponse],
)
def get_heritage_site(
    site_id: str,
    db: Session = Depends(get_db),
):
    site = get_site(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=site,
        message="Heritage site retrieved successfully",
    )


@router.post(
    "",
    response_model=APIResponse[HeritageSiteResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_heritage_site(
    data: HeritageSiteCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    site = create_site(
        db,
        data,
    )

    return APIResponse(
        success=True,
        data=site,
        message="Heritage site created successfully",
    )


@router.patch(
    "/{site_id}",
    response_model=APIResponse[HeritageSiteResponse],
)
def update_heritage_site(
    site_id: str,
    data: HeritageSiteUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    site = update_site(
        db,
        site_id,
        data,
    )

    return APIResponse(
        success=True,
        data=site,
        message="Heritage site updated successfully",
    )


@router.delete(
    "/{site_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_heritage_site(
    site_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    delete_site(
        db,
        site_id,
    )

    return None
