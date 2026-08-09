from sqlalchemy.orm import Session

from app.models.heritage_site_historical_event import HeritageSiteHistoricalEvent
from app.schemas.heritage_site_historical_event import (
    HeritageSiteHistoricalEventCreate,
    HeritageSiteHistoricalEventUpdate,
)


def create_heritage_site_historical_event(
    db: Session,
    site_id: str,
    data: HeritageSiteHistoricalEventCreate,
) -> HeritageSiteHistoricalEvent:
    event = HeritageSiteHistoricalEvent(
        site_id=site_id,
        **data.model_dump(),
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_heritage_site_historical_event_by_id(
    db: Session,
    event_id: str,
) -> HeritageSiteHistoricalEvent | None:
    return (
        db.query(HeritageSiteHistoricalEvent)
        .filter(
            HeritageSiteHistoricalEvent.id == event_id,
            HeritageSiteHistoricalEvent.is_active.is_(True),
        )
        .first()
    )


def get_heritage_site_historical_events_by_site_id(
    db: Session,
    site_id: str,
) -> list[HeritageSiteHistoricalEvent]:
    return (
        db.query(HeritageSiteHistoricalEvent)
        .filter(
            HeritageSiteHistoricalEvent.site_id == site_id,
            HeritageSiteHistoricalEvent.is_active.is_(True),
        )
        .order_by(
            HeritageSiteHistoricalEvent.display_order.asc(),
            HeritageSiteHistoricalEvent.event_date.asc(),
            HeritageSiteHistoricalEvent.created_at.asc(),
        )
        .all()
    )


def update_heritage_site_historical_event(
    db: Session,
    event_id: str,
    data: HeritageSiteHistoricalEventUpdate,
) -> HeritageSiteHistoricalEvent | None:
    event = (
        db.query(HeritageSiteHistoricalEvent)
        .filter(HeritageSiteHistoricalEvent.id == event_id)
        .first()
    )

    if event is None:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)

    return event


def delete_heritage_site_historical_event(
    db: Session,
    event_id: str,
) -> bool:
    event = (
        db.query(HeritageSiteHistoricalEvent)
        .filter(HeritageSiteHistoricalEvent.id == event_id)
        .first()
    )

    if event is None:
        return False

    event.is_active = False

    db.commit()

    return True
