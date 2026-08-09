from sqlalchemy.orm import Session

from app.models.heritage_site_source import HeritageSiteSource


def create_heritage_site_source(
    db: Session,
    source: HeritageSiteSource,
) -> HeritageSiteSource:
    db.add(source)
    db.commit()
    db.refresh(source)

    return source


def get_heritage_site_source_by_id(
    db: Session,
    source_id: str,
) -> HeritageSiteSource | None:
    return (
        db.query(HeritageSiteSource)
        .filter(HeritageSiteSource.id == source_id)
        .first()
    )


def get_heritage_site_sources_by_site_id(
    db: Session,
    site_id: str,
) -> list[HeritageSiteSource]:
    return (
        db.query(HeritageSiteSource)
        .filter(
            HeritageSiteSource.site_id == site_id,
            HeritageSiteSource.is_active.is_(True),
        )
        .order_by(
            HeritageSiteSource.display_order.asc(),
            HeritageSiteSource.created_at.asc(),
        )
        .all()
    )


def update_heritage_site_source(
    db: Session,
    source: HeritageSiteSource,
) -> HeritageSiteSource:
    db.commit()
    db.refresh(source)

    return source


def delete_heritage_site_source(
    db: Session,
    source: HeritageSiteSource,
) -> None:
    db.delete(source)
    db.commit()
