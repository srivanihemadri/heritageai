from sqlalchemy.orm import Session

from app.crud.heritage_site import (
    create_heritage_site,
    delete_heritage_site,
    get_heritage_site_or_404,
    search_heritage_sites,
    update_heritage_site,
)
from app.models.heritage_site import HeritageSite
from app.schemas.heritage_site import (
    HeritageSiteCreate,
    HeritageSiteUpdate,
)


def create_site(
    db: Session,
    data: HeritageSiteCreate,
) -> HeritageSite:
    return create_heritage_site(
        db,
        data,
    )


def list_active_sites(
    db: Session,
    *,
    search: str | None = None,
    category: str | None = None,
    country: str | None = None,
    state: str | None = None,
    city: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[HeritageSite], int]:
    return search_heritage_sites(
        db,
        search=search,
        category=category,
        country=country,
        state=state,
        city=city,
        page=page,
        page_size=page_size,
    )


def get_site(
    db: Session,
    site_id: str,
) -> HeritageSite:
    return get_heritage_site_or_404(
        db,
        site_id,
    )


def update_site(
    db: Session,
    site_id: str,
    data: HeritageSiteUpdate,
) -> HeritageSite:
    site = get_heritage_site_or_404(
        db,
        site_id,
    )

    return update_heritage_site(
        db,
        site,
        data,
    )


def delete_site(
    db: Session,
    site_id: str,
) -> None:
    site = get_heritage_site_or_404(
        db,
        site_id,
    )

    delete_heritage_site(
        db,
        site,
    )
