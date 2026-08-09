from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.db.session import get_db
from app.dependencies import get_current_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.heritage_site_historical_event import (
    HeritageSiteHistoricalEventCreate,
    HeritageSiteHistoricalEventListResponse,
    HeritageSiteHistoricalEventResponse,
    HeritageSiteHistoricalEventUpdate,
)
from app.services.heritage_site_historical_event import (
    create_event,
    delete_event,
    get_event_or_404,
    list_events,
    update_event,
)


router = APIRouter(
    prefix="/heritage-sites/{site_id}/historical-events",
    tags=["Heritage Site Historical Events"],
)


@router.get(
    "",
    response_model=APIResponse[HeritageSiteHistoricalEventListResponse],
)
def list_heritage_site_historical_events(
    site_id: str,
    db: Session = Depends(get_db),
):
    events = list_events(
        db,
        site_id,
    )

    return APIResponse(
        success=True,
        data=HeritageSiteHistoricalEventListResponse(
            events=events,
            total=len(events),
        ),
        message="Heritage site historical events retrieved successfully",
    )


@router.get(
    "/{event_id}",
    response_model=APIResponse[HeritageSiteHistoricalEventResponse],
)
def get_heritage_site_historical_event(
    site_id: str,
    event_id: str,
    db: Session = Depends(get_db),
):
    event = get_event_or_404(
        db,
        event_id,
    )

    if event.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site historical event not found",
            error_code="HERITAGE_SITE_HISTORICAL_EVENT_NOT_FOUND",
        )

    return APIResponse(
        success=True,
        data=event,
        message="Heritage site historical event retrieved successfully",
    )


@router.post(
    "",
    response_model=APIResponse[HeritageSiteHistoricalEventResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_heritage_site_historical_event(
    site_id: str,
    data: HeritageSiteHistoricalEventCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    event = create_event(
        db,
        site_id,
        data,
    )

    return APIResponse(
        success=True,
        data=event,
        message="Heritage site historical event created successfully",
    )


@router.patch(
    "/{event_id}",
    response_model=APIResponse[HeritageSiteHistoricalEventResponse],
)
def update_heritage_site_historical_event(
    site_id: str,
    event_id: str,
    data: HeritageSiteHistoricalEventUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    event = get_event_or_404(
        db,
        event_id,
    )

    if event.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site historical event not found",
            error_code="HERITAGE_SITE_HISTORICAL_EVENT_NOT_FOUND",
        )

    event = update_event(
        db,
        event_id,
        data,
    )

    return APIResponse(
        success=True,
        data=event,
        message="Heritage site historical event updated successfully",
    )


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_heritage_site_historical_event(
    site_id: str,
    event_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    event = get_event_or_404(
        db,
        event_id,
    )

    if event.site_id != site_id:
        raise ResourceNotFoundException(
            message="Heritage site historical event not found",
            error_code="HERITAGE_SITE_HISTORICAL_EVENT_NOT_FOUND",
        )

    delete_event(
        db,
        event_id,
    )

    return None
