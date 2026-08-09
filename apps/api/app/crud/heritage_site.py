from sqlalchemy.orm import Session

from app.core.exceptions import ResourceConflictException, ResourceNotFoundException
from app.models.heritage_site import HeritageSite
from app.schemas.heritage_site import HeritageSiteCreate, HeritageSiteUpdate


def get_heritage_site_by_id(
    db: Session,
    site_id: str,
) -> HeritageSite | None:
    return (
        db.query(HeritageSite)
        .filter(HeritageSite.id == site_id)
        .first()
    )


def get_heritage_site_by_slug(
    db: Session,
    slug: str,
) -> HeritageSite | None:
    return (
        db.query(HeritageSite)
        .filter(HeritageSite.slug == slug)
        .first()
    )


def get_heritage_sites(
    db: Session,
) -> list[HeritageSite]:
    return (
        db.query(HeritageSite)
        .order_by(HeritageSite.created_at.desc())
        .all()
    )


def create_heritage_site(
    db: Session,
    site: HeritageSiteCreate,
) -> HeritageSite:
    existing_site = get_heritage_site_by_slug(
        db,
        site.slug,
    )

    if existing_site:
        raise ResourceConflictException(
            message="Heritage site slug already exists",
            error_code="SLUG_ALREADY_EXISTS",
        )

    db_site = HeritageSite(
        **site.model_dump(),
    )

    db.add(db_site)
    db.commit()
    db.refresh(db_site)

    return db_site


def update_heritage_site(
    db: Session,
    site: HeritageSite,
    data: HeritageSiteUpdate,
) -> HeritageSite:
    updates = data.model_dump(
        exclude_unset=True,
    )

    if "slug" in updates:
        existing_site = get_heritage_site_by_slug(
            db,
            updates["slug"],
        )

        if existing_site and existing_site.id != site.id:
            raise ResourceConflictException(
                message="Heritage site slug already exists",
                error_code="SLUG_ALREADY_EXISTS",
            )

    for field, value in updates.items():
        setattr(site, field, value)

    db.commit()
    db.refresh(site)

    return site


def delete_heritage_site(
    db: Session,
    site: HeritageSite,
) -> None:
    db.delete(site)
    db.commit()


def get_heritage_site_or_404(
    db: Session,
    site_id: str,
) -> HeritageSite:
    site = get_heritage_site_by_id(
        db,
        site_id,
    )

    if not site:
        raise ResourceNotFoundException(
            message="Heritage site not found",
            error_code="HERITAGE_SITE_NOT_FOUND",
        )

    return site
