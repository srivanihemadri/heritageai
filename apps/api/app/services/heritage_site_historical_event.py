from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.crud.heritage_site_historical_event import (
    create_heritage_site_historical_event,
    delete_heritage_site_historical_event,
    get_heritage_site_historical_event_by_id,
    get_heritage_site_historical_events_by_site_id,
    update_heritage_site_historical_event,
)
from app.schemas.heritage_site_historical_event import (
    HeritageSiteHistoricalEventCreate,
    HeritageSiteHistoricalEventUpdate,
)


def create_event(
    db: Session,
    site_id: str,
    data: HeritageSiteHistoricalEventCreate,
):
    return create_heritage_site_historical_event(
        db,
        site_id,
        data,
    )


def get_event_or_404(
    db: Session,
    event_id: str,
):
    event = get_heritage_site_historical_event_by_id(
        db,
        event_id,
    )

    if event is None:
        raise ResourceNotFoundException(
            message="Heritage site historical event not found",
            error_code="HERITAGE_SITE_HISTORICAL_EVENT_NOT_FOUND",
        )

    return event


def list_events(
    db: Session,
    site_id: str,
):
    return get_heritage_site_historical_events_by_site_id(
        db,
        site_id,
    )


def update_event(
    db: Session,
    event_id: str,
    data: HeritageSiteHistoricalEventUpdate,
):
    event = update_heritage_site_historical_event(
        db,
        event_id,
        data,
    )

    if event is None:
        raise ResourceNotFoundException(
            message="Heritage site historical event not found",
            error_code="HERITAGE_SITE_HISTORICAL_EVENT_NOT_FOUND",
        )

    return event


def delete_event(
    db: Session,
    event_id: str,
):
    deleted = delete_heritage_site_historical_event(
        db,
        event_id,
    )

    if not deleted:
        raise ResourceNotFoundException(
            message="Heritage site historical event not found",
            error_code="HERITAGE_SITE_HISTORICAL_EVENT_NOT_FOUND",
        )
