from math import ceil

from fastapi import APIRouter, Depends, Query, status
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
    activate_site,
    create_site,
    deactivate_site,
    delete_site,
    get_site,
    list_active_sites,
    update_site,
    verify_site,
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
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    category: str | None = Query(
        default=None,
        max_length=100,
    ),
    country: str | None = Query(
        default=None,
        max_length=100,
    ),
    state: str | None = Query(
        default=None,
        max_length=100,
    ),
    city: str | None = Query(
        default=None,
        max_length=100,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    sites, total = list_active_sites(
        db,
        search=search,
        category=category,
        country=country,
        state=state,
        city=city,
        page=page,
        page_size=page_size,
    )

    total_pages = ceil(total / page_size) if total else 0

    return APIResponse(
        success=True,
        data=HeritageSiteListResponse(
            sites=sites,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
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

@router.post(
    "/{site_id}/verify",
    response_model=APIResponse[HeritageSiteResponse],
)
def verify_heritage_site_endpoint(
    site_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    site = verify_site(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=site,
        message="Heritage site verified successfully",
    )

@router.post(
    "/{site_id}/activate",
    response_model=APIResponse[HeritageSiteResponse],
)
def activate_heritage_site(
    site_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    site = activate_site(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=site,
        message="Heritage site activated successfully",
    )


@router.post(
    "/{site_id}/deactivate",
    response_model=APIResponse[HeritageSiteResponse],
)
def deactivate_heritage_site(
    site_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    site = deactivate_site(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=site,
        message="Heritage site deactivated successfully",
    )
