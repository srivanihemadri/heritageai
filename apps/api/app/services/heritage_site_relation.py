from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundException
from app.crud.heritage_site_relation import (
    create_heritage_site_relation,
    delete_heritage_site_relation,
    get_heritage_site_relation_by_id,
    get_heritage_site_relations_by_site_id,
    update_heritage_site_relation,
)
from app.crud.heritage_site import get_heritage_site_by_id
from app.models.heritage_site_relation import HeritageSiteRelation
from app.schemas.heritage_site_relation import (
    HeritageSiteRelationCreate,
    HeritageSiteRelationUpdate,
)


def create_relation(
    db: Session,
    site_id: str,
    data: HeritageSiteRelationCreate,
) -> HeritageSiteRelation:
    source_site = get_heritage_site_by_id(
        db,
        site_id,
    )

    if source_site is None:
        raise ResourceNotFoundException(
            message="Source heritage site not found",
            error_code="SOURCE_HERITAGE_SITE_NOT_FOUND",
        )

    target_site = get_heritage_site_by_id(
        db,
        data.target_site_id,
    )

    if target_site is None:
        raise ResourceNotFoundException(
            message="Target heritage site not found",
            error_code="TARGET_HERITAGE_SITE_NOT_FOUND",
        )

    if site_id == data.target_site_id:
        raise ResourceNotFoundException(
            message="A heritage site cannot relate to itself",
            error_code="SELF_HERITAGE_SITE_RELATION",
        )

    return create_heritage_site_relation(
        db,
        site_id,
        data,
    )


def get_relation_or_404(
    db: Session,
    relation_id: str,
) -> HeritageSiteRelation:
    relation = get_heritage_site_relation_by_id(
        db,
        relation_id,
    )

    if relation is None:
        raise ResourceNotFoundException(
            message="Heritage site relation not found",
            error_code="HERITAGE_SITE_RELATION_NOT_FOUND",
        )

    return relation


def list_relations(
    db: Session,
    site_id: str,
) -> list[HeritageSiteRelation]:
    site = get_heritage_site_by_id(
        db,
        site_id,
    )

    if site is None:
        raise ResourceNotFoundException(
            message="Heritage site not found",
            error_code="HERITAGE_SITE_NOT_FOUND",
        )

    return get_heritage_site_relations_by_site_id(
        db,
        site_id,
    )


def update_relation(
    db: Session,
    relation_id: str,
    data: HeritageSiteRelationUpdate,
) -> HeritageSiteRelation:
    relation = get_relation_or_404(
        db,
        relation_id,
    )

    return update_heritage_site_relation(
        db,
        relation,
        data,
    )


def delete_relation(
    db: Session,
    relation_id: str,
) -> None:
    relation = get_relation_or_404(
        db,
        relation_id,
    )

    delete_heritage_site_relation(
        db,
        relation,
    )
