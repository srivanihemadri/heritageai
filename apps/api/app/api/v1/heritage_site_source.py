from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.heritage_site_source import HeritageSiteSource
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.heritage_site_source import (
    HeritageSiteSourceCreate,
    HeritageSiteSourceListResponse,
    HeritageSiteSourceResponse,
    HeritageSiteSourceUpdate,
)
from app.services.heritage_site_source import (
    create_source,
    delete_source,
    get_source_or_404,
    list_sources,
    update_source,
)

router = APIRouter(
    prefix="/heritage-sites/{site_id}/sources",
    tags=["Heritage Site Sources"],
)


@router.get(
    "",
    response_model=APIResponse[HeritageSiteSourceListResponse],
)
def get_sources(
    site_id: str,
    db: Session = Depends(get_db),
):
    sources = list_sources(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=HeritageSiteSourceListResponse(
            sources=sources,
            total=len(sources),
        ),
        message="Heritage site sources retrieved successfully",
    )


@router.get(
    "/{source_id}",
    response_model=APIResponse[HeritageSiteSourceResponse],
)
def get_source(
    site_id: str,
    source_id: str,
    db: Session = Depends(get_db),
):
    source = get_source_or_404(
        db,
        source_id,
    )

    if source.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site source not found",
            error_code="HERITAGE_SITE_SOURCE_NOT_FOUND",
        )

    return APIResponse(
        success=True,
        data=source,
        message="Heritage site source retrieved successfully",
    )


@router.post(
    "",
    response_model=APIResponse[HeritageSiteSourceResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_source_endpoint(
    site_id: str,
    data: HeritageSiteSourceCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    source = HeritageSiteSource(
        site_id=site_id,
        source_type=data.source_type,
        title=data.title,
        author=data.author,
        organization=data.organization,
        publisher=data.publisher,
        publication_date=data.publication_date,
        url=data.url,
        citation_text=data.citation_text,
        language=data.language,
    )

    source = create_source(
        db,
        source,
    )

    return APIResponse(
        success=True,
        data=source,
        message="Heritage site source created successfully",
    )


@router.patch(
    "/{source_id}",
    response_model=APIResponse[HeritageSiteSourceResponse],
)
def update_source_endpoint(
    site_id: str,
    source_id: str,
    data: HeritageSiteSourceUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    source = get_source_or_404(
        db,
        source_id,
    )

    if source.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site source not found",
            error_code="HERITAGE_SITE_SOURCE_NOT_FOUND",
        )

    update_data = data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(source, field, value)

    source = update_source(
        db,
        source,
    )

    return APIResponse(
        success=True,
        data=source,
        message="Heritage site source updated successfully",
    )


@router.delete(
    "/{source_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_source_endpoint(
    site_id: str,
    source_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    source = get_source_or_404(
        db,
        source_id,
    )

    if source.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site source not found",
            error_code="HERITAGE_SITE_SOURCE_NOT_FOUND",
        )

    delete_source(
        db,
        source_id,
    )

    return None
